/**
 * Tests for utility functions
 */
import { describe, it, expect } from 'vitest'
import { formatDate, formatTime, formatDateTime } from '@/utils/dateFormatter'
import { validateEmail, validatePassword } from '@/utils/validators'
import { truncateText, capitalize, slugify } from '@/utils/stringHelpers'

describe('Date Formatter Utils', () => {
  it('formats date correctly', () => {
    const date = new Date('2024-03-15T10:30:00')
    const formatted = formatDate(date)
    
    // Should format as DD/MM/YYYY or similar
    expect(formatted).toMatch(/\d{2}\/\d{2}\/\d{4}/)
  })

  it('formats time correctly', () => {
    const date = new Date('2024-03-15T14:30:00')
    const formatted = formatTime(date)
    
    // Should format as HH:MM
    expect(formatted).toMatch(/\d{2}:\d{2}/)
  })

  it('formats datetime correctly', () => {
    const date = new Date('2024-03-15T14:30:00')
    const formatted = formatDateTime(date)
    
    expect(formatted).toBeTruthy()
    expect(typeof formatted).toBe('string')
  })
})

describe('Validator Utils', () => {
  it('validates email correctly', () => {
    expect(validateEmail('test@example.com')).toBe(true)
    expect(validateEmail('invalid-email')).toBe(false)
    expect(validateEmail('missing@')).toBe(false)
    expect(validateEmail('@nodomain.com')).toBe(false)
  })

  it('validates password strength', () => {
    expect(validatePassword('short')).toBe(false)
    expect(validatePassword('longpassword123')).toBe(true)
    expect(validatePassword('12345678')).toBe(true)
  })
})

describe('String Helper Utils', () => {
  it('truncates text correctly', () => {
    const longText = 'This is a very long text that needs truncation'
    const truncated = truncateText(longText, 20)
    
    expect(truncated.length).toBeLessThanOrEqual(23) // 20 + '...'
    expect(truncated).toContain('...')
  })

  it('capitalizes first letter', () => {
    expect(capitalize('hello')).toBe('Hello')
    expect(capitalize('HELLO')).toBe('HELLO')
    expect(capitalize('hello world')).toBe('Hello world')
  })

  it('creates slug from text', () => {
    expect(slugify('Hello World')).toBe('hello-world')
    expect(slugify('Test Case #123')).toBe('test-case-123')
    expect(slugify('Special @#$ Characters')).toBe('special-characters')
  })
})
