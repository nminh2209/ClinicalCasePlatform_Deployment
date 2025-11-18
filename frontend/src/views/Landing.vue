<!-- Landing Page for Unauthenticated Users -->

<template>
  <div class="landing">
    <header class="hero">
      <nav class="absolute top-4 right-4">
        <router-link to="/login" class="btn btn-primary btn-large mx-5">
          Log in
        </router-link>
        <router-link to="/login" class="btn btn-primary-outline btn-large">
          Sign Up
        </router-link>
      </nav>

      <div class="hero-content">
        <h1>Clinical Case Management Platform</h1>
        <p>Streamline medical case documentation and collaboration for healthcare education</p>
        <div class="hero-actions">
          <router-link to="/login" class="btn btn-primary btn-large">
            Get Started
          </router-link>
          <button class="btn btn-outline btn-large">
            Learn More
          </button>
        </div>
      </div>
      <div class="hero-image">
        <div class="medical-illustration">
          <svg width="400" height="300" viewBox="0 0 400 300" fill="none">
            <rect x="50" y="50" width="300" height="200" rx="12" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2" />
            <rect x="70" y="80" width="60" height="40" rx="4" fill="#3b82f6" />
            <rect x="150" y="80" width="180" height="8" rx="4" fill="#e2e8f0" />
            <rect x="150" y="100" width="120" height="8" rx="4" fill="#e2e8f0" />
            <rect x="70" y="140" width="260" height="8" rx="4" fill="#e2e8f0" />
            <rect x="70" y="160" width="200" height="8" rx="4" fill="#e2e8f0" />
            <rect x="70" y="200" width="140" height="20" rx="4" fill="#10b981" />
          </svg>
        </div>
      </div>
    </header>

    <section class="features">
      <div class="container">
        <h2>Key Features</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14,2 14,8 20,8" />
              </svg>
            </div>
            <h3>Case Documentation</h3>
            <p>Create and manage detailed medical case reports with standardized templates</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            </div>
            <h3>Collaboration</h3>
            <p>Share cases with colleagues and instructors for feedback and learning</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7" />
                <rect x="14" y="3" width="7" height="7" />
                <rect x="14" y="14" width="7" height="7" />
                <rect x="3" y="14" width="7" height="7" />
              </svg>
            </div>
            <h3>Organization</h3>
            <p>Organize cases in repositories with powerful search and filtering</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14,2 14,8 20,8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
              </svg>
            </div>
            <h3>Export & Reports</h3>
            <p>Export cases to PDF, Word, and PowerPoint for presentations</p>
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
}

.hero {
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  padding: 4rem 2rem;
  display: flex;
  align-items: center;
  min-height: 80vh;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.1;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.medical-illustration {
  opacity: 0.8;
}

.features {
  padding: 5rem 0;
  background: #f8fafc;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.features h2 {
  text-align: center;
  margin-bottom: 4rem;
  font-size: 3rem;
  font-weight: 700;
  color: #1f2937;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid #e5e7eb;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1.5rem;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1f2937;
}

.feature-card p {
  color: #6b7280;
  line-height: 1.6;
}

/* Button Styles */
.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary-outline {

  border: 2px solid #1d4ed8;
  color: white;
}

.btn-primary-outline:hover {
  background: #1a4df3;
  transform: translateY(-2px);
}



.btn-primary:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
}

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Responsive Design */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .main-grid {
    grid-template-columns: 1fr;
  }

  .hero {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }

  .hero h1 {
    font-size: 2.5rem;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .hero-image {
    order: -1;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
