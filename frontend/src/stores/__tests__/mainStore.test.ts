/**
 * Tests for main Pinia store
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useMainStore } from '@/stores/mainStore'

describe('Main Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with default state', () => {
    const store = useMainStore()
    
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(store.notifications).toEqual([])
  })

  it('sets user on login', () => {
    const store = useMainStore()
    const testUser = { id: 1, email: 'test@test.com', role: 'student' }
    
    store.setUser(testUser)
    
    expect(store.user).toEqual(testUser)
    expect(store.isAuthenticated).toBe(true)
  })

  it('clears user on logout', () => {
    const store = useMainStore()
    store.setUser({ id: 1, email: 'test@test.com' })
    
    store.clearUser()
    
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('adds notification', () => {
    const store = useMainStore()
    const notification = {
      id: 1,
      title: 'Test Notification',
      message: 'Test message',
      type: 'info'
    }
    
    store.addNotification(notification)
    
    expect(store.notifications).toHaveLength(1)
    expect(store.notifications[0]).toEqual(notification)
  })

  it('removes notification', () => {
    const store = useMainStore()
    store.addNotification({ id: 1, title: 'Test' })
    store.addNotification({ id: 2, title: 'Test 2' })
    
    store.removeNotification(1)
    
    expect(store.notifications).toHaveLength(1)
    expect(store.notifications[0].id).toBe(2)
  })

  it('marks notification as read', () => {
    const store = useMainStore()
    store.addNotification({ id: 1, title: 'Test', is_read: false })
    
    store.markAsRead(1)
    
    expect(store.notifications[0].is_read).toBe(true)
  })

  it('counts unread notifications', () => {
    const store = useMainStore()
    store.addNotification({ id: 1, is_read: false })
    store.addNotification({ id: 2, is_read: false })
    store.addNotification({ id: 3, is_read: true })
    
    expect(store.unreadCount).toBe(2)
  })
})
