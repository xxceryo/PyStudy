export interface PublicUser {
  id: number
  username: string
  nickname: string | null
  avatar_url: string | null
  signature: string | null
}

export interface LoginResponse {
  access_token: string
  token_type: 'bearer'
  expires_in: number
  user: PublicUser
}

export interface RegisterPayload {
  username: string
  password: string
  nickname: string
}
