<template>
  <div class="public-feed-container">
    <!-- Header -->
    <div class="feed-header">
      <div class="header-content">
        <h1 class="page-title">Bệnh Án Công Khai</h1>
        <p class="page-subtitle">
          Học hỏi từ những ca bệnh hay được giảng viên phê duyệt
        </p>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-tabs">
        <Button
          outlined
          :class="['filter-tab', { active: filterType === 'department' }]"
          @click="filterType = 'department'"
          label="Khoa của tôi"
        />
        <Button
          outlined
          :class="['filter-tab', { active: filterType === 'all' }]"
          @click="filterType = 'all'"
          label="Tất cả"
        />
        <Button
          outlined
          :class="['filter-tab', { active: filterType === 'featured' }]"
          @click="filterType = 'featured'"
          label="Nổi bật"
        />
      </div>

      <div class="filter-controls">
        <Select
          v-model="specialtyFilter"
          :options="specialtyOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Tất cả chuyên khoa"
          class="filter-select"
          :disabled="choicesLoading"
        />
        <Button
          outlined
          size="small"
          class="refresh-btn"
          @click="refreshFeed"
          label="Làm mới"
        />
      </div>
    </div>

    <!-- Feed Stats Banner -->
    <div v-if="statistics" class="feed-stats-banner">
      <div class="stat-item">
        <span class="stat-value">{{ statistics.total_published }}</span>
        <span class="stat-label">Ca bệnh công khai</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ statistics.department_published }}</span>
        <span class="stat-label">Ca bệnh khoa bạn</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ statistics.featured_count }}</span>
        <span class="stat-label">Ca nổi bật</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <ProgressSpinner
        style="width: 2.5rem; height: 2.5rem"
        strokeWidth="4"
        fill="transparent"
        animationDuration=".8s"
        aria-label="Đang tải ca bệnh"
      />
      <p>Đang tải ca bệnh...</p>
    </div>

    <!-- Feed Posts -->
    <div v-else-if="feedPosts.length > 0" class="feed-posts">
      <FeedPostCard
        v-for="post in feedPosts"
        :key="post.id"
        :post="post"
        @view-details="openCaseModal"
        @refresh="loadFeed"
      />

      <div v-if="hasMore" class="load-more">
        <Button
          :label="loadingMore ? 'Đang tải...' : 'Xem thêm ca bệnh'"
          :disabled="loadingMore"
          :loading="loadingMore"
          @click="loadMore"
        />
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <h3>Chưa có ca bệnh nào</h3>
      <p>
        Hiện chưa có ca bệnh nào được xuất bản lên feed công khai.<br />
        Các ca bệnh hay sẽ được giảng viên phê duyệt và chia sẻ ở đây.
      </p>
    </div>

    <!-- Case Detail Modal -->
    <CaseDetailModal
      :case-id="selectedCaseId"
      :is-open="showCaseModal"
      @close="closeCaseModal"
      @refresh="loadFeed"
      @comment-added="handleCommentAdded"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { useToast } from "@/composables/useToast";
import { useChoices } from "@/composables/useChoices";
import feedService, {
  type FeedPost,
  type FeedStatistics,
} from "@/services/feed";
import FeedPostCard from "@/components/FeedPostCard.vue";
import CaseDetailModal from "@/components/CaseDetailModal.vue";
import Button from "primevue/button";
import Select from "primevue/select";
import ProgressSpinner from "primevue/progressspinner";

const { toast } = useToast();
const { specialties, loading: choicesLoading } = useChoices();

const loading = ref(true);
const loadingMore = ref(false);
const feedPosts = ref<FeedPost[]>([]);
const filterType = ref<"all" | "department" | "featured">("department");
const specialtyFilter = ref("");
const currentPage = ref(1);
const hasMore = ref(false);
const statistics = ref<FeedStatistics | null>(null);
const showCaseModal = ref(false);
const selectedCaseId = ref<number | null>(null);

const specialtyOptions = computed(() => {
  const allOption = {
    label: choicesLoading.value ? "Đang tải..." : "Tất cả chuyên khoa",
    value: "",
  };
  const options = specialties.value.map((s) => ({
    label: s.name,
    value: s.name,
  }));
  return [allOption, ...options];
});

