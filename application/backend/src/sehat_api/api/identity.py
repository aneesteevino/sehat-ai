"""Versioned authentication endpoints and authorization dependencies."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

from sehat_api.identity.models import Role, UserRecord
from sehat_api.identity.service import (
    DuplicateEmailError,
    IdentityService,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidSessionError,
)

router = APIRouter(prefix="/api/v1/auth", tags=["identity"])
bearer_scheme = HTTPBearer(auto_error=False)
DisplayName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=80),
]


class RegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    display_name: DisplayName
    password: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    email: EmailStr
    display_name: str
    role: Role

    @classmethod
    def from_record(cls, user: UserRecord) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            role=user.role,
        )


class SessionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class MessageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str


def get_identity_service(request: Request) -> IdentityService:
    return request.app.state.identity_service


async def get_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    if credentials is None or credentials.scheme.casefold() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


async def get_current_user(
    token: Annotated[str, Depends(get_bearer_token)],
    service: Annotated[IdentityService, Depends(get_identity_service)],
) -> UserRecord:
    try:
        return await service.authenticate(token)
    except InvalidSessionError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session is invalid or expired.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def require_roles(*allowed_roles: Role):
    async def authorize(
        user: Annotated[UserRecord, Depends(get_current_user)],
    ) -> UserRecord:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account does not have permission to perform that action.",
            )
        return user

    return authorize


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegistrationRequest,
    service: Annotated[IdentityService, Depends(get_identity_service)],
) -> UserResponse:
    try:
        user = await service.register(payload.email, payload.display_name, payload.password)
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from exc
    return UserResponse.from_record(user)


@router.post("/login", response_model=SessionResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    service: Annotated[IdentityService, Depends(get_identity_service)],
) -> SessionResponse:
    try:
        user, token, _session = await service.sign_in(payload.email, payload.password)
    except (InvalidCredentialsError, InactiveUserError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The email or password is incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return SessionResponse(
        access_token=token,
        expires_in=request.app.state.settings.session_ttl_minutes * 60,
        user=UserResponse.from_record(user),
    )


@router.get("/me", response_model=UserResponse)
async def me(user: Annotated[UserRecord, Depends(get_current_user)]) -> UserResponse:
    return UserResponse.from_record(user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    token: Annotated[str, Depends(get_bearer_token)],
    service: Annotated[IdentityService, Depends(get_identity_service)],
) -> MessageResponse:
    await service.sign_out(token)
    return MessageResponse(message="Signed out.")
