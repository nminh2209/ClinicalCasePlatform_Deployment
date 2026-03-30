<template>
  <div class="bg-white rounded-xl shadow-sm mb-4 overflow-hidden">
    <!-- Post Header -->
    <div
      class="flex items-start justify-between px-5 py-4 border-b border-gray-100"
    >
      <div class="flex gap-3 flex-1">
        <!-- Avatar -->
        <div
          class="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center shrink-0"
        >
          <i class="pi pi-user text-gray-400 text-xl" />
        </div>

        <!-- Author Details -->
        <div class="flex-1">
          <h4 class="text-sm font-semibold text-gray-900 m-0 mb-1">
            {{ post.student.full_name }}
          </h4>
          <p
            class="text-xs text-gray-500 m-0 flex items-center gap-1 flex-wrap"
          >
            <span>{{ post.student.department_name }}</span>
            <span class="mx-1">·</span>
            <span>{{ formatDate(post.published_to_feed_at) }}</span>
            <Tag
              v-if="post.published_by"
              :value="`Được duyệt bởi ${post.published_by.full_name}`"
              severity="secondary"
              class="ml-1"
            />
          </p>
        </div>
      </div>

      <!-- Featured Badge -->
      <Tag
        v-if="post.is_featured"
        value="Nổi bật"
        icon="pi pi-star-fill"
        class="featured-tag"
      />
    </div>

    <!-- Case Content -->
    <div class="px-5 py-4">
      <h3 class="text-lg font-semibold text-gray-900 m-0 mb-3 leading-snug">
        {{ post.title }}
      </h3>

      <!-- Meta badges -->
      <div class="flex gap-2 flex-wrap mb-3">
        <Tag :value="post.specialty" severity="info" />
        <Tag
          :value="formatComplexity(post.case?.complexity_level || 'basic')"
          severity="secondary"
        />
        <Tag
          :value="
            post.feed_visibility === 'university' ? 'Toàn trường' : 'Cùng khoa'
          "
          severity="contrast"
        />
      </div>

      <!-- Summary -->
      <div
        v-if="post.case_summary"
        class="text-gray-600 leading-relaxed my-3 text-sm"
      >
        <p :class="{ 'line-clamp-3': !expanded }" class="m-0">
          {{ post.case_summary }}
        </p>
      </div>

      <!-- Expand toggle -->
      <Button
        v-if="post.case_summary && post.case_summary.length > 200"
        :label="expanded ? 'Thu gọn' : 'Xem thêm'"
        :icon="expanded ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"
        icon-pos="right"
        text
        size="small"
        class="p-0 text-blue-500"
        @click="toggleExpand"
      />
    </div>

    <!-- Stats Bar -->
    <div
      class="flex items-center justify-between px-5 py-2 border-t border-b border-gray-100 text-xs text-gray-500"
    >
      <div class="flex items-center gap-3">
        <span v-if="post.reaction_count > 0" class="flex items-center gap-1">
          <i class="pi pi-heart text-blue-400" />
          <span class="font-medium">{{ post.reaction_count }} lượt thích</span>
        </span>
      </div>
      <div class="flex items-center gap-3">
        <span v-if="post.comments_count > 0" class="flex items-center gap-1">
          <i class="pi pi-comments" />
          {{ post.comments_count }} bình luận
        </span>
        <span class="flex items-center gap-1">
          <i class="pi pi-eye" />
          {{ post.view_count }} lượt xem
        </span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex px-2 py-1 gap-1">
      <!-- Like (blue when active; mutually exclusive with love) -->
      <Button
        :icon="
          likeLoveReaction === 'like'
            ? 'pi pi-thumbs-up-fill'
            : 'pi pi-thumbs-up'
        "
        label="Thích"
        text
        size="small"
        :class="[
          'reaction-btn',
          likeLoveReaction === 'like'
            ? 'reaction-active-blue'
            : 'reaction-inactive',
        ]"
        @click="react('like')"
      />

      <!-- Love (red when active; mutually exclusive with like) -->
      <Button
        :icon="likeLoveReaction === 'love' ? 'pi pi-heart-fill' : 'pi pi-heart'"
        label="Yêu thích"
        text
        size="small"
        :class="[
          'reaction-btn',
          likeLoveReaction === 'love'
            ? 'reaction-active-red'
            : 'reaction-inactive',
        ]"
        @click="react('love')"
      />

      <!-- Insightful (yellow, independent toggle) -->
      <Button
        :icon="insightfulActive ? 'pi pi-star-fill' : 'pi pi-star'"
        label="Hữu ích"
        text
        size="small"
        :class="[
          'reaction-btn',
          insightfulActive ? 'reaction-active-yellow' : 'reaction-inactive',
        ]"
        @click="react('insightful')"
      />

      <!-- Learned (green, independent toggle) -->
      <Button
        :icon="learnedActive ? 'pi pi-verified' : 'pi pi-graduation-cap'"
        label="Học được"
        text
        size="small"
        :class="[
          'reaction-btn',
          learnedActive ? 'reaction-active-green' : 'reaction-inactive',
        ]"
        @click="react('learned')"
      />

      <!-- Comment -->
      <Button
        icon="pi pi-comment"
        label="Bình luận"
        text
        size="small"
        class="reaction-btn reaction-inactive"
        @click="viewFullCase"
      />

      <!-- View Full -->
      <Button
        icon="pi pi-arrow-right"
        label="Xem đầy đủ"
        text
        size="small"
        class="reaction-btn reaction-inactive"
        @click="viewFullCase"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useToast } from "@/composables/useToast";
