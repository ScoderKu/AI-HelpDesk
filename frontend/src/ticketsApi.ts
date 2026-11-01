import { API_BASE_URL } from './api'
import type { Ticket, TicketPriority, TicketSummary } from './types'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}/api/v1${path}`, {
    ...init,
    credentials: 'include',
    headers: {
      ...(init?.body ? { 'Content-Type': 'application/json' } : {}),
      ...init?.headers,
    },
  })
  if (!response.ok) {
    const error = new Error(`Ticket request failed: ${response.status}`)
    Object.assign(error, { status: response.status })
    throw error
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export const ticketsApi = {
  list: () => request<Ticket[]>('/tickets'),
  summary: () => request<TicketSummary>('/tickets/summary'),
  get: (id: number) => request<Ticket>(`/tickets/${id}`),
  create: (ticket: { title: string; description: string; priority: TicketPriority }) =>
    request<Ticket>('/tickets', { method: 'POST', body: JSON.stringify(ticket) }),
  update: (id: number, ticket: { title: string; description: string; priority: TicketPriority }) =>
    request<Ticket>(`/tickets/${id}`, { method: 'PATCH', body: JSON.stringify(ticket) }),
  close: (id: number) =>
    request<Ticket>(`/tickets/${id}/close`, { method: 'POST' }),
}
