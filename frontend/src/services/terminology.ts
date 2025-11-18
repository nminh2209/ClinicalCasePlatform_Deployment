import api from './api'

export interface Term {
  id: number
  term: string
  vietnamese_term?: string
  english_term?: string
  synonyms?: string[]
  definition?: string
  specialty?: string
  is_active?: boolean
}

export interface ICD10 {
  id: number
  code: string
  description_en?: string
  description_vi?: string
  chapter?: string
  category?: string
}

export interface Abbreviation {
  id: number
  abbr: string
  expansion: string
  description?: string
  specialty?: string
}

const terminologyService = {
  async autocompleteTerms(q: string, specialty?: string, limit = 20) {
    const params: any = { q, limit }
    if (specialty) params.specialty = specialty
    const resp = await api.get('/cases/terminology/terms/autocomplete/', { params })
    return resp.data as Term[]
  },

  async searchICD(q: string) {
    const resp = await api.get('/cases/terminology/icd10/', { params: { q } })
    return resp.data as ICD10[]
  },

  async getAbbreviations(q: string) {
    const resp = await api.get('/cases/terminology/abbreviations/', { params: { q } })
    return resp.data as Abbreviation[]
  }
}

export default terminologyService
