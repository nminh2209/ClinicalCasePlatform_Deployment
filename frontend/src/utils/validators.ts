/**
 * Validation utilities
 */

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

export function validatePassword(password: string): boolean {
  // Minimum 8 characters
  return password.length >= 8
}

export function validatePhoneNumber(phone: string): boolean {
  // Vietnamese phone number pattern
  const phoneRegex = /^(0|\+84)[3|5|7|8|9][0-9]{8}$/
  return phoneRegex.test(phone)
}

export function isRequired(value: string): boolean {
  return value.trim().length > 0
}
