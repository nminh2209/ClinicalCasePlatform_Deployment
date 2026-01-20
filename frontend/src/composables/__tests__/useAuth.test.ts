/**
 * Tests for useAuth composable
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useAuth } from '@/composables/useAuth'
import axios from 'axios'

vi.mock('axios')

describe('useAuth', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('initializes with no user when no token', () => {
    const { user, isAuthenticated } = useAuth()
    
    expect(user.value).toBeNull()
    expect(isAuthenticated.value).toBe(false)
  })

  it('loads user from localStorage token', async () => {
    localStorage.setItem('access_token', 'fake-token')
    vi.mocked(axios.get).mockResolvedValue({
      data: { id: 1, email: 'test@test.com', role: 'student' }
    })

    const { user, loadUser } = useAuth()
    await loadUser()

    expect(user.value).toEqual({
      id: 1,
      email: 'test@test.com',
      role: 'student'
    })
  })

  it('login stores token and loads user', async () => {
    vi.mocked(axios.post).mockResolvedValue({
      data: { access: 'new-token', refresh: 'refresh-token' }
    })
    vi.mocked(axios.get).mockResolvedValue({
      data: { id: 1, email: 'test@test.com' }
    })

    const { login, user } = useAuth()
    await login('test@test.com', 'password')

    expect(localStorage.getItem('access_token')).toBe('new-token')
    expect(user.value).toBeTruthy()
  })

  it('logout clears token and user', () => {
    localStorage.setItem('access_token', 'token')
    
    const { logout, user, isAuthenticated } = useAuth()
    logout()

    expect(localStorage.getItem('access_token')).toBeNull()
    expect(user.value).toBeNull()
    expect(isAuthenticated.value).toBe(false)
  })

  it('checks if user has role', () => {
    const { user, hasRole } = useAuth()
    user.value = { id: 1, email: 'test@test.com', role: 'instructor' }

    expect(hasRole('instructor')).toBe(true)
    expect(hasRole('student')).toBe(false)
    expect(hasRole('admin')).toBe(false)
  })
})
