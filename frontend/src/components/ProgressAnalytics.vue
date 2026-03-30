<template>
  <div v-if="loading" class="space-y-6">
    <div class="bg-white rounded-lg shadow p-6">
      <Skeleton height="1rem" width="25%" class="mb-4" />
      <Skeleton height="2rem" width="50%" class="mb-4" />
      <Skeleton height="0.5rem" />
    </div>
  </div>

  <div
    v-else-if="stats.totalCases === 0"
    class="bg-white rounded-lg shadow p-12 text-center"
  >
    <div class="text-gray-300 mb-4">
      <i class="pi pi-book" style="font-size: 4rem" />
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-2">Chưa có dữ liệu</h3>
    <p class="text-gray-500">Bạn chưa có bệnh án nào để phân tích tiến độ.</p>
  </div>

  <div v-else class="space-y-6">
    <!-- Overall Progress -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card class="shadow-sm">
        <template #content>
          <div class="flex items-center gap-2 text-gray-500 mb-3">
            <i class="pi pi-bullseye" />
            <span class="text-sm font-medium">Tỷ lệ hoàn thành</span>
          </div>
          <div class="flex items-baseline gap-2 mb-2">
            <span class="text-gray-800 text-2xl font-bold"
              >{{ completionRate }}%</span
            >
            <span class="text-sm text-gray-500">
              {{ stats.completedCases }}/{{ stats.totalCases }} bệnh án
            </span>
          </div>
          <ProgressBar
            :value="completionRate"
            :show-value="false"
            style="height: 0.5rem"
          />
        </template>
      </Card>

      <Card class="shadow-sm">
        <template #content>
          <div class="flex items-center gap-2 text-gray-500 mb-3">
            <i class="pi pi-star" />
            <span class="text-sm font-medium">Điểm trung bình</span>
          </div>
          <div class="flex items-baseline gap-2 mb-2">
            <span class="text-gray-800 text-2xl font-bold"
              >{{ stats.averageGrade }}%</span
            >
            <Tag
              :value="trendLabel(stats.recentTrend)"
              :severity="trendSeverity(stats.recentTrend)"
              :icon="trendIcon(stats.recentTrend)"
            />
          </div>
          <ProgressBar
            :value="stats.averageGrade"
            :show-value="false"
            :style="{
              height: '0.5rem',
              '--p-progressbar-value-background': gradeColor(
                stats.averageGrade,
              ),
            }"
          />
        </template>
      </Card>

      <Card class="shadow-sm">
        <template #content>
          <div class="flex items-center gap-2 text-gray-500 mb-3">
            <i class="pi pi-clock" />
            <span class="text-sm font-medium">Giờ học</span>
          </div>
          <div class="flex items-baseline gap-2 mb-2">
            <span class="text-gray-800 text-2xl font-bold"
              >{{ stats.studyTime }}h</span
            >
            <span class="text-sm text-gray-500"
              >/ {{ stats.targetStudyTime }}h mục tiêu</span
            >
          </div>
          <ProgressBar
            :value="studyProgress"
            :show-value="false"
            style="height: 0.5rem"
          />
        </template>
      </Card>
    </div>

    <!-- Specialty Progress -->
    <Card v-if="departmentProgress.length > 0" class="shadow-sm">
      <template #title>Tiến độ theo chuyên khoa</template>
      <template #subtitle>Phân tích tiến độ theo từng chuyên khoa</template>
      <template #content>
        <div class="space-y-3 mt-2">
          <div
            v-for="dept in departmentProgress"
            :key="dept.department"
            class="space-y-2"
          >
            <div class="flex items-center justify-between">
              <span class="font-medium text-sm">{{ dept.department }}</span>
              <div class="flex items-center gap-3">
                <span class="text-sm text-gray-500">
                  {{ dept.completed }}/{{ dept.total }} hoàn thành
                </span>
                <Tag
                  v-if="dept.avgGrade > 0"
                  :value="dept.avgGrade + '%'"
                  :severity="
                    dept.avgGrade >= 85
                      ? 'success'
                      : dept.avgGrade >= 70
                        ? 'info'
                        : 'warn'
                  "
                />
              </div>
            </div>
            <ProgressBar
              :value="Math.round((dept.completed / dept.total) * 100)"
              :show-value="false"
              style="height: 0.5rem"
            />
          </div>
        </div>
      </template>
    </Card>

    <!-- Skills Assessment -->
    <Card class="shadow-sm">
      <template #title>Đánh giá kỹ năng lâm sàng</template>
      <template #subtitle>Phân tích điểm theo từng kỹ năng lâm sàng</template>
      <template #content>
        <div class="space-y-4 mt-2">
          <div
            v-for="skill in skillsProgress"
            :key="skill.skill"
            class="space-y-2"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <i class="pi pi-check-circle text-blue-500" />
                <span class="font-medium text-sm">{{ skill.skill }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-sm text-gray-500">{{ skill.progress }}%</span>
                <Tag
                  :value="skill.level"
                  :severity="getSkillSeverity(skill.progress)"
                />
              </div>
            </div>
            <ProgressBar
              :value="skill.progress"
              :show-value="false"
              :style="{
                height: '0.5rem',
                '--p-progressbar-value-background': gradeColor(skill.progress),
              }"
            />
          </div>
        </div>
      </template>
    </Card>

    <!-- Strengths & Focus Areas -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card class="shadow-sm border-l-4 border-green-500">
        <template #content>
          <div class="flex items-center gap-2 text-green-700 mb-3">
            <i class="pi pi-star" />
            <span class="font-semibold">Điểm mạnh</span>
          </div>
          <div v-if="stats.strengths.length > 0" class="space-y-2">
            <div
              v-for="(strength, index) in stats.strengths"
              :key="index"
              class="flex items-center gap-2 text-green-700 text-sm"
            >
              <i class="pi pi-check-circle" />
              <span>{{ strength }}</span>
            </div>
          </div>
          <p v-else class="text-sm text-gray-400 italic">
            Chưa có đánh giá. Hoàn thành thêm bệnh án để xác định điểm mạnh.
          </p>
        </template>
      </Card>

      <Card class="shadow-sm border-l-4 border-orange-500">
        <template #content>
          <div class="flex items-center gap-2 text-orange-700 mb-3">
            <i class="pi pi-bullseye" />
            <span class="font-semibold">Cần cải thiện</span>
          </div>
          <div v-if="stats.needsImprovement.length > 0" class="space-y-2">
            <div
              v-for="(area, index) in stats.needsImprovement"
              :key="index"
              class="flex items-center gap-2 text-orange-700 text-sm"
            >
              <i class="pi pi-arrow-up-right" />
              <span>{{ area }}</span>
            </div>
          </div>
          <p
            v-else
            class="text-sm text-green-600 italic flex items-center gap-2"
          >
            <i class="pi pi-check-circle" />
            Tất cả kỹ năng đều ở mức tốt! Hãy duy trì phong độ.
          </p>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import Card from "primevue/card";
