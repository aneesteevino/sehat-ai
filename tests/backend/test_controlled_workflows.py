import pytest
from sehat_api.audit.ledger import InMemoryAuditLedger
from sehat_api.generation.models import ProviderRequest, ProviderResult, ProviderUsage
from sehat_api.generation.service import GenerationService
from sehat_api.generation.usage import InMemoryUsageLedger
from sehat_api.safety.policy import RedFlagPolicy
from sehat_api.workflows.service import (
    IdempotencyConflictError,
    InvalidTransitionError,
    WorkflowNotFoundError,
    WorkflowService,
)


class CountingRetrieval:
    def __init__(self) -> None:
        self.calls = 0

    async def search(self, query: str, *, limit: int = 5):
        self.calls += 1
        return []


class CountingProvider:
    name = "counting"
    model = "test"

    def __init__(self) -> None:
        self.calls = 0

    async def generate(self, request: ProviderRequest) -> ProviderResult:
        self.calls += 1
        return ProviderResult(
            payload={}, usage=ProviderUsage(input_units=0, output_units=0)
        )


@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("I can't breathe", "breathing"),
        ("I have severe chest pressure", "chest"),
        ("They are unconscious", "consciousness"),
        ("The heavy bleeding will not stop", "bleeding"),
        ("Their face is drooping", "stroke"),
    ],
)
def test_red_flags_return_application_owned_emergency_decision(
    text: str, category: str
) -> None:
    decision = RedFlagPolicy().evaluate(text)

    assert decision.level == "emergency"
    assert category in decision.categories
    assert "local emergency services" in decision.message


@pytest.mark.asyncio
async def test_emergency_answer_bypasses_retrieval_and_generation() -> None:
    retrieval = CountingRetrieval()
    provider = CountingProvider()
    service = GenerationService(
        retrieval,  # type: ignore[arg-type]
        provider,
        InMemoryUsageLedger(),
    )

    answer = await service.answer("I have severe chest pain")

    assert answer.status == "escalated"
    assert answer.escalation is not None
    assert answer.usage.attempts == 0
    assert retrieval.calls == 0
    assert provider.calls == 0


@pytest.mark.asyncio
async def test_symptom_workflow_enforces_order_and_idempotency() -> None:
    audit = InMemoryAuditLedger()
    service = WorkflowService(audit)
    started = await service.start(
        owner_user_id="user-1",
        kind="symptom_questionnaire",
        idempotency_key="start-key-1",
        request_id="request-1",
    )
    replay = await service.start(
        owner_user_id="user-1",
        kind="symptom_questionnaire",
        idempotency_key="start-key-1",
        request_id="request-2",
    )
    assert replay == started
    assert len(await audit.list_events()) == 1

    collecting = await service.transition(
        owner_user_id="user-1",
        workflow_id=started.id,
        action="begin",
        idempotency_key="begin-key-1",
        request_id="request-3",
    )
    assert collecting.state == "collecting"
    review = await service.transition(
        owner_user_id="user-1",
        workflow_id=started.id,
        action="submit",
        idempotency_key="submit-key-1",
        request_id="request-4",
        payload={"concern": "fever", "duration": "days", "severity": "moderate"},
    )
    assert review.state == "review"
    assert review.summary == ("concern:fever", "duration:days", "severity:moderate")
    completed = await service.transition(
        owner_user_id="user-1",
        workflow_id=started.id,
        action="complete",
        idempotency_key="complete-key-1",
        request_id="request-5",
    )
    assert completed.state == "completed"


@pytest.mark.asyncio
async def test_workflow_rejects_invalid_transition_owner_and_key_reuse() -> None:
    service = WorkflowService(InMemoryAuditLedger())
    started = await service.start(
        owner_user_id="owner",
        kind="symptom_questionnaire",
        idempotency_key="start-owner",
        request_id="request-1",
    )
    with pytest.raises(InvalidTransitionError):
        await service.transition(
            owner_user_id="owner",
            workflow_id=started.id,
            action="complete",
            idempotency_key="bad-order",
            request_id="request-2",
        )
    with pytest.raises(WorkflowNotFoundError):
        await service.transition(
            owner_user_id="other-user",
            workflow_id=started.id,
            action="begin",
            idempotency_key="other-begin",
            request_id="request-3",
        )
    with pytest.raises(IdempotencyConflictError):
        await service.start(
            owner_user_id="owner",
            kind="document_explanation",
            idempotency_key="start-owner",
            request_id="request-4",
        )


@pytest.mark.asyncio
async def test_document_workflow_requires_synthetic_bounded_facts() -> None:
    audit = InMemoryAuditLedger()
    service = WorkflowService(audit)
    started = await service.start(
        owner_user_id="user-1",
        kind="document_explanation",
        idempotency_key="document-start",
        request_id="request-1",
    )
    await service.transition(
        owner_user_id="user-1",
        workflow_id=started.id,
        action="begin",
        idempotency_key="document-begin",
        request_id="request-2",
    )
    with pytest.raises(InvalidTransitionError):
        await service.transition(
            owner_user_id="user-1",
            workflow_id=started.id,
            action="submit",
            idempotency_key="document-real",
            request_id="request-3",
            payload={"synthetic": False, "facts": [{"label": "Result", "value": "42"}]},
        )
    review = await service.transition(
        owner_user_id="user-1",
        workflow_id=started.id,
        action="submit",
        idempotency_key="document-synthetic",
        request_id="request-4",
        payload={"synthetic": True, "facts": [{"label": "Example", "value": "Normal"}]},
    )
    assert review.summary == ("Example: Normal",)
    audit_text = repr(await audit.list_events())
    assert "Normal" not in audit_text
    assert "facts" not in audit_text


@pytest.mark.asyncio
async def test_audit_metadata_rejects_health_content_keys() -> None:
    with pytest.raises(ValueError, match="non-allow-listed"):
        await InMemoryAuditLedger().record(
            actor_user_id="user",
            action="test",
            target_type="workflow",
            target_id="id",
            outcome="success",
            request_id="request",
            metadata={"symptom_text": "private"},
        )
