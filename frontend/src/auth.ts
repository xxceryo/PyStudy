import { computed, reactive } from 'vue'
import { ApiError, apiRequest } from './api'
import type { LoginResponse, PublicUser, RegisterPayload } from './types'

const TOKEN_KEY = 'loot_shift_access_token'

const state = reactive<{
  token: string | null
  user: PublicUser | null
  initialized: boolean
}>({
  token: localStorage.getItem(TOKEN_KEY),
  user: null,
  initialized: false,
})

function clearSession(): void {
  state.token = null
  state.user = null
  localStorage.removeItem(TOKEN_KEY)
}

async function restoreSession(): Promise<void> {
  if (state.initialized) return
  if (!state.token) {
    state.initialized = true
    return
  }

  try {
    state.user = await apiRequest<PublicUser>('/auth/me', {}, state.token)
  } catch {
    clearSession()
  } finally {
    state.initialized = true
  }
}

async function login(username: string, password: string): Promise<void> {
  const response = await apiRequest<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
  state.token = response.access_token
  state.user = response.user
  state.initialized = true
  localStorage.setItem(TOKEN_KEY, response.access_token)
}

async function register(payload: RegisterPayload): Promise<PublicUser> {
  return apiRequest<PublicUser>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

async function loadCurrentUser(): Promise<void> {
  if (!state.token) return
  try {
    state.user = await apiRequest<PublicUser>('/auth/me', {}, state.token)
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      clearSession()
    }
    throw error
  }
}

export const auth = {
  state,
  isAuthenticated: computed(() => Boolean(state.token && state.user)),
  clearSession,
  loadCurrentUser,
  login,
  register,
  restoreSession,
}
