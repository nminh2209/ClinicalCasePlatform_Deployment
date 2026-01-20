<template>
  <div class="public-feed-container">
    <!-- Header -->
    <div class="feed-header">
      <div class="header-content">
        <h1 class="page-title">
          <GlobeIcon class="w-7 h-7" />
          Bệnh Án Công Khai
        </h1>
        <p class="page-subtitle">
          Học hỏi từ những ca bệnh hay được giảng viên phê duyệt
        </p>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-tabs">
        <button @click="filterType = 'department'" :class="['filter-tab', { active: filterType === 'department' }]">
          <BuildingIcon class="w-4 h-4" />
          Khoa của tôi
        </button>
        <button @click="filterType = 'all'" :class="['filter-tab', { active: filterType === 'all' }]">
          <GlobeIcon class="w-4 h-4" />
          Tất cả
        </button>
        <button @click="filterType = 'featured'" :class="['filter-tab', { active: filterType === 'featured' }]">
          ⭐ Nổi bật
        </button>
      </div>

      <div class="filter-controls">
        <select v-model="specialtyFilter" class="filter-select" :disabled="choicesLoading">
          <option value="">{{ choicesLoading ? 'Đang tải...' : 'Tất cả chuyên khoa' }}</option>
          <option v-for="s in specialties" :key="s.id" :value="s.name">
            {{ s.name }}
          </option>
        </select>

        <Button @click="refreshFeed" variant="outline" size="sm">
          🔄 Làm mới
        </Button>
      </div>
    </div>

    <!-- Feed Stats (Optional) -->
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
      <div class="spinner"></div>
      <p>Đang tải ca bệnh...</p>
    </div>

    <!-- Feed Posts -->
    <div v-else-if="feedPosts.length > 0" class="feed-posts">
      <FeedPostCard v-for="post in feedPosts" :key="post.id" :post="post" @react="handleReaction"
        @comment="handleComment" @view-details="openCaseModal" @refresh="loadFeed" />

      <!-- Load More -->
      <div v-if="hasMore" class="load-more">
        <Button @click="loadMore" :disabled="loadingMore">
          {{ loadingMore ? 'Đang tải...' : 'Xem thêm ca bệnh' }}
        </Button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <GlobeIcon class="w-16 h-16 text-gray-300" />
      </div>
      <h3>Chưa có ca bệnh nào</h3>
      <p>
        Hiện chưa có ca bệnh nào được xuất bản lên feed công khai.
        <br />
        Các ca bệnh hay sẽ được giảng viên phê duyệt và chia sẻ ở đây.
      </p>
    </div>

    <!-- Case Detail Modal -->
    <CaseDetailModal :case-id="selectedCaseId" :is-open="showCaseModal" @close="closeCaseModal" @refresh="loadFeed" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useToast } from '@/composables/useToast';
import { useChoices } from '@/composables/useChoices';
import feedService, { type FeedPost, type FeedStatistics } from '@/services/feed';
import FeedPostCard from '@/components/FeedPostCard.vue';
import CaseDetailModal from '@/components/CaseDetailModal.vue';
import Button from '@/components/ui/Button.vue';
import GlobeIcon from '@/components/icons/GlobeIcon.vue';
import BuildingIcon from '@/components/icons/BuildingIcon.vue';

const { toast } = useToast();
const { specialties, loading: choicesLoading } = useChoices();

const loading = ref(true);
const loadingMore = ref(false);
const feedPosts = ref<FeedPost[]>([]);
const filterType = ref<'all' | 'department' | 'featured'>('department');
const specialtyFilter = ref('');
const currentPage = ref(1);
const hasMore = ref(false);
const statistics = ref<FeedStatistics | null>(null);
const showCaseModal = ref(false);
const selectedCaseId = ref<number | null>(null);

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
    console.error('Failed to load feed:', error);
    toast.error('Không thể tải feed. Vui lòng thử lại.');
  } finally {
    loading.value = false;
    loadingMore.value = false;
  }
};

const loadStatistics = async () => {
  try {
    statistics.value = await feedService.getStatistics();
  } catch (error) {
    console.error('Failed to load statistics:', error);
  }
};

const loadMore = () => {
  currentPage.value++;
  loadFeed(true);
};

const refreshFeed = () => {
  loadFeed(false);
  loadStatistics();
};

const handleReaction = (data: { caseId: number; reactionType: string }) => {
  // Reaction already handled in FeedPostCard
  console.log('Reaction:', data);
};

const handleComment = (caseId: number) => {
  console.log('Comment on case:', caseId);
};

const openCaseModal = (caseId: number) => {
  selectedCaseId.value = caseId;
  showCaseModal.value = true;
};

const closeCaseModal = () => {
  showCaseModal.value = false;
  selectedCaseId.value = null;
};

// Watch filters
watch([filterType, specialtyFilter], () => {
  loadFeed(false);
});

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
  color: #111827;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 15px;
  color: #6b7280;
  margin: 0;
}

.filter-bar {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.filter-tab.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  color: #374151;
  cursor: pointer;
}

.feed-stats-banner {
  display: flex;
  justify-content: space-around;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
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

.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.feed-posts {
  margin-bottom: 24px;
}

.load-more {
  text-align: center;
  padding: 24px 0;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
}

.empty-icon {
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 15px;
  color: #6b7280;
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
  }

  .filter-tabs {
    justify-content: center;
  }

  .filter-controls {
    flex-direction: column;
    width: 100%;
  }

  .filter-select {
    width: 100%;
  }

  .feed-stats-banner {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
