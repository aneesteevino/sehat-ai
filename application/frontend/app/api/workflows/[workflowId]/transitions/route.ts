import { proxyAuthenticatedJson } from '@/lib/authenticated-proxy'

type RouteContext = { params: Promise<{ workflowId: string }> }

export async function POST(request: Request, context: RouteContext) {
  const { workflowId } = await context.params
  return proxyAuthenticatedJson(
    request,
    `/api/v1/workflows/${encodeURIComponent(workflowId)}/transitions`,
    'Workflow transition is unavailable.',
  )
}
