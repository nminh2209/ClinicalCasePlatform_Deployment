<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <div class="error-illustration">
        <svg width="200" height="200" viewBox="0 0 200 200" fill="none">
          <circle cx="100" cy="100" r="80" fill="#EFF6FF" />
          <path d="M70 90C70 85.5817 73.5817 82 78 82H122C126.418 82 130 85.5817 130 90V130C130 134.418 126.418 138 122 138H78C73.5817 138 70 134.418 70 130V90Z" fill="#3B82F6" />
          <circle cx="88" cy="105" r="6" fill="white" />
          <circle cx="112" cy="105" r="6" fill="white" />
          <path d="M85 120C85 120 92 125 100 125C108 125 115 120 115 120" stroke="white" stroke-width="3" stroke-linecap="round" />
        </svg>
      </div>
      
      <h1 class="error-code">404</h1>
      <h2 class="error-title">Không Tìm Thấy Trang</h2>
      <p class="error-description">
        Trang mà bạn đang tìm kiếm hiện không tồn tại hoặc đã bị chuyển qua địa chỉ khác.
      </p>

      <div class="error-actions">
        <router-link to="/home" class="btn-primary">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          Quay về Bảng điều khiển
        </router-link>
        <button @click="$router.go(-1)" class="btn-secondary">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
          Quay về Trang trước đó
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
  padding: 2rem;
}

.not-found-container {
  text-align: center;
  max-width: 600px;
}

.error-illustration {
  margin-bottom: 2rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.error-code {
  font-size: 6rem;
  font-weight: 800;
  color: #1e40af;
  margin-bottom: 1rem;
  line-height: 1;
  letter-spacing: -0.02em;
}

.error-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.error-description {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.btn-secondary {
  background: white;
  color: #374151;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

@media (max-width: 640px) {
  .error-code {
    font-size: 4rem;
  }

  .error-title {
    font-size: 1.5rem;
  }

  .error-description {
    font-size: 1rem;
  }

  .error-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}
</style>