const loadFeed = async (append = false) => {
  if (append) {
    loadingMore.value = true;
  } else {
    loading.value = true;
    currentPage.value = 1;
  }
  try {
    const response = await feedService.getFeed({
      filter: filterType.value,
      specialty: specialtyFilter.value || undefined,
      page: currentPage.value,
      page_size: 10,
    });
    if (append) {
      feedPosts.value = [...feedPosts.value, ...response.results];
    } else {
      feedPosts.value = response.results;
    }
    hasMore.value = !!response.next;
  } catch (error) {
    toast.error("Không thể tải feed. Vui lòng thử lại.");
  } finally {
    loading.value = false;
    loadingMore.value = false;
  }
};

const loadStatistics = async () => {
  try {
    statistics.value = await feedService.getStatistics();
  } catch (error) {}
};

const loadMore = () => {
  currentPage.value++;
  loadFeed(true);
};
const refreshFeed = () => {
  loadFeed(false);
  loadStatistics();
};

const handleCommentAdded = (caseId: number) => {
  const post = feedPosts.value.find((p) => p.id === caseId);
  if (post) post.comments_count = (post.comments_count || 0) + 1;
};

const openCaseModal = (caseId: number) => {
  selectedCaseId.value = caseId;
  showCaseModal.value = true;
};
const closeCaseModal = () => {
  showCaseModal.value = false;
  selectedCaseId.value = null;
};

watch([filterType, specialtyFilter], () => loadFeed(false));

onMounted(() => {
  loadFeed(false);
  loadStatistics();
});
</script>

<style scoped>
.public-feed-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.feed-header {
  margin-bottom: 24px;
}

.header-content {
  text-align: center;
}

.page-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 700;
  color: var(--foreground);
  margin: 0 0 8px;
}

.page-subtitle {
  font-size: 15px;
  color: var(--muted-foreground);
  margin: 0;
}

/* Filter bar */
.filter-bar {
  background: var(--card);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 20px;
  border: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Filter tab — overrides globals.css .p-button defaults via :deep.
   Active state inverts the colour scheme (dark bg + light text). */
:deep(.filter-tab.p-button) {
  min-height: 2.5rem;
  padding: 0.5rem 0.9rem;
  background: var(--secondary) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--muted-foreground) !important;
  box-shadow: none;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease,
    transform 0.08s ease;
}

:deep(.filter-tab.p-button:hover) {
  background: var(--accent) !important;
  border-color: var(--foreground) !important;
  color: var(--foreground) !important;
}

:deep(.filter-tab.p-button.active),
:deep(.filter-tab.p-button.active:hover) {
  background: var(--foreground) !important;
  border-color: var(--foreground) !important;
  color: var(--background) !important;
}

:deep(.filter-tab.p-button.active .p-button-label),
:deep(.filter-tab.p-button.active span) {
  color: var(--background) !important;
}

:deep(.filter-tab.p-button:active) {
  transform: translateY(1px);
}

.filter-controls {
  display: flex;
  gap: 0.625rem;
  align-items: center;
  margin-left: auto;
}

/* Specialty select — width override; colour/border governed by globals.css */
:deep(.filter-select.p-select) {
  min-width: 220px;
  min-height: 2.5rem;
  border-radius: 8px;
  font-size: 14px;
}

.refresh-btn {
  min-height: 2.5rem;
  white-space: nowrap;
}

/* Stats banner */
.feed-stats-banner {
  display: flex;
  justify-content: space-around;
  background: var(--primary);
  color: var(--primary-foreground);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px var(--shadow-blue);
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  opacity: 0.9;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.feed-posts {
  margin-bottom: 24px;
}

.load-more {
  text-align: center;
  padding: 24px 0;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: var(--card);
  border-radius: 16px;
  border: 1px solid var(--border);
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--foreground);
  margin: 0 0 8px;
}

.empty-state p {
  font-size: 15px;
  color: var(--muted-foreground);
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 640px) {
  .public-feed-container {
    padding: 12px;
  }
  .page-title {
    font-size: 24px;
  }
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
    padding: 0.9rem;
  }
  .filter-tabs {
    justify-content: flex-start;
  }
  .filter-controls {
    flex-direction: row;
    width: 100%;
    margin-left: 0;
  }
  :deep(.filter-select.p-select) {
    min-width: 0;
    width: 100%;
    flex: 1;
  }
  .feed-stats-banner {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
