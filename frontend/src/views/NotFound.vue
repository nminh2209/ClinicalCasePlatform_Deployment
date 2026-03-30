<template>
  <div class="not-found-page">
    <Card class="not-found-container">
      <template #content>
        <div class="not-found-content">
          <h1 class="error-code">404</h1>
          <h2 class="error-title">Không Tìm Thấy Trang</h2>
          <p class="error-description">
            Trang mà bạn đang tìm kiếm hiện không tồn tại hoặc đã bị chuyển qua
            địa chỉ khác.
          </p>

          <div class="error-actions">
            <Button
              icon="pi pi-home"
              label="Quay về Bảng điều khiển"
              @click="goHome"
            />
            <Button
              icon="pi pi-arrow-left"
              label="Quay về Trang trước đó"
              severity="secondary"
              outlined
              @click="goBack"
            />
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Button from "primevue/button";
import Card from "primevue/card";
import { useRouter } from "vue-router";

const router = useRouter();

const goHome = () => {
  router.push("/home");
};

const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--background);
  padding: 2.5rem 2rem;
}

/*
  Card border-radius fix:
  - Set a single clean radius (20px) on the outer .p-card element
  - Reset all child elements (body, content) to 0 or inherit so no
    double-stacked radius appears at the inner boundary
  - The overflow:hidden on .p-card clips children cleanly
*/
:deep(.p-card) {
  border-radius: 20px !important;
  overflow: hidden;
  border: 1px solid var(--border) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
  background: var(--card) !important;
}

:deep(.p-card-body) {
  border-radius: 0 !important;
  padding: 3rem 2.5rem !important;
}

:deep(.p-card-content) {
  border-radius: 0 !important;
  padding: 0 !important;
}

.not-found-container {
  max-width: 600px;
  width: 100%;
}

.not-found-content {
  text-align: center;
}

.error-code {
  font-size: 6rem;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 1rem;
  line-height: 1;
  letter-spacing: -0.02em;
}

.error-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--foreground);
  margin-bottom: 1rem;
}

.error-description {
  font-size: 1.125rem;
  color: var(--muted-foreground);
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
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

  .error-actions :deep(.p-button) {
    width: 100%;
    justify-content: center;
  }
}
</style>