import ProgressBar from "primevue/progressbar";
import Skeleton from "primevue/skeleton";
import Tag from "primevue/tag";
import { casesService } from "@/services/cases";
import { gradesService } from "@/services/grades";

const props = defineProps<{ studentName?: string }>();
const student = computed(() => props.studentName || "Student");

const casesData = ref<any[]>([]);
const gradesData = ref<any[]>([]);
const loading = ref(true);

const stats = computed(() => {
  const totalCases = casesData.value.length;
  const completedCases = casesData.value.filter(
    (c: any) =>
      c.case_status === "submitted" ||
      c.case_status === "approved" ||
      c.case_status === "reviewed",
  ).length;

  const gradedCases = gradesData.value.filter(
    (g: any) => g.is_final && g.score !== null,
  );
  const averageGrade =
    gradedCases.length > 0
      ? Math.round(
          gradedCases.reduce((sum: number, g: any) => sum + (g.score || 0), 0) /
            gradedCases.length,
        )
      : 0;

  const criteriaScores = {
    history: [] as number[],
    examination: [] as number[],
    differential: [] as number[],
    treatment: [] as number[],
    presentation: [] as number[],
  };

  gradedCases.forEach((g: any) => {
    if (g.grading_criteria) {
      if (g.grading_criteria.history)
        criteriaScores.history.push(g.grading_criteria.history);
      if (g.grading_criteria.examination)
        criteriaScores.examination.push(g.grading_criteria.examination);
      if (g.grading_criteria.differential)
        criteriaScores.differential.push(g.grading_criteria.differential);
      if (g.grading_criteria.treatment)
        criteriaScores.treatment.push(g.grading_criteria.treatment);
      if (g.grading_criteria.presentation)
        criteriaScores.presentation.push(g.grading_criteria.presentation);
    }
  });

  const avg = (arr: number[]) =>
    arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;

  const avgHistory = avg(criteriaScores.history);
  const avgExamination = avg(criteriaScores.examination);
  const avgDifferential = avg(criteriaScores.differential);
  const avgTreatment = avg(criteriaScores.treatment);
  const avgPresentation = avg(criteriaScores.presentation);

  const skillAverages = [
    { name: "Lấy tiền sử bệnh", score: avgHistory },
    { name: "Khám lâm sàng", score: avgExamination },
    { name: "Chẩn đoán phân biệt", score: avgDifferential },
    { name: "Kế hoạch điều trị", score: avgTreatment },
    { name: "Trình bày ca bệnh", score: avgPresentation },
  ];

  const strengths = skillAverages
    .filter((s) => s.score >= 85)
    .sort((a, b) => b.score - a.score)
    .map((s) => s.name)
    .slice(0, 3);

  const needsImprovement = skillAverages
    .filter((s) => s.score > 0 && s.score < 70)
    .sort((a, b) => a.score - b.score)
    .map((s) => s.name)
    .slice(0, 3);

  const sortedGrades = [...gradedCases].sort(
    (a: any, b: any) =>
      new Date(a.graded_at).getTime() - new Date(b.graded_at).getTime(),
  );

  let recentTrend = "stable";
  if (sortedGrades.length >= 4) {
    const mid = Math.floor(sortedGrades.length / 2);
    const recentHalf = sortedGrades.slice(mid);
    const olderHalf = sortedGrades.slice(0, mid);
    const recentAvg =
      recentHalf.reduce((sum: number, g: any) => sum + (g.score || 0), 0) /
      recentHalf.length;
    const olderAvg =
      olderHalf.reduce((sum: number, g: any) => sum + (g.score || 0), 0) /
      olderHalf.length;
    if (recentAvg > olderAvg + 5) recentTrend = "improving";
    else if (recentAvg < olderAvg - 5) recentTrend = "declining";
  }

  const studyTime = casesData.value.reduce(
    (sum: any, c: any) => sum + (c.estimated_study_hours || 0),
    0,
  );
  const targetStudyTime = totalCases * 2;

  return {
    totalCases,
    completedCases,
    averageGrade,
    strengths: strengths.length > 0 ? strengths : ["Chưa có dữ liệu đánh giá"],
    needsImprovement: needsImprovement.length > 0 ? needsImprovement : [],
    recentTrend,
    studyTime,
    targetStudyTime,
    avgHistory,
    avgExamination,
    avgDifferential,
    avgTreatment,
    avgPresentation,
  };
});

