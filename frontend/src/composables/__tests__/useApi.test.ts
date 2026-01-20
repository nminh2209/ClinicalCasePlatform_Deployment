/**
 * Tests for useApi composable
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useApi } from '@/composables/useApi'
import axios from 'axios'

vi.mock('axios')

describe('useApi', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches data successfully', async () => {
    vi.mocked(axios.get).mockResolvedValue({
      data: { id: 1, title: 'Test Case' }
    })

    const { data, loading, error, fetchData } = useApi()
    await fetchData('/api/cases/1/')

    expect(loading.value).toBe(false)
    expect(error.value).toBeNull()
    expect(data.value).toEqual({ id: 1, title: 'Test Case' })
  })

  it('handles fetch errors', async () => {
    vi.mocked(axios.get).mockRejectedValue(new Error('Network error'))

    const { error, fetchData } = useApi()
    await fetchData('/api/cases/1/')

    expect(error.value).toBeTruthy()
  })

  it('sets loading state during fetch', async () => {
    vi.mocked(axios.get).mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({ data: {} }), 100))
    )

    const { loading, fetchData } = useApi()
    
    const fetchPromise = fetchData('/api/test/')
    expect(loading.value).toBe(true)
    
    await fetchPromise
    expect(loading.value).toBe(false)
  })

  it('posts data successfully', async () => {
    vi.mocked(axios.post).mockResolvedValue({
      data: { id: 2, title: 'Created' }
    })

    const { data, postData } = useApi()
    await postData('/api/cases/', { title: 'New Case' })

    expect(data.value).toEqual({ id: 2, title: 'Created' })
  })

  it('includes auth token in requests', async () => {
    localStorage.setItem('access_token', 'test-token')
    vi.mocked(axios.get).mockResolvedValue({ data: {} })

    const { fetchData } = useApi()
    await fetchData('/api/protected/')

    expect(axios.get).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: 'Bearer test-token'
        })
      })
    )
  })
})
