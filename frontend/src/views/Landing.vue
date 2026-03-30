<template>
  <div class="landing">
    <!-- Header Navigation -->
    <header class="nav-header">
      <nav class="nav-container">
        <div class="nav-logo">
          <div class="logo-icon">
            <i class="pi pi-heart-fill"></i>
          </div>
          <span class="logo-text">MedCase</span>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <!-- Badge -->
          <div class="badge" data-scroll="fade-up">
            <i class="pi pi-sparkles badge-icon"></i>
            <span class="badge-text">Nền tảng y khoa thế hệ mới</span>
          </div>

          <!-- Title -->
          <h1 class="hero-title" data-scroll="fade-up">
            Quản lý Ca bệnh Lâm sàng
            <span class="title-highlight">Thông minh & Hiệu quả</span>
          </h1>

          <!-- Description -->
          <p class="hero-description" data-scroll="fade-up">
            Nâng tầm đào tạo y khoa với nền tảng toàn diện. Tạo, chia sẻ và hợp
            tác trên các ca bệnh lâm sàng một cách chuyên nghiệp.
          </p>

          <!-- Stats -->
          <div class="stats-container" data-scroll="fade-up">
            <div class="stat-card">
              <div class="stat-number">850+</div>
              <div class="stat-label">Người dùng</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">2.5K+</div>
              <div class="stat-label">Ca bệnh</div>
            </div>
          </div>

          <!-- CTA Button -->
          <div class="cta-container" data-scroll="fade-up">
            <Button
              label="Bắt đầu"
              icon="pi pi-arrow-right"
              iconPos="right"
              class="cta-button"
              @click="goToLogin"
            />
          </div>
        </div>

        <!-- Scroll Indicators -->
        <div class="scroll-indicator" data-scroll="fade">
          <div class="scroll-line"></div>
        </div>
        <ScrollTop />
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="features-container">
        <!-- Section Header -->
        <div class="section-header" data-scroll="fade-up">
          <div class="section-badge">
            <i class="pi pi-star-fill badge-icon"></i>
            <span class="badge-text">Tính năng ưu việt</span>
          </div>
          <h2 class="section-title">
            Công cụ toàn diện cho
            <span class="title-accent">đào tạo y khoa chuyên nghiệp</span>
          </h2>
          <p class="section-subtitle">
            Thiết kế dành riêng cho sinh viên y khoa, bác sĩ và giảng viên
          </p>
        </div>

        <!-- Feature Cards -->
        <div class="features-grid">
          <div class="feature-card" data-scroll="fade-up">
            <div class="feature-icon">
              <i class="pi pi-file-edit"></i>
            </div>
            <h3 class="feature-title">Ghi chép y khoa</h3>
            <p class="feature-description">
              Tạo báo cáo ca bệnh theo chuẩn y khoa với giao diện trực quan
            </p>
          </div>

          <div class="feature-card" data-scroll="fade-up">
            <div class="feature-icon">
              <i class="pi pi-comments"></i>
            </div>
            <h3 class="feature-title">Hợp tác thông minh</h3>
            <p class="feature-description">
              Chia sẻ và nhận phản hồi từ chuyên gia trong cộng đồng y khoa
            </p>
          </div>

          <div class="feature-card" data-scroll="fade-up">
            <div class="feature-icon">
              <i class="pi pi-sliders-h"></i>
            </div>
            <h3 class="feature-title">Quản lý khoa học</h3>
            <p class="feature-description">
              Sắp xếp và tìm kiếm ca bệnh với hệ thống phân loại thông minh
            </p>
          </div>

          <div class="feature-card" data-scroll="fade-up">
            <div class="feature-icon">
              <i class="pi pi-file-export"></i>
            </div>
            <h3 class="feature-title">Xuất báo cáo</h3>
            <p class="feature-description">
              Xuất định dạng PDF, Word cho thuyết trình và đánh giá
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import Button from "primevue/button";
import ScrollTop from "primevue/scrolltop";

const router = useRouter();

const goToLogin = () => {
  router.push("/login");
};

// Scroll animations
let observer: IntersectionObserver | null = null;

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    },
  );

  const scrollElements = document.querySelectorAll("[data-scroll]");
  scrollElements.forEach((el) => observer?.observe(el));

  document.documentElement.style.scrollBehavior = "smooth";
});

onUnmounted(() => {
  observer?.disconnect();
});
</script>

<style scoped>
.landing {
  min-height: 100vh;
  background: var(--background);
  color: var(--foreground);
}

/* Scroll Animations */
[data-scroll] {
  opacity: 0;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-scroll="fade"] {
  transform: translateY(0);
}

[data-scroll="fade-up"] {
  transform: translateY(30px);
}

[data-scroll].visible {
  opacity: 1;
  transform: translateY(0);
}

/* Navigation Header */
.nav-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--card);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 3px 0 var(--shadow-grey);
  margin-bottom: 1rem;
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1.25rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: var(--primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.logo-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px var(--shadow-blue-hover);
}

.logo-icon .pi {
  color: var(--primary-foreground);
  font-size: 1.25rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--foreground);
  letter-spacing: -0.02em;
}

