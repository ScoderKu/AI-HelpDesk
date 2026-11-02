export type Language = 'fi' | 'en'
export type AuthMode = 'login' | 'register'

export type AuthStatus = { must_change_password: boolean }

export type AuthenticatedUser = {
  id: number
  first_name: string
  last_name: string
  username: string
  email: string
}

export type TicketStatus = 'OPEN' | 'CLOSED'
export type TicketPriority = 'LOW' | 'MEDIUM' | 'HIGH'

export type Ticket = {
  id: number
  title: string
  description: string
  status: TicketStatus
  priority: TicketPriority
  created_at: string
}

export type TicketSummary = {
  total: number
  open: number
  closed: number
}


export type UserProfileUpdate = Pick<AuthenticatedUser, 'first_name' | 'last_name' | 'username'>

export type PasswordChange = {
  current_password: string
  new_password: string
  confirm_new_password: string
}
