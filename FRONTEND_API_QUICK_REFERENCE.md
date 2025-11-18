# Frontend API Quick Reference Guide

## 🚨 Most Commonly Misused Endpoints

### 1. Authentication Flow
**❌ Wrong:**
```javascript
// Don't store tokens in localStorage without httpOnly cookies
localStorage.setItem('token', response.data.token)

// Don't send tokens in request body
axios.post('/api/auth/login/', { token: storedToken })
```

**✅ Correct:**
```javascript
// Store tokens securely
const tokens = response.data.tokens;
localStorage.setItem('access_token', tokens.access);
localStorage.setItem('refresh_token', tokens.refresh);

// Include in headers
const config = {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
};
axios.get('/api/cases/', config);
```

### 2. Case Listing and Filtering
**❌ Wrong:**
```javascript
// Don't fetch all cases at once
axios.get('/api/cases/')

// Don't filter on frontend
const allCases = await axios.get('/api/cases/');
const myCases = allCases.data.filter(case => case.student.id === userId);
```

**✅ Correct:**
```javascript
// Use proper filtering and pagination
const params = {
  page: 1,
  page_size: 20,
  ordering: '-created_at',
  search: 'diabetes',  // Search in title, diagnosis, etc.
  case_status: 'approved',
  department: departmentId
};

const response = await axios.get('/api/cases/', { params });
```

### 3. Export Endpoints
**❌ Wrong:**
```javascript
// Don't use deprecated endpoints
axios.get(`/api/exports/cases/${caseId}/pdf/`)

// Don't call export without handling the blob response
axios.get(`/api/exports/quick/cases/${caseId}/pdf/`)
  .then(response => console.log(response.data)); // Won't work for files
```

**✅ Correct:**
```javascript
// Use quick export endpoints with proper blob handling
const exportCase = async (caseId, format) => {
  try {
    const response = await axios.get(
      `/api/exports/quick/cases/${caseId}/${format}/`,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        responseType: 'blob'  // Important for file downloads
      }
    );

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `case.${format}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error('Export failed:', error);
  }
};
```

### 4. Permission Management
**❌ Wrong:**
```javascript
// Don't share cases one by one
for (const userId of userIds) {
  await axios.post(`/api/cases/${caseId}/permissions/`, {
    user: userId,
    share_type: 'individual'
  });
}
```

**✅ Correct:**
```javascript
// Use bulk operations
await axios.post(`/api/cases/${caseId}/permissions/bulk-grant/`, {
  users: userIds,
  share_type: 'individual',
  can_view: true,
  can_edit: false,
  can_export: true,
  expires_at: '2024-12-31T23:59:59Z'  // Optional
});
```

### 5. File Uploads
**❌ Wrong:**
```javascript
// Don't send files as JSON
axios.post(`/api/cases/${caseId}/attachments/`, {
  file: fileObject,
  description: 'Medical report'
});
```

**✅ Correct:**
```javascript
// Use FormData for file uploads
const formData = new FormData();
formData.append('file', fileObject);
formData.append('attachment_type', 'document');
formData.append('description', 'Medical report');

