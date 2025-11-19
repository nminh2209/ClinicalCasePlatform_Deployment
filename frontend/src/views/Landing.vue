<!-- Landing Page for Unauthenticated Users -->

<template>
  <div class="landing">
    <header class="hero">
      <nav class="nav-bar">
        <div class="nav-logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="logo-icon">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
          <span class="logo-text">MedCase</span>
        </div>
        <router-link to="/login" class="btn btn-login">
          Đăng Nhập
        </router-link>
      </nav>

      <div class="hero-container">
        <div class="hero-content">
          <div class="hero-badge">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
            <span>Được các tổ chức y dược hàng đầu tin tưởng</span>
          </div>
          <h1 class="hero-title">Nền tảng Quản lý Ca bệnh Lâm sàng</h1>
          <p class="hero-description">Đơn giản hóa việc ghi chép hồ sơ ca bệnh và hợp tác trong đào tạo y khoa với nền tảng toàn diện của chúng tôi!</p>
          <div class="hero-actions">
            <router-link to="/login" class="btn btn-primary-large">
              <span>Bắt đầu</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
              </svg>
            </router-link>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14,2 14,8 20,8" />
              </svg>
            </div>
            <div class="card-content">
              <div class="card-title">Số ca bệnh được báo cáo</div>
              <div class="card-stat">1,284</div>
            </div>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon success">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
              </svg>
            </div>
            <div class="card-content">
              <div class="card-title">Số người dùng đang hoạt động</div>
              <div class="card-stat">856</div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <section class="features">
      <div class="container">
        <div class="features-header">
          <span class="section-label">Tính năng nổi bật</span>
          <h2 class="section-title">Mọi thứ mà bạn cần để quản lý các ca bệnh lâm sàng, trên một nền tảng duy nhất.</h2>
          <p class="section-description">Những công cụ mạnh mẽ được thiết kế cho giáo dục và hợp tác trong lĩnh vực chăm sóc sức khỏe.</p>
        </div>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14,2 14,8 20,8" />
                </svg>
              </div>
            </div>
            <h3>Ghi chép</h3>
            <p>Tạo và quản lý các báo cáo ca bệnh chi tiết với các mẫu tiêu chuẩn hóa.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
              </div>
            </div>
            <h3>Hợp tác</h3>
            <p>Chia sẻ các ca bệnh với đồng nghiệp, bạn học, và giảng viên để nhận phản hồi và học hỏi.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="7" height="7" />
                  <rect x="14" y="3" width="7" height="7" />
                  <rect x="14" y="14" width="7" height="7" />
                  <rect x="3" y="14" width="7" height="7" />
                </svg>
              </div>
            </div>
            <h3>Sắp xếp</h3>
            <p>Tổ chức các ca bệnh trong các kho lưu trữ với khả năng tìm kiếm và lọc mạnh mẽ</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14,2 14,8 20,8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                </svg>
              </div>
            </div>
            <h3>Xuất Báo Cáo</h3>
            <p>Xuất các ca bệnh sang PDF và Word để phục vụ thuyết trình.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>


<style scoped>
/* Dashboard Styles */
.welcome-header {
  margin-bottom: 2rem;
}

.welcome-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  color: #6b7280;
  font-size: 1rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-primary .stat-icon {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
}

.stat-success .stat-icon {
  background: linear-gradient(135deg, #10b981, #059669);
}

.stat-warning .stat-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.stat-info .stat-icon {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.stat-content {
  flex: 1;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.stat-change {
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.stat-change.positive {
  color: #059669;
  background: #d1fae5;
}

.stat-change.negative {
  color: #dc2626;
  background: #fee2e2;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

/* Main Content Grid */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-all-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
}

.view-all-link:hover {
  color: #1d4ed8;
}

.card-content {
  padding: 1.5rem;
}

/* Review List */
.review-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.review-item:hover {
  background: #f9fafb;
}

.review-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.875rem;
  min-width: 80px;
}

.review-details {
  flex: 1;
}

.review-patient {
  font-weight: 600;
  color: #1f2937;
}

.review-type {
  font-size: 0.875rem;
  color: #6b7280;
}

.review-status {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.review-status.confirmed {
  background: #d1fae5;
  color: #059669;
}

.review-status.waiting {
  background: #fef3c7;
  color: #d97706;
}

/* Case List */
.case-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.case-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.case-item:hover {
  background: #f9fafb;
  border-color: #3b82f6;
  transform: translateX(4px);
}

.case-info {
  flex: 1;
}

.case-patient {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.case-id {
  font-size: 0.875rem;
  color: #6b7280;
}

.case-time {
  font-size: 0.875rem;
  color: #9ca3af;
}

.case-age {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

/* Landing Page Styles */
.landing {
  min-height: 100vh;
  background: #ffffff;
}

.hero {
  position: relative;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  padding: 0;
  min-height: 100vh;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(30, 64, 175, 0.3) 0%, transparent 50%);
  pointer-events: none;
}

.nav-bar {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 4rem;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  color: white;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.btn-login {
  padding: 0.625rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
  backdrop-filter: blur(10px);
}

.btn-login:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.hero-container {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 6rem 4rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  min-height: calc(100vh - 80px);
}

.hero-content {
  max-width: 600px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  font-size: 0.875rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
}

.hero-badge svg {
  width: 16px;
  height: 16px;
}

.hero-title {
  font-size: 3.75rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.hero-description {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn-primary-large {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: white;
  color: #1e40af;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.125rem;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}

.btn-primary-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.hero-visual {
  position: relative;
  height: 500px;
}

.floating-card {
  position: absolute;
  background: white;
  border-radius: 20px;
  padding: 1.75rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  animation: float 6s ease-in-out infinite;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.card-1 {
  top: 8%;
  right: 15%;
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: 5%;
  animation-delay: 2s;
  transform: translateY(-50%);
}

.card-3 {
  bottom: 12%;
  right: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

.card-2 {
  animation-name: float-center;
}

@keyframes float-center {
  0%, 100% {
    transform: translateY(-50%);
  }
  50% {
    transform: translateY(calc(-50% - 15px));
  }
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-icon.success {
  background: linear-gradient(135deg, #10b981, #059669);
}

.card-icon.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.card-title {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.card-stat {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.features {
  padding: 6rem 0;
  background: #f8fafc;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.features-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-label {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.section-description {
  font-size: 1.125rem;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: #3b82f6;
}

.feature-icon-wrapper {
  margin-bottom: 1.5rem;
}

.feature-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1e40af;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #1f2937;
}

.feature-card p {
  color: #6b7280;
  line-height: 1.6;
  font-size: 0.9375rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    padding: 4rem 2rem;
  }

  .hero-visual {
    display: none;
  }

  .hero-title {
    font-size: 3rem;
  }

  .nav-bar {
    padding: 1.5rem 2rem;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .main-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-description {
    font-size: 1.125rem;
  }

  .hero-actions {
    flex-direction: column;
    width: 100%;
  }

  .btn-primary-large {
    width: 100%;
    justify-content: center;
  }

  .feature-grid {
    grid-template-columns: 1fr;
    max-width: 100%;
  }

  .section-title {
    font-size: 2rem;
  }

  .nav-bar {
    padding: 1rem 1.5rem;
  }

  .logo-text {
    font-size: 1.25rem;
  }
}
</style>
