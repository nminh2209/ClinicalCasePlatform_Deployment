<template>
  <div v-if="loading" class="space-y-6">
    <!-- Loading skeleton -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="animate-pulse space-y-4">
        <div class="h-4 bg-gray-200 rounded w-1/4"></div>
        <div class="h-8 bg-gray-200 rounded w-1/2"></div>
        <div class="h-2 bg-gray-200 rounded"></div>
      </div>
    </div>
  </div>

  <div v-else-if="stats.totalCases === 0" class="bg-white rounded-lg shadow p-12 text-center">
    <div class="text-gray-400 mb-4">
      <BookOpen class="h-16 w-16 mx-auto" />
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-2">Chưa có dữ liệu</h3>
    <p class="text-gray-500">Bạn chưa có bệnh án nào để phân tích tiến độ.</p>
  </div>

  <div v-else class="space-y-6">
    <!-- Overall Progress -->
    <div class="bg-white rounded-lg shadow grid grid-cols-1 md:grid-cols-3 gap-6 p-3">
      <div class="card">
        <div class="card-header pb-3 flex items-center gap-2 text-muted-foreground">
          <Target class="h-4 w-4" />
          <h3>Tỷ lệ hoàn thành</h3>
        </div>
        <div class="card-content space-y-2">
          <div class="flex items-baseline gap-2">
            <span class="text-gray-800 text-2xl font-bold">{{ completionRate }}%</span>
            <span class="text-sm text-muted-foreground">
              {{ stats.completedCases }}/{{ stats.totalCases }} bệnh án
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
          <h3>Điểm trung bình</h3>
        </div>
        <div class="card-content space-y-2">
          <div class="flex items-baseline gap-2">
            <span class="text-gray-800 text-2xl font-bold">{{ stats.averageGrade }}%</span>
            <span class="flex items-center gap-1 text-sm px-2 py-1 rounded" :class="{
              'bg-green-100 text-green-700': stats.recentTrend === 'improving',
              'bg-red-100 text-red-700': stats.recentTrend === 'declining',
              'bg-gray-100 text-gray-700': stats.recentTrend === 'stable'
            }">
              <TrendingUp v-if="stats.recentTrend === 'improving'" class="h-3 w-3" />
              <svg v-else-if="stats.recentTrend === 'declining'" class="h-3 w-3" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path>
              </svg>
              {{ stats.recentTrend === 'improving' ? 'Tiến bộ' : stats.recentTrend === 'declining' ? 'Giảm' : 'Ổn định'
              }}
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="h-2 rounded-full" :class="{
              'bg-green-500': stats.averageGrade >= 85,
              'bg-blue-500': stats.averageGrade >= 70 && stats.averageGrade < 85,
              'bg-yellow-500': stats.averageGrade < 70
            }" :style="{ width: stats.averageGrade + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header pb-3 flex items-center gap-2 text-muted-foreground">
          <Clock class="h-4 w-4" />
          <h3>Giờ học</h3>
        </div>
        <div class="card-content space-y-2">
          <div class="flex items-baseline gap-2">
            <span class="text-gray-800 text-2xl font-bold">{{ stats.studyTime }}h</span>
            <span class="text-sm text-muted-foreground">
              / {{ stats.targetStudyTime }}h mục tiêu
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-purple-500 h-2 rounded-full" :style="{ width: studyProgress + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Specialty Progress -->
    <div v-if="departmentProgress.length > 0" class="bg-white p-3 rounded-lg shadow card">
      <div class="card-header">
        <h3>Tiến độ theo chuyên khoa</h3>
        <p class="text-muted-foreground">
          Phân tích tiến độ theo từng chuyên khoa
        </p>
      </div>
      <div class="card-content space-y-3">
        <div v-for="dept in departmentProgress" :key="dept.department" class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-medium">{{ dept.department }}</span>
            <div class="flex items-center gap-3">
              <span class="text-sm text-muted-foreground">
                {{ dept.completed }}/{{ dept.total }} hoàn thành
              </span>
              <span v-if="dept.avgGrade > 0" class="text-sm font-medium px-2 py-1 rounded" :class="{
                'bg-green-100 text-green-700': dept.avgGrade >= 85,
                'bg-blue-100 text-blue-700': dept.avgGrade >= 70 && dept.avgGrade < 85,
                'bg-yellow-100 text-yellow-700': dept.avgGrade < 70
              }">
                {{ dept.avgGrade }}%
              </span>
            </div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-blue-500 h-2 rounded-full" :style="{ width: (dept.completed / dept.total * 100) + '%' }">
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Skills Assessment -->
    <div class="bg-white p-3 rounded-lg shadow card">
      <div class="card-header">
        <h3>Đánh giá kỹ năng lâm sàng</h3>
        <p class="text-muted-foreground">
          Phân tích điểm theo từng kỹ năng lâm sàng
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
          <h3>Điểm mạnh</h3>
        </div>
        <div class="card-content space-y-2">
          <div v-if="stats.strengths.length > 0" v-for="(strength, index) in stats.strengths" :key="index"
            class="flex items-center gap-2 text-green-700">
            <CheckCircle class="h-4 w-4" />
            <span>{{ strength }}</span>
          </div>
          <p v-else class="text-sm text-muted-foreground italic">
            Chưa có đánh giá. Hoàn thành thêm bệnh án để xác định điểm mạnh.
          </p>
        </div>
      </div>

      <div class="card">
        <div class="card-header flex items-center gap-2 text-orange-700 mb-3">
          <Target class="h-5 w-5" />
          <h3>Cần cải thiện</h3>
        </div>
        <div class="card-content space-y-2">
          <div v-if="stats.needsImprovement.length > 0" v-for="(area, index) in stats.needsImprovement" :key="index"
            class="flex items-center gap-2 text-orange-700">
            <TrendingUp class="h-4 w-4" />
            <span>{{ area }}</span>
          </div>
          <p v-else class="text-sm text-green-600 italic flex items-center gap-2">
            <CheckCircle class="h-4 w-4" />
            Tất cả kỹ năng đều ở mức tốt! Hãy duy trì phong độ.
          </p>
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
import { computed, ref, onMounted } from "vue";
import { casesService } from "@/services/cases";
import { gradesService } from "@/services/grades";

const props = defineProps<{ studentName?: string }>();
const student = computed(() => props.studentName || "Student");

// Real data refs
const casesData = ref<any[]>([]);
const gradesData = ref<any[]>([]);
const loading = ref(true);

// Computed stats from real data
const stats = computed(() => {
  const totalCases = casesData.value.length;
  const completedCases = casesData.value.filter((c: any) =>
    c.case_status === 'submitted' || c.case_status === 'approved' || c.case_status === 'reviewed'
  ).length;

  // Calculate average grade
  const gradedCases = gradesData.value.filter((g: any) => g.is_final && g.score !== null);
  const averageGrade = gradedCases.length > 0
    ? Math.round(gradedCases.reduce((sum: number, g: any) => sum + (g.score || 0), 0) / gradedCases.length)
    : 0;

  // Analyze strengths and weaknesses from grading criteria
  const criteriaScores = {
    history: [] as number[],
    examination: [] as number[],
    differential: [] as number[],
    treatment: [] as number[],
    presentation: [] as number[]
  };

  gradedCases.forEach((g: any) => {
    if (g.grading_criteria) {
      if (g.grading_criteria.history) criteriaScores.history.push(g.grading_criteria.history);
      if (g.grading_criteria.examination) criteriaScores.examination.push(g.grading_criteria.examination);
      if (g.grading_criteria.differential) criteriaScores.differential.push(g.grading_criteria.differential);
      if (g.grading_criteria.treatment) criteriaScores.treatment.push(g.grading_criteria.treatment);
      if (g.grading_criteria.presentation) criteriaScores.presentation.push(g.grading_criteria.presentation);
    }
  });

  // Calculate averages for each criteria
  const avgHistory = criteriaScores.history.length > 0
    ? criteriaScores.history.reduce((a, b) => a + b, 0) / criteriaScores.history.length : 0;
  const avgExamination = criteriaScores.examination.length > 0
    ? criteriaScores.examination.reduce((a, b) => a + b, 0) / criteriaScores.examination.length : 0;
  const avgDifferential = criteriaScores.differential.length > 0
    ? criteriaScores.differential.reduce((a, b) => a + b, 0) / criteriaScores.differential.length : 0;
  const avgTreatment = criteriaScores.treatment.length > 0
    ? criteriaScores.treatment.reduce((a, b) => a + b, 0) / criteriaScores.treatment.length : 0;
  const avgPresentation = criteriaScores.presentation.length > 0
    ? criteriaScores.presentation.reduce((a, b) => a + b, 0) / criteriaScores.presentation.length : 0;

  // Identify strengths (>= 85) and areas needing improvement (< 70)
  const skillAverages = [
    { name: "Lấy tiền sử bệnh", score: avgHistory },
    { name: "Khám lâm sàng", score: avgExamination },
    { name: "Chẩn đoán phân biệt", score: avgDifferential },
    { name: "Kế hoạch điều trị", score: avgTreatment },
    { name: "Trình bày ca bệnh", score: avgPresentation }
  ];

  const strengths = skillAverages
    .filter(s => s.score >= 85)
    .sort((a, b) => b.score - a.score)
    .map(s => s.name)
    .slice(0, 3);

  const needsImprovement = skillAverages
    .filter(s => s.score > 0 && s.score < 70)
    .sort((a, b) => a.score - b.score)
    .map(s => s.name)
    .slice(0, 3);

  // Calculate trend (comparing recent vs older grades)
  const sortedGrades = [...gradedCases].sort((a: any, b: any) =>
    new Date(a.graded_at).getTime() - new Date(b.graded_at).getTime()
  );

  let recentTrend = "stable";
  if (sortedGrades.length >= 4) {
    const recentHalf = sortedGrades.slice(Math.floor(sortedGrades.length / 2));
    const olderHalf = sortedGrades.slice(0, Math.floor(sortedGrades.length / 2));

    const recentAvg = recentHalf.reduce((sum: number, g: any) => sum + (g.score || 0), 0) / recentHalf.length;
    const olderAvg = olderHalf.reduce((sum: number, g: any) => sum + (g.score || 0), 0) / olderHalf.length;

    if (recentAvg > olderAvg + 5) recentTrend = "improving";
    else if (recentAvg < olderAvg - 5) recentTrend = "declining";
  }

  // Calculate total study time from cases (estimated)
  const studyTime = casesData.value.reduce((sum: any, c: any) =>
    sum + (c.estimated_study_hours || 0), 0
  );

  const targetStudyTime = totalCases * 2; // Assume 2 hours per case target

  return {
    totalCases,
    completedCases,
    averageGrade,
    strengths: strengths.length > 0 ? strengths : ["Chưa có dữ liệu đánh giá"],
    needsImprovement: needsImprovement.length > 0 ? needsImprovement : ["Chưa có dữ liệu đánh giá"],
    recentTrend,
    studyTime,
    targetStudyTime,
    avgHistory,
    avgExamination,
    avgDifferential,
    avgTreatment,
    avgPresentation
  };
});

// Department progress from real data
const departmentProgress = computed(() => {
  const specialtyMap = new Map<string, { completed: number; total: number; grades: number[] }>();

  casesData.value.forEach((c: any) => {
    const specialty = c.specialty || 'Khác';
    if (!specialtyMap.has(specialty)) {
      specialtyMap.set(specialty, { completed: 0, total: 0, grades: [] });
    }

    const data = specialtyMap.get(specialty)!;
    data.total++;

    if (c.case_status === 'submitted' || c.case_status === 'approved' || c.case_status === 'reviewed') {
      data.completed++;
    }

    // Find grade for this case
    const grade = gradesData.value.find((g: any) => g.case === c.id);
    if (grade?.is_final && grade.score !== null) {
      data.grades.push(grade.score);
    }
  });

  return Array.from(specialtyMap.entries())
    .map(([department, data]) => ({
      department,
      completed: data.completed,
      total: data.total,
      avgGrade: data.grades.length > 0
        ? Math.round(data.grades.reduce((a, b) => a + b, 0) / data.grades.length)
        : 0
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 5); // Top 5 specialties
});

// Skills progress from grading criteria
const skillsProgress = computed(() => {
  const s = stats.value;

  return [
    {
      skill: "Lấy tiền sử bệnh",
      progress: Math.round(s.avgHistory || 0),
      level: getSkillLevel(s.avgHistory || 0)
    },
    {
      skill: "Khám lâm sàng",
      progress: Math.round(s.avgExamination || 0),
      level: getSkillLevel(s.avgExamination || 0)
    },
    {
      skill: "Chẩn đoán phân biệt",
      progress: Math.round(s.avgDifferential || 0),
      level: getSkillLevel(s.avgDifferential || 0)
    },
    {
      skill: "Kế hoạch điều trị",
      progress: Math.round(s.avgTreatment || 0),
      level: getSkillLevel(s.avgTreatment || 0)
    },
    {
      skill: "Trình bày ca bệnh",
      progress: Math.round(s.avgPresentation || 0),
      level: getSkillLevel(s.avgPresentation || 0)
    }
  ].filter(skill => skill.progress > 0); // Only show skills with data
});

const completionRate = computed(() =>
  stats.value.totalCases > 0
    ? Math.round((stats.value.completedCases / stats.value.totalCases) * 100)
    : 0
);

const studyProgress = computed(() =>
  stats.value.targetStudyTime > 0
    ? Math.min(100, Math.round((stats.value.studyTime / stats.value.targetStudyTime) * 100))
    : 0
);

function getSkillLevel(progress: number): string {
  if (progress >= 90) return "Xuất sắc";
  if (progress >= 85) return "Giỏi";
  if (progress >= 70) return "Khá";
  if (progress >= 60) return "Trung bình";
  if (progress > 0) return "Cần cố gắng";
  return "Chưa có dữ liệu";
}

function getSkillColor(progress: number) {
  if (progress >= 85) return "bg-green-100 text-green-700";
  if (progress >= 70) return "bg-blue-100 text-blue-700";
  if (progress > 0) return "bg-yellow-100 text-yellow-700";
  return "bg-gray-100 text-gray-700";
}

// Load data on mount
async function loadProgressData() {
  loading.value = true;
  try {
    const [cases, grades] = await Promise.all([
      casesService.getCases(),
      gradesService.getStudentGrades().catch(() => [])
    ]);

    casesData.value = Array.isArray(cases) ? cases : (cases?.results || []);
    gradesData.value = Array.isArray(grades) ? grades : (grades?.results || []);
  } catch (error) {
    console.error("Error loading progress data:", error);
    casesData.value = [];
    gradesData.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadProgressData();
});
</script>
