<template>
  <div class="feed-post-card">
    <!-- Post Header -->
    <div class="post-header">
      <div class="author-info">
        <div class="avatar">
          <User class="w-8 h-8 text-blue-600" />
        </div>
        <div class="author-details">
          <h4 class="author-name">{{ post.student.full_name }}</h4>
          <p class="meta-info">
            <span class="department">{{ post.student.department_name }}</span>
            <span class="separator">·</span>
            <span class="time">{{ formatDate(post.published_to_feed_at) }}</span>
            <Badge v-if="post.published_by" variant="outline" class="ml-2">
              Được duyệt bởi {{ post.published_by.full_name }}
            </Badge>
          </p>
        </div>
      </div>
      <Badge v-if="post.is_featured" class="featured-badge">
        ⭐ Nổi bật
      </Badge>
    </div>

    <!-- Case Content -->
    <div class="post-content">
      <h3 class="case-title">{{ post.title }}</h3>
      
      <div class="case-meta">
        <Badge>{{ post.specialty }}</Badge>
        <Badge variant="secondary">{{ formatComplexity(post.complexity_level) }}</Badge>
        <Badge variant="outline">
          <GlobeIcon v-if="post.feed_visibility === 'university'" class="w-3 h-3 mr-1" />
          <BuildingIcon v-else class="w-3 h-3 mr-1" />
          {{ post.feed_visibility === 'university' ? 'Toàn trường' : 'Cùng khoa' }}
        </Badge>
      </div>

      <div v-if="post.case_summary" class="case-summary">
        <p :class="{ 'line-clamp-3': !expanded }">
          {{ post.case_summary }}
        </p>
      </div>

      <button 
        v-if="post.case_summary && post.case_summary.length > 200" 
        @click="toggleExpand" 
        class="expand-btn"
      >
        {{ expanded ? 'Thu gọn' : 'Xem thêm' }}
      </button>
    </div>

    <!-- Stats Bar -->
    <div class="post-stats">
      <div class="stat-group">
        <span class="stat" v-if="post.reaction_count > 0">
          <span class="reaction-icons">
            👍❤️💡
          </span>
          <span class="count">{{ post.reaction_count }}</span>
        </span>
      </div>
      <div class="stat-group-right">
        <span class="stat" v-if="post.comments_count > 0">
          {{ post.comments_count }} bình luận
        </span>
        <span class="stat">
          {{ post.view_count }} lượt xem
        </span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="post-actions">
      <button 
        @click="react('like')" 
        :class="['action-btn', { active: userReaction === 'like' }]"
      >
        <span class="icon">👍</span>
        <span>Thích</span>
      </button>
      
      <button 
        @click="react('love')" 
        :class="['action-btn', { active: userReaction === 'love' }]"
      >
        <span class="icon">❤️</span>
        <span>Yêu thích</span>
      </button>
      
      <button 
        @click="react('insightful')" 
        :class="['action-btn', { active: userReaction === 'insightful' }]"
      >
        <span class="icon">💡</span>
        <span>Hữu ích</span>
      </button>
      
      <button 
        @click="react('learned')" 
        :class="['action-btn', { active: userReaction === 'learned' }]"
      >
        <span class="icon">📚</span>
        <span>Học được</span>
      </button>
      
      <button @click="viewFullCase" class="action-btn">
        <span class="icon">💬</span>
        <span>Bình luận</span>
      </button>
      
      <button @click="viewFullCase" class="action-btn">
        <span class="icon">👁️</span>
        <span>Xem đầy đủ</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useToast } from '@/composables/useToast';
import feedService from '@/services/feed';
import Badge from '@/components/ui/Badge.vue';
import User from '@/components/icons/User.vue';
import GlobeIcon from '@/components/icons/GlobeIcon.vue';
import BuildingIcon from '@/components/icons/BuildingIcon.vue';

interface Props {
  post: any;
}

const props = defineProps<Props>();
const emit = defineEmits(['react', 'comment', 'refresh', 'view-details']);

const { toast } = useToast();

const expanded = ref(false);
const userReaction = ref(props.post.user_reaction);

const toggleExpand = () => {
  expanded.value = !expanded.value;
};

const react = async (reactionType: 'like' | 'love' | 'insightful' | 'learned') => {
  try {
    await feedService.toggleReaction(props.post.id, reactionType, userReaction.value);
    
    // Update local state
    if (userReaction.value === reactionType) {
      userReaction.value = null;
      props.post.reaction_count--;
    } else {
      const wasNull = userReaction.value === null;
      userReaction.value = reactionType;
      if (wasNull) {
        props.post.reaction_count++;
      }
    }
    
    emit('react', { caseId: props.post.id, reactionType });
  } catch (error) {
    console.error('Failed to react:', error);
    toast.error('Không thể thực hiện reaction');
  }
};

const viewFullCase = () => {
  emit('view-details', props.post.id);
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(hours / 24);
  
  if (hours < 1) return 'Vừa xong';
  if (hours < 24) return `${hours} giờ trước`;
  if (days < 7) return `${days} ngày trước`;
  
  return date.toLocaleDateString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};

const formatComplexity = (level: string) => {
  const map: Record<string, string> = {
    basic: 'Cơ bản',
    intermediate: 'Trung cấp',
    advanced: 'Nâng cao',
    expert: 'Chuyên gia'
  };
  return map[level] || level;
};
</script>

<style scoped>
.feed-post-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
  overflow: hidden;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.author-info {
  display: flex;
  gap: 12px;
  flex: 1;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-details {
  flex: 1;
}

.author-name {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.meta-info {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.separator {
  margin: 0 4px;
}

.featured-badge {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  font-weight: 600;
}

.post-content {
  padding: 16px 20px;
}

.case-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.case-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.case-summary {
  color: #4b5563;
  line-height: 1.6;
  margin: 12px 0;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.expand-btn {
  color: #3b82f6;
  font-weight: 500;
  font-size: 14px;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.expand-btn:hover {
  text-decoration: underline;
}

.post-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 20px;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
  color: #6b7280;
}

.stat-group,
.stat-group-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.stat {
  display: flex;
  align-items: center;
  gap: 4px;
}

.reaction-icons {
  font-size: 14px;
  line-height: 1;
}

.count {
  font-weight: 500;
}

.post-actions {
  display: flex;
  padding: 4px 8px;
  gap: 4px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 12px;
  background: none;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: background 0.2s;
}

.action-btn:hover {
  background: #f3f4f6;
}

.action-btn.active {
  color: #3b82f6;
  background: #eff6ff;
}

.action-btn .icon {
  font-size: 18px;
  line-height: 1;
}

@media (max-width: 640px) {
  .post-actions {
    flex-wrap: wrap;
  }
  
  .action-btn {
    font-size: 13px;
    padding: 8px 10px;
  }
  
  .action-btn span:not(.icon) {
    display: none;
  }
  
  .action-btn .icon {
    font-size: 20px;
  }
}
</style>