import feedService from "@/services/feed";
import Button from "primevue/button";
import Tag from "primevue/tag";

interface Props {
  post: any;
}

const props = defineProps<Props>();
const emit = defineEmits(["react", "comment", "refresh", "view-details"]);

const { toast } = useToast();

const expanded = ref(false);

// like and love are mutually exclusive — stored as a single nullable ref.
// insightful and learned are independent boolean toggles.
const likeLoveReaction = ref<"like" | "love" | null>(
  props.post.user_reaction === "like" || props.post.user_reaction === "love"
    ? props.post.user_reaction
    : null,
);
const insightfulActive = ref(props.post.user_reaction === "insightful");
const learnedActive = ref(props.post.user_reaction === "learned");

const toggleExpand = () => {
  expanded.value = !expanded.value;
};

const react = async (
  reactionType: "like" | "love" | "insightful" | "learned",
) => {
  try {
    await feedService.toggleReaction(props.post.id, reactionType, null);

    if (reactionType === "like" || reactionType === "love") {
      if (likeLoveReaction.value === reactionType) {
        // Same button — toggle off
        likeLoveReaction.value = null;
        props.post.reaction_count--;
      } else {
        // Switch within the pair (or activate from null)
        const wasNull = likeLoveReaction.value === null;
        likeLoveReaction.value = reactionType;
        if (wasNull) props.post.reaction_count++;
      }
    } else if (reactionType === "insightful") {
      insightfulActive.value = !insightfulActive.value;
      props.post.reaction_count += insightfulActive.value ? 1 : -1;
    } else if (reactionType === "learned") {
      learnedActive.value = !learnedActive.value;
      props.post.reaction_count += learnedActive.value ? 1 : -1;
    }

    emit("react", { caseId: props.post.id, reactionType });
  } catch (error) {
    toast.error("Không thể thực hiện reaction");
  }
};

const viewFullCase = () => {
  emit("view-details", props.post.id);
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(hours / 24);

  if (hours < 1) return "Vừa xong";
  if (hours < 24) return `${hours} giờ trước`;
  if (days < 7) return `${days} ngày trước`;

  return date.toLocaleDateString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
};

const formatComplexity = (level: string) => {
  const map: Record<string, string> = {
    basic: "Cơ bản",
    intermediate: "Trung cấp",
    advanced: "Nâng cao",
    expert: "Chuyên gia",
  };
  return map[level] || level;
};
</script>

<style scoped>
.featured-tag {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  font-weight: 600;
  border: none;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Reaction buttons — override PrimeVue text Button defaults */
.reaction-btn.p-button {
  flex: 1;
  justify-content: center;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition:
    background 0.15s,
    color 0.15s;
}

/* Inactive — grey text, subtle hover */
.reaction-inactive.p-button {
  color: #6b7280 !important;
  background: transparent !important;
}

.reaction-inactive.p-button:hover {
  background: #f3f4f6 !important;
  color: #374151 !important;
}

/* Like — blue */
.reaction-active-blue.p-button,
.reaction-active-blue.p-button:enabled {
  color: #2563eb !important;
  background: #eff6ff !important;
}

.reaction-active-blue.p-button:hover {
  background: #dbeafe !important;
}

/* Love — red */
.reaction-active-red.p-button,
.reaction-active-red.p-button:enabled {
  color: #dc2626 !important;
  background: #fef2f2 !important;
}

.reaction-active-red.p-button:hover {
  background: #fee2e2 !important;
}

/* Insightful — yellow/amber */
.reaction-active-yellow.p-button,
.reaction-active-yellow.p-button:enabled {
  color: #d97706 !important;
  background: #fffbeb !important;
}

.reaction-active-yellow.p-button:hover {
  background: #fef3c7 !important;
}

/* Learned — green */
.reaction-active-green.p-button,
.reaction-active-green.p-button:enabled {
  color: #16a34a !important;
  background: #f0fdf4 !important;
}

.reaction-active-green.p-button:hover {
  background: #dcfce7 !important;
}

@media (max-width: 640px) {
  .reaction-btn.p-button {
    font-size: 13px;
    padding: 8px 6px;
  }
}
</style>
