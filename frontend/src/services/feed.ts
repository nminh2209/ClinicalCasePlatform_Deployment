/**
 * Public Feed Service
 * Social media-style feed for sharing approved cases
 */

import api from "./api";

export interface FeedPost {
  id: number;
  title: string;
  case_status: string;
  specialty: string;
  complexity_level: string;
  case_summary: string;
  student: {
    id: number;
    full_name: string;
    department_name: string;
    specialization?: string;
  };
  published_by: {
    id: number;
    full_name: string;
  };
  published_to_feed_at: string;
  feed_visibility: 'department' | 'university';
  is_featured: boolean;
  view_count: number;
  reaction_count: number;
  comments_count: number;
  reactions?: {
    total: number;
    breakdown: {
      like?: number;
      love?: number;
      insightful?: number;
      learned?: number;
    };
  };
  user_reaction?: 'like' | 'love' | 'insightful' | 'learned' | null;
}

export interface ReactionSummary {
  total: number;
  breakdown: {
    like?: number;
    love?: number;
    insightful?: number;
    learned?: number;
  };
  user_reaction: string | null;
  recent_reactions: Array<{
    user: string;
    reaction_type: string;
    created_at: string;
  }>;
}

export interface FeedStatistics {
  total_published: number;
  department_published: number;
  featured_count: number;
  total_reactions: number;
  most_reacted: Array<{
    id: number;
    title: string;
    reaction_count: number;
    specialty: string;
  }>;
  most_viewed: Array<{
    id: number;
    title: string;
    view_count: number;
    specialty: string;
  }>;
  recent_featured: Array<{
    id: number;
    title: string;
    specialty: string;
    published_to_feed_at: string;
  }>;
}

export const feedService = {
  /**
   * Get public feed posts
   * @param params Filter parameters
   */
  async getFeed(params?: {
    filter?: 'all' | 'department' | 'featured';
    specialty?: string;
    department_id?: number;
    page?: number;
    page_size?: number;
  }) {
    const response = await api.get('/cases/public-feed/', { params });
    return response.data;
  },

  /**
   * Get single feed post with full details
   * @param id Case ID
   */
  async getFeedPost(id: number) {
    const response = await api.get(`/cases/public-feed/${id}/`);
    return response.data;
  },

  /**
   * Publish case to public feed (Instructor only)
   * @param caseId Case ID
   * @param data Publication options
   */
  async publishToFeed(
    caseId: number,
    data: {
      feed_visibility?: 'department' | 'university';
      is_featured?: boolean;
    }
  ) {
    const response = await api.post(`/cases/${caseId}/publish-to-feed/`, data);
    return response.data;
  },

  /**
   * Unpublish case from public feed (Instructor only)
   * @param caseId Case ID
   */
  async unpublishFromFeed(caseId: number) {
    const response = await api.post(`/cases/${caseId}/unpublish-from-feed/`);
    return response.data;
  },

  /**
   * React to a case
   * @param caseId Case ID
   * @param reactionType Type of reaction
   */
  async reactToCase(
    caseId: number,
    reactionType: 'like' | 'love' | 'insightful' | 'learned'
  ) {
    const response = await api.post(`/cases/${caseId}/react/`, {
      reaction_type: reactionType,
    });
    return response.data;
  },

  /**
   * Remove reaction from a case
   * @param caseId Case ID
   */
  async removeReaction(caseId: number) {
    const response = await api.delete(`/cases/${caseId}/react/`);
    return response.data;
  },

  /**
   * Get detailed reactions for a case
   * @param caseId Case ID
   */
  async getReactions(caseId: number): Promise<ReactionSummary> {
    const response = await api.get(`/cases/${caseId}/reactions/`);
    return response.data;
  },

  /**
   * Get feed statistics
   */
  async getStatistics(): Promise<FeedStatistics> {
    const response = await api.get('/cases/feed-statistics/');
    return response.data;
  },

  /**
   * Toggle reaction (add if not exists, update if different, remove if same)
   * @param caseId Case ID
   * @param reactionType Type of reaction
   * @param currentReaction User's current reaction
   */
  async toggleReaction(
    caseId: number,
    reactionType: 'like' | 'love' | 'insightful' | 'learned',
    currentReaction: string | null
  ) {
    if (currentReaction === reactionType) {
      // Remove reaction if clicking same type
      return await this.removeReaction(caseId);
    } else {
      // Add or update reaction
      return await this.reactToCase(caseId, reactionType);
    }
  },
};

export default feedService;
