<template>
  <div class="space-y-6">
    <!-- Overall Progress -->
    <div class="bg-white rounded-lg shadow grid grid-cols-1 md:grid-cols-3 gap-6 p-3">
      <div class="card">
        <div class="card-header pb-3 flex items-center gap-2 text-muted-foreground">
          <Target class="h-4 w-4" />
          <h3>Completion Rate</h3>
        </div>
        <div class="card-content space-y-2">
          <div class="flex items-baseline gap-2">
            <span class="text-gray-800">{{ completionRate }}%</span>
            <span class="text-sm text-muted-foreground">
              {{ stats.completedCases }}/{{ stats.totalCases }} cases
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-blue-500 h-2 rounded-full" :style="{ width: completionRate + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header pb-3 flex items-center gap-2 text-muted-foreground">
          <Award class="h-4 w-4" />
          <h3>Average Grade</h3>
        </div>
        <div class="card-content space-y-2">
          <div class="flex items-baseline gap-2">
            <span class="text-gray-800">{{ stats.averageGrade }}%</span>
            <span class="flex items-center gap-1 text-sm bg-gray-100 px-2 py-1 rounded">
              <TrendingUp class="h-3 w-3" />
              {{ stats.recentTrend }}
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-green-500 h-2 rounded-full" :style="{ width: stats.averageGrade + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header pb-3 flex items-center gap-2 text-muted-foreground">
          <Clock class="h-4 w-4" />
          <h3>Study Time</h3>
        </div>
        <div class="card-content space-y-2">
          <div class="flex items-baseline gap-2">
            <span class="text-gray-800">{{ stats.studyTime }}h</span>
            <span class="text-sm text-muted-foreground">
              / {{ stats.targetStudyTime }}h goal
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-purple-500 h-2 rounded-full" :style="{ width: studyProgress + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    

    <!-- Skills Assessment -->
    <div class="bg-white p-3 rounded-lg shadow card">
      <div class="card-header">
        <h3>Clinical Skills Assessment</h3>
        <p class="text-muted-foreground">
          Your proficiency across key clinical competencies
        </p>
      </div>
      <div class="card-content space-y-4">
        <div v-for="skill in skillsProgress" :key="skill.skill" class="space-y-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <CheckCircle class="h-4 w-4 text-primary" />
              <span class="font-medium">{{ skill.skill }}</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-sm text-muted-foreground">
                {{ skill.progress }}%
              </span>
              <span class="text-sm px-2 py-1 rounded" :class="getSkillColor(skill.progress)">
                {{ skill.level }}
              </span>
            </div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="h-2 rounded-full" :class="{
              'bg-green-500': skill.progress >= 85,
              'bg-blue-500': skill.progress >= 70 && skill.progress < 85,
              'bg-yellow-500': skill.progress < 70
            }" :style="{ width: skill.progress + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Strengths & Focus Areas -->
    <div class="bg-white rounded-lg shadow grid grid-cols-1 md:grid-cols-2 gap-4 p-3">
      <div class="card">
        <div class="card-header flex items-center gap-2 text-green-700 mb-3">
          <Award class="h-5 w-5" />
          <h3>Strengths</h3>
        </div>
        <div class="card-content space-y-2">
          <div v-for="(strength, index) in stats.strengths" :key="index" class="flex items-center gap-2 text-green-700">
            <CheckCircle class="h-4 w-4" />
            <span>{{ strength }}</span>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header flex items-center gap-2 text-orange-700 mb-3">
          <Target class="h-5 w-5" />
          <h3>Focus Areas</h3>
        </div>
        <div class="card-content space-y-2">
          <div v-for="(area, index) in stats.needsImprovement" :key="index"
            class="flex items-center gap-2 text-orange-700">
            <TrendingUp class="h-4 w-4" />
            <span>{{ area }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Award,
  TrendingUp,
  Target,
  BookOpen,
  Clock,
  CheckCircle
} from "lucide-vue-next";
import { computed } from "vue";

const props = defineProps<{ studentName?: string }>();
const student = computed(() => props.studentName || "Student");

const stats = {
  totalCases: 45,
  completedCases: 32,
  averageGrade: 87,
  strengths: ["Differential Diagnosis", "Treatment Planning"],
  needsImprovement: ["Physical Examination Documentation"],
  recentTrend: "improving",
  studyTime: 42,
  targetStudyTime: 50
};

const departmentProgress = [
  { department: "Cardiology", completed: 12, total: 15, avgGrade: 89 },
  { department: "Pulmonology", completed: 8, total: 10, avgGrade: 85 },
  { department: "Neurology", completed: 7, total: 12, avgGrade: 82 },
  { department: "Nephrology", completed: 5, total: 8, avgGrade: 91 }
];

const skillsProgress = [
  { skill: "History Taking", progress: 92, level: "Advanced" },
  { skill: "Differential Diagnosis", progress: 88, level: "Advanced" },
  { skill: "Treatment Planning", progress: 85, level: "Proficient" },
  { skill: "Physical Examination", progress: 72, level: "Developing" },
  { skill: "Clinical Documentation", progress: 78, level: "Proficient" }
];

const completionRate = Math.round((stats.completedCases / stats.totalCases) * 100);
const studyProgress = Math.round((stats.studyTime / stats.targetStudyTime) * 100);

function getSkillColor(progress: number) {
  if (progress >= 85) return "bg-green-100 text-green-700";
  if (progress >= 70) return "bg-blue-100 text-blue-700";
  return "bg-yellow-100 text-yellow-700";
}
</script>