/* Hero Section */
.hero-section {
  min-height: calc(100vh - 90px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--background);
  padding: 3rem 2rem;
  position: relative;
}

.hero-container {
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  text-align: center;
}

.hero-content {
  max-width: 760px;
  margin: 0 auto;
}

/* Badge Styling */
.badge,
.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    rgba(59, 130, 246, 0.1) 100%
  );
  border: 1px solid var(--shadow-blue);
  border-radius: 100px;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.badge:hover,
.section-badge:hover {
  box-shadow: 0 4px 12px var(--shadow-blue-hover);
  transform: translateY(-2px);
}

.badge-icon {
  color: var(--primary);
  font-size: 0.875rem;
}

.badge-text {
  color: var(--primary);
  font-size: 0.875rem;
  font-weight: 600;
}

/* Hero Title */
.hero-title {
  font-size: 3.75rem;
  font-weight: 800;
  line-height: 1.15;
  color: var(--foreground);
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.title-highlight {
  display: block;
  color: var(--primary);
  margin-top: 0.25rem;
}

/* Hero Description */
.hero-description {
  font-size: 1.125rem;
  line-height: 1.75;
  color: var(--muted-foreground);
  margin-bottom: 2.5rem;
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
}

/* Stats Container */
.stats-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 640px;
  margin: 0 auto 2.5rem;
}

.stat-card {
  background: var(--card);
  padding: 1.75rem 1.5rem;
  border-radius: 16px;
  border: 1px solid var(--border);
  box-shadow: 0 2px 4px var(--shadow-grey);
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: var(--shadow-blue);
  box-shadow: 0 4px 12px var(--shadow-blue-hover);
  transform: translateY(-2px);
}

.stat-number {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--primary);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--muted-foreground);
  font-weight: 500;
}

/* CTA Button */
.cta-container {
  margin-bottom: 3rem;
}

.cta-button {
  background: var(--primary) !important;
  border: 1px solid var(--primary) !important;
  color: var(--primary-foreground) !important;
  padding: 1rem 2.5rem !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  border-radius: 100px !important;
  box-shadow: 0 4px 12px var(--shadow-blue) !important;
  transition: all 0.3s ease !important;
  cursor: pointer;
}

.cta-button:hover {
  background: var(--primary-hover) !important;
  border-color: var(--primary-hover) !important;
  box-shadow: 0 6px 16px var(--shadow-blue-hover) !important;
  transform: translateY(-2px) !important;
}

.cta-button:active {
  transform: translateY(0) !important;
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0.5;
  transition: opacity 0.3s ease;
}

.scroll-indicator:hover {
  opacity: 1;
}

.scroll-line {
  width: 2px;
  height: 40px;
  background: linear-gradient(
    to bottom,
    transparent,
    var(--primary),
    transparent
  );
  animation: scrollPulse 2s ease-in-out infinite;
}

@keyframes scrollPulse {
  0%,
  100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(10px);
  }
}

/* Features Section */
.features-section {
  background: var(--card);
  padding: 5rem 2rem;
  border-top: 1px solid var(--border);
}

.features-container {
  max-width: 1280px;
  margin: 0 auto;
}

/* Section Header */
.section-header {
  text-align: center;
  margin-bottom: 3.5rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--foreground);
  margin-bottom: 1rem;
  letter-spacing: -0.01em;
}

.title-accent {
  color: var(--primary);
}

.section-subtitle {
  font-size: 1.125rem;
  color: var(--muted-foreground);
  max-width: 600px;
  margin: 0 auto;
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 1100px;
  margin: 0 auto;
}

.feature-card {
  background: var(--card);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid var(--border);
  box-shadow: 0 2px 4px var(--shadow-grey);
  transition: all 0.3s ease;
}

.feature-card:hover {
  border-color: var(--shadow-blue-hover);
  box-shadow: 0 8px 24px var(--shadow-blue);
  transform: translateY(-4px);
}

.feature-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    var(--shadow-blue-hover) 100%
  );
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  background: linear-gradient(
    135deg,
    var(--primary) 0%,
    var(--shadow-blue) 100%
  );
  transform: scale(1.05);
}

.feature-icon .pi {
  font-size: 1.5rem;
  color: var(--primary);
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon .pi {
  color: var(--primary-foreground);
}

.feature-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--foreground);
  margin-bottom: 0.75rem;
}

.feature-description {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--muted-foreground);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 3rem;
  }

  .section-title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .nav-container {
    padding: 1rem 1.5rem;
  }

  .hero-section {
    padding: 2rem 1.5rem;
    min-height: calc(100vh - 80px);
  }

  .hero-title {
    font-size: 2.25rem;
  }

  .hero-description {
    font-size: 1rem;
  }

  .stats-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .cta-button {
    width: 100%;
    justify-content: center;
  }

  .scroll-indicator {
    display: none;
  }

  .features-section {
    padding: 3rem 1.5rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .feature-card {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.875rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .stat-number {
    font-size: 1.875rem;
  }
}
</style>
