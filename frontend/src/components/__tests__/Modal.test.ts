/**
 * Tests for Modal component
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Modal from '@/components/Modal.vue'

describe('Modal', () => {
  it('renders modal when show is true', () => {
    const wrapper = mount(Modal, {
      props: { show: true }
    })
    
    expect(wrapper.find('.modal').exists()).toBe(true)
  })

  it('does not render when show is false', () => {
    const wrapper = mount(Modal, {
      props: { show: false }
    })
    
    expect(wrapper.find('.modal').exists()).toBe(false)
  })

  it('displays title', () => {
    const wrapper = mount(Modal, {
      props: { 
        show: true,
        title: 'Test Modal'
      }
    })
    
    expect(wrapper.text()).toContain('Test Modal')
  })

  it('renders slot content', () => {
    const wrapper = mount(Modal, {
      props: { show: true },
      slots: {
        default: '<div class="custom-content">Custom Content</div>'
      }
    })
    
    expect(wrapper.html()).toContain('Custom Content')
  })

  it('emits close event when close button clicked', async () => {
    const wrapper = mount(Modal, {
      props: { show: true }
    })
    
    await wrapper.find('.close-button').trigger('click')
    
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('emits close on backdrop click', async () => {
    const wrapper = mount(Modal, {
      props: { show: true }
    })
    
    await wrapper.find('.modal-backdrop').trigger('click')
    
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('prevents close on content click', async () => {
    const wrapper = mount(Modal, {
      props: { show: true }
    })
    
    await wrapper.find('.modal-content').trigger('click')
    
    expect(wrapper.emitted('close')).toBeFalsy()
  })
})
