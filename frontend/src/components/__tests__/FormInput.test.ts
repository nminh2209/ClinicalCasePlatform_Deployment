/**
 * Tests for FormInput component
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FormInput from '@/components/FormInput.vue'

describe('FormInput', () => {
  it('renders input with label', () => {
    const wrapper = mount(FormInput, {
      props: { 
        label: 'Email',
        modelValue: ''
      }
    })
    
    expect(wrapper.text()).toContain('Email')
    expect(wrapper.find('input').exists()).toBe(true)
  })

  it('updates value on input', async () => {
    const wrapper = mount(FormInput, {
      props: { modelValue: '' }
    })
    
    await wrapper.find('input').setValue('test@example.com')
    
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['test@example.com'])
  })

  it('displays error message', () => {
    const wrapper = mount(FormInput, {
      props: { 
        modelValue: '',
        error: 'This field is required'
      }
    })
    
    expect(wrapper.text()).toContain('This field is required')
  })

  it('applies error class when error exists', () => {
    const wrapper = mount(FormInput, {
      props: { 
        modelValue: '',
        error: 'Error'
      }
    })
    
    expect(wrapper.find('input').classes()).toContain('input-error')
  })

  it('sets input type correctly', () => {
    const wrapper = mount(FormInput, {
      props: { 
        modelValue: '',
        type: 'password'
      }
    })
    
    expect(wrapper.find('input').attributes('type')).toBe('password')
  })

  it('disables input when disabled prop is true', () => {
    const wrapper = mount(FormInput, {
      props: { 
        modelValue: '',
        disabled: true
      }
    })
    
    expect(wrapper.find('input').attributes('disabled')).toBeDefined()
  })

  it('displays placeholder', () => {
    const wrapper = mount(FormInput, {
      props: { 
        modelValue: '',
        placeholder: 'Enter email'
      }
    })
    
    expect(wrapper.find('input').attributes('placeholder')).toBe('Enter email')
  })
})