const departmentProgress = computed(() => {
  const specialtyMap = new Map<
    string,
    { completed: number; total: number; grades: number[] }
  >();

  casesData.value.forEach((c: any) => {
    const specialty = c.specialty || "Khác";
    if (!specialtyMap.has(specialty)) {
      specialtyMap.set(specialty, { completed: 0, total: 0, grades: [] });
    }
    const data = specialtyMap.get(specialty)!;
    data.total++;
    if (
      c.case_status === "submitted" ||
      c.case_status === "approved" ||
      c.case_status === "reviewed"
    ) {
      data.completed++;
    }
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
      avgGrade:
        data.grades.length > 0
          ? Math.round(
              data.grades.reduce((a, b) => a + b, 0) / data.grades.length,
            )
          : 0,
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 5);
});

const skillsProgress = computed(() => {
  const s = stats.value;
  return [
    {
      skill: "Lấy tiền sử bệnh",
      progress: Math.round(s.avgHistory || 0),
      level: getSkillLevel(s.avgHistory || 0),
    },
    {
      skill: "Khám lâm sàng",
      progress: Math.round(s.avgExamination || 0),
      level: getSkillLevel(s.avgExamination || 0),
    },
    {
      skill: "Chẩn đoán phân biệt",
      progress: Math.round(s.avgDifferential || 0),
      level: getSkillLevel(s.avgDifferential || 0),
    },
    {
      skill: "Kế hoạch điều trị",
      progress: Math.round(s.avgTreatment || 0),
      level: getSkillLevel(s.avgTreatment || 0),
    },
    {
      skill: "Trình bày ca bệnh",
      progress: Math.round(s.avgPresentation || 0),
      level: getSkillLevel(s.avgPresentation || 0),
    },
  ].filter((skill) => skill.progress > 0);
});

const completionRate = computed(() =>
  stats.value.totalCases > 0
    ? Math.round((stats.value.completedCases / stats.value.totalCases) * 100)
    : 0,
);

const studyProgress = computed(() =>
  stats.value.targetStudyTime > 0
    ? Math.min(
        100,
        Math.round((stats.value.studyTime / stats.value.targetStudyTime) * 100),
      )
    : 0,
);

function getSkillLevel(progress: number): string {
  if (progress >= 90) return "Xuất sắc";
  if (progress >= 85) return "Giỏi";
  if (progress >= 70) return "Khá";
  if (progress >= 60) return "Trung bình";
  if (progress > 0) return "Cần cố gắng";
  return "Chưa có dữ liệu";
}

function getSkillSeverity(progress: number): string {
  if (progress >= 85) return "success";
  if (progress >= 70) return "info";
  if (progress > 0) return "warn";
  return "secondary";
}

function gradeColor(value: number): string {
  if (value >= 85) return "var(--p-green-500)";
  if (value >= 70) return "var(--p-blue-500)";
  return "var(--p-yellow-500)";
}

function trendLabel(trend: string): string {
  if (trend === "improving") return "Tiến bộ";
  if (trend === "declining") return "Giảm";
  return "Ổn định";
}

function trendSeverity(trend: string): string {
  if (trend === "improving") return "success";
  if (trend === "declining") return "danger";
  return "secondary";
}

function trendIcon(trend: string): string {
  if (trend === "improving") return "pi pi-arrow-up-right";
  if (trend === "declining") return "pi pi-arrow-down-right";
  return "pi pi-minus";
}

async function loadProgressData() {
  loading.value = true;
  try {
    const [cases, grades] = await Promise.all([
      casesService.getCases(),
      gradesService.getStudentGrades().catch(() => []),
    ]);
    casesData.value = Array.isArray(cases) ? cases : cases?.results || [];
    gradesData.value = Array.isArray(grades) ? grades : grades?.results || [];
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
