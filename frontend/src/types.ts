export type Language = 'fi' | 'en'
export type AuthMode = 'login' | 'register'

export type AuthenticatedUser = {
  id: number
  first_name: string
  last_name: string
  username: string
  email: string
}
