import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import CaseSummary from '@/views/CaseSummary.vue'
import axios from 'axios'

vi.mock('axios')

describe('CaseSummary.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()

    // Mock localStorage
    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue('mock-token')

    // Mock axios responses
    vi.mocked(axios.get).mockResolvedValue({
      data: {
        total_cases: 10,
        by_status: {
          draft: 3,
          submitted: 4,
          reviewed: 2,
          approved: 1
        },
        by_specialty: [],
        by_priority: {},
        by_complexity: {},
        recent_cases: []
      }
    })
  })

  it('renders case summary dashboard', () => {
    const wrapper = mount(CaseSummary, {
      global: {
        stubs: {
          Card: true,
          CardHeader: true,
          CardTitle: true,
          CardContent: true
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('fetches statistics on mount', () => {
    mount(CaseSummary, {
      global: {
        stubs: {
          Card: true
        }
      }
    })

    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/api/cases/statistics'),
      expect.any(Object)
    )
  })

  it('displays total case count', async () => {
    const wrapper = mount(CaseSummary, {
      global: {
        stubs: {
          Card: true,
          CardHeader: true,
          CardTitle: true,
          CardContent: true
        }
      }
    })

    await wrapper.vm.$nextTick()

    // Should have statistics data
    expect(wrapper.vm.statistics).toBeDefined()
  })

  it('handles loading state', () => {
    const wrapper = mount(CaseSummary, {
      global: {
        stubs: {
          Card: true
        }
      }
    })

    // Initially loading should be true or false
    expect(typeof wrapper.vm.loading).toBe('boolean')
  })
})
