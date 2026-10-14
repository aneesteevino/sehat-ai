import { proxyAuthenticatedJson } from '@/lib/authenticated-proxy'

export async function POST(request: Request) {
  return proxyAuthenticatedJson(request, '/api/v1/safety/check', 'Safety check is unavailable.')
}