await axios.post(`/api/cases/${caseId}/attachments/`, formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

## 🔄 Common Data Flow Patterns

### User Authentication Flow
```javascript
// 1. Login
const login = async (email, password) => {
  const response = await axios.post('/api/auth/login/', {
    email,
    password
  });

  const { tokens, user } = response.data;
  localStorage.setItem('access_token', tokens.access);
  localStorage.setItem('refresh_token', tokens.refresh);
  localStorage.setItem('user', JSON.stringify(user));

  return user;
};

// 2. Refresh token when needed
const refreshToken = async () => {
  const refresh = localStorage.getItem('refresh_token');
  const response = await axios.post('/api/auth/token/refresh/', {
    refresh
  });

  localStorage.setItem('access_token', response.data.access);
  return response.data.access;
};

// 3. Logout
const logout = async () => {
  const refresh = localStorage.getItem('refresh_token');
  await axios.post('/api/auth/logout/', { refresh_token: refresh });

  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
};
```

### Case Management Flow
```javascript
// 1. List cases with filtering
const getCases = async (filters = {}) => {
  const params = {
    page: 1,
    page_size: 20,
    ordering: '-updated_at',
    ...filters
  };

  const response = await axios.get('/api/cases/', {
    params,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });

  return response.data; // { count, next, previous, results }
};

// 2. Create case
const createCase = async (caseData) => {
  const response = await axios.post('/api/cases/', caseData, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });

  return response.data;
};

// 3. Update case
const updateCase = async (caseId, updates) => {
  const response = await axios.patch(`/api/cases/${caseId}/`, updates, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });

  return response.data;
};
```

### Permission Management Flow
```javascript
// 1. Share case with users
const shareCase = async (caseId, userIds, permissions) => {
  await axios.post(`/api/cases/${caseId}/permissions/bulk-grant/`, {
    users: userIds,
    share_type: 'individual',
    ...permissions
  }, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });
};

// 2. Get case permissions
const getCasePermissions = async (caseId) => {
  const response = await axios.get(`/api/cases/${caseId}/permissions/`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });

  return response.data;
};
```

## 🛠️ Utility Functions

### Axios Interceptor for Token Refresh
```javascript
// Add to your main.js or app initialization
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try refresh
      try {
        const refresh = localStorage.getItem('refresh_token');
        const response = await axios.post('/api/auth/token/refresh/', {
          refresh
        });

        localStorage.setItem('access_token', response.data.access);

        // Retry original request
        error.config.headers.Authorization = `Bearer ${response.data.access}`;
        return axios(error.config);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

### API Service Class
```javascript
class ApiService {
  constructor() {
    this.baseURL = '/api';
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 10000,
    });

    this.setupInterceptors();
  }

  setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Response interceptor for token refresh
    this.client.interceptors.response.use(
      (response) => response,
      this.handleError.bind(this)
    );
  }

  async handleError(error) {
    if (error.response?.status === 401) {
      try {
        await this.refreshToken();
        // Retry original request
        const config = error.config;
        config.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
        return this.client(config);
      } catch (refreshError) {
        this.logout();
        throw refreshError;
      }
    }
    throw error;
  }

  async refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    const response = await axios.post('/api/auth/token/refresh/', { refresh });
    localStorage.setItem('access_token', response.data.access);
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  // Auth methods
  async login(credentials) {
    const response = await this.client.post('/auth/login/', credentials);
    const { tokens, user } = response.data;
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    localStorage.setItem('user', JSON.stringify(user));
    return user;
  }

  // Cases methods
  async getCases(params = {}) {
    const response = await this.client.get('/cases/', { params });
    return response.data;
  }

  async createCase(caseData) {
    const response = await this.client.post('/cases/', caseData);
    return response.data;
  }

  async exportCase(caseId, format) {
    const response = await this.client.get(`/exports/quick/cases/${caseId}/${format}/`, {
      responseType: 'blob'
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `case-${caseId}.${format}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  }
}

// Usage
const api = new ApiService();
export default api;
```

## 📋 Checklist for API Calls

- [ ] **Authentication**: Include `Authorization: Bearer <token>` header
- [ ] **Content-Type**: Use `application/json` for JSON, `multipart/form-data` for files
- [ ] **Response Type**: Set `responseType: 'blob'` for file downloads
- [ ] **Error Handling**: Check for 401 (token expired) and handle token refresh
- [ ] **Pagination**: Handle paginated responses (`count`, `next`, `previous`, `results`)
- [ ] **Filtering**: Use query parameters instead of filtering on frontend
- [ ] **File Uploads**: Use `FormData` for multipart requests
- [ ] **Bulk Operations**: Use bulk endpoints for multiple items
- [ ] **Rate Limits**: Implement retry logic with exponential backoff

## 🚨 Common Mistakes to Avoid

1. **Storing sensitive data in localStorage** - Use httpOnly cookies for refresh tokens
2. **Not handling token expiration** - Implement automatic token refresh
3. **Fetching all data at once** - Use pagination and filtering
4. **Not using proper Content-Type headers** - Especially for file uploads
5. **Ignoring error responses** - Always handle 4xx and 5xx responses
6. **Making sequential API calls** - Use `Promise.all()` for parallel requests
7. **Not validating response data** - Check response structure before using
8. **Hardcoding API URLs** - Use environment variables or config
9. **Not implementing loading states** - Show loading indicators for better UX
10. **Not handling network errors** - Implement offline/error states

## 🔗 Useful Links

- **Full API Documentation**: `/api/docs/` (Swagger UI)
- **Alternative Docs**: `/api/redoc/` (ReDoc)
- **OpenAPI Schema**: `/api/schema/` (JSON/YAML)

Remember: When in doubt, check the API documentation at `/api/docs/` or refer to the comprehensive `API_DOCUMENTATION.md` file in the project root.