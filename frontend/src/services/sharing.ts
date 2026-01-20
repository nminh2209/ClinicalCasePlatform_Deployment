import api from "./api";

// Simple caching mechanism for performance
class SimpleCache {
  private cache: Map<string, { data: any; timestamp: number; ttl: number }> = new Map()

  set(key: string, data: any, ttlMinutes: number = 5): void {
    this.cache.set(key, {
      data: JSON.parse(JSON.stringify(data)), // Deep copy
      timestamp: Date.now(),
      ttl: ttlMinutes * 60 * 1000
    })
  }

  get(key: string): any | null {
    const entry = this.cache.get(key)
    if (!entry) return null

    if (Date.now() - entry.timestamp > entry.ttl) {
      this.cache.delete(key)
      return null
    }

    return JSON.parse(JSON.stringify(entry.data)) // Deep copy
  }

  clear(pattern?: string): void {
    if (!pattern) {
      this.cache.clear()
      return
    }

    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key)
      }
    }
  }
}

// Create cache instance
const cache = new SimpleCache()

export interface SharePermission {
  id?: number;
  case: number;
  user?: number;
  share_type: 'individual' | 'department' | 'class_group' | 'public';
  target_department?: number;
  class_group?: string;
  permission_type: 'view' | 'comment' | 'analyze' | 'edit';
  expires_at?: string;
  notes?: string;
}

// Request payload type (without case field since it's in URL)
export interface CreatePermissionRequest {
  user?: number;
  share_type: 'individual' | 'department' | 'class_group' | 'public';
  target_department?: number;
  class_group?: string;
  permission_type: 'view' | 'comment' | 'analyze' | 'edit';
  expires_at?: string;
  notes?: string;
}

// Departments
export interface Department {
  id: number;
  name: string;
  code?: string;
  description?: string;
  is_active?: boolean;
  vietnamese_name?: string; // Optional: present in model, may not be serialized
}

export interface GuestAccess {
  id?: number;
  case: number;
  guest_email: string;
  guest_name?: string;
  permission_type: 'view' | 'comment';
  expiration_hours?: number;
}

export interface CaseGroup {
  id?: number;
  name: string;
  description?: string;
  group_type: 'assignment' | 'project' | 'exam' | 'study_group';
  department?: number;
  class_identifier?: string;
  add_cases_ids?: number[];
  remove_cases_ids?: number[];
}

export const sharingService = {
  // Enhanced Case Permissions
  async getCasePermissions(caseId: number) {
    const response = await api.get(`/cases/${caseId}/permissions/`);
    return response.data;
  },

  async createPermission(caseId: number, permission: CreatePermissionRequest) {
    const response = await api.post(`/cases/${caseId}/permissions/`, permission)

    // Clear related caches
    cache.clear(`permissions_${caseId}`)
    cache.clear('accessible_cases')
    cache.clear('shared_cases')

    return response.data
  },

  async getDepartments(params?: { search?: string; ordering?: string; page?: number; page_size?: number }) {
    const cacheKey = `departments_${JSON.stringify(params || {})}`

    // Check cache first
    const cached = cache.get(cacheKey)
    if (cached) {
      return cached
    }

    const response = await api.get(`/cases/departments/`, { params })
    const data = response.data as any
    // Handle pagination or plain list
    const result = Array.isArray(data) ? data as Department[] : (data.results ?? []) as Department[]

    // Cache for 10 minutes since departments don't change often
    cache.set(cacheKey, result, 10)

    return result
  },

  async updatePermission(caseId: number, permissionId: number, permission: Partial<SharePermission>) {
    const response = await api.put(`/cases/${caseId}/permissions/${permissionId}/`, permission)

    // Clear related caches
    cache.clear(`permissions_${caseId}`)

    return response.data
  },

  async deletePermission(caseId: number, permissionId: number) {
    await api.delete(`/cases/${caseId}/permissions/${permissionId}/`)

    // Clear related caches
    cache.clear(`permissions_${caseId}`)
    cache.clear('accessible_cases')
    cache.clear('shared_cases')
  },

  async bulkGrantPermissions(caseId: number, bulkData: {
    share_type: string;
    users_ids?: number[];
    department_id?: number;
    class_group?: string;
    permission_type: string;
    expires_hours?: number;
    notes?: string;
  }) {
    const response = await api.post(`/cases/${caseId}/permissions/bulk-grant/`, bulkData);
    return response.data;
  },

  async bulkRevokePermissions(caseId: number, permissionIds: number[]) {
    const response = await api.post(`/cases/${caseId}/permissions/bulk-revoke/`, {
      permission_ids: permissionIds
    });
    return response.data;
  },

  async getPermissionAuditLog(caseId: number) {
    const response = await api.get(`/cases/${caseId}/permissions/audit-log/`);
    return response.data;
  },

  // Guest Access Management
  async getGuestAccesses(caseId: number) {
    const response = await api.get(`/cases/${caseId}/guest-access/`);
    return response.data;
  },

  async createGuestAccess(caseId: number, guestData: GuestAccess) {
    const response = await api.post(`/cases/${caseId}/guest-access/`, guestData);
    return response.data;
  },

  async updateGuestAccess(caseId: number, guestId: number, guestData: Partial<GuestAccess>) {
    const response = await api.put(`/cases/${caseId}/guest-access/${guestId}/`, guestData);
    return response.data;
  },

  async deleteGuestAccess(caseId: number, guestId: number) {
    await api.delete(`/cases/${caseId}/guest-access/${guestId}/`);
  },

  async extendGuestAccess(caseId: number, guestId: number, hours: number) {
    const response = await api.post(`/cases/${caseId}/guest-access/${guestId}/extend/`, {
      hours: hours
    });
    return response.data;
  },

  // Case Groups
  async getCaseGroups() {
    const response = await api.get('/case-groups/');
    return response.data;
  },

  async createCaseGroup(groupData: CaseGroup) {
    const response = await api.post('/case-groups/', groupData);
    return response.data;
  },

  async updateCaseGroup(groupId: number, groupData: Partial<CaseGroup>) {
    const response = await api.put(`/case-groups/${groupId}/`, groupData);
    return response.data;
  },

  async deleteCaseGroup(groupId: number) {
    await api.delete(`/case-groups/${groupId}/`);
  },

  async grantGroupPermissions(groupId: number, permissionData: {
    target_users: number[];
    permission_type: string;
    expires_hours?: number;
  }) {
    const response = await api.post(`/case-groups/${groupId}/grant-permissions/`, permissionData);
    return response.data;
  },

  // Utility endpoints
  async getMySharedCases() {
    const response = await api.get('/my-shared-cases/');
    return response.data;
  },

  async getAccessibleCases() {
    const response = await api.get('/accessible-cases/');
    return response.data;
  },

  async cleanupExpiredPermissions() {
    const response = await api.post('/cleanup-expired-permissions/');
    return response.data;
  },

  // Enhanced helper methods
  async getUsersForSharing(params?: { search?: string; department?: number; role?: string; page_size?: number }) {
    const response = await api.get('/auth/users/', {
      params: {
        role: 'instructor', // Default to instructors for sharing
        page_size: 20, // Reasonable default
        ...params
      }
    })

    // Handle paginated response
    const data = response.data
    return Array.isArray(data) ? data : (data.results ?? [])
  },

  // NOTE: Legacy simple getDepartments removed (use the above method with params)
};

export default sharingService;
