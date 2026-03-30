<template>
  <div class="cases-page">
    <!-- ── Page Header ──────────────────────────────────── -->
    <div class="page-header">
      <div class="header-content">
        <h1 v-if="isStudent">Hồ sơ Bệnh án Lâm sàng</h1>
        <h1 v-else-if="authStore.user?.role === 'instructor'">
          Chấm điểm Bệnh án
        </h1>
        <h1 v-else>Quản lý Bệnh án</h1>

        <div class="header-actions">
          <router-link
            v-if="isStudent"
            to="/cases/create"
            custom
            v-slot="{ navigate }"
          >
            <Button
              @click="navigate"
              icon="pi pi-plus-circle"
              label="Tạo hồ sơ mới"
            />
          </router-link>
          <router-link
            v-if="authStore.user?.role === 'instructor'"
            to="/cases/create"
            custom
            v-slot="{ navigate }"
          >
            <Button
              @click="navigate"
              icon="pi pi-plus-circle"
              label="Tạo hồ sơ mẫu"
            />
          </router-link>
        </div>
      </div>
    </div>

    <!-- ── Filters and Search ───────────────────────────── -->
    <div class="filters-section">
      <div class="search-and-filters">
        <div class="search-container">
          <SearchAutocomplete
            v-model="searchQuery"
            placeholder="Tìm kiếm hồ sơ bệnh án theo tên, chuyên khoa, bệnh nhân..."
          />
        </div>
        <div class="filter-options">
          <Select
            v-model="specialtyFilter"
            @change="applyFilters"
            :options="[
              {
                name: choicesLoading ? 'Đang tải...' : 'Tất cả chuyên khoa',
                id: '',
              },
              ...specialties,
            ]"
            optionLabel="name"
            optionValue="name"
            :disabled="choicesLoading"
            placeholder="Tất cả chuyên khoa"
            class="specialty-select"
          />

          <Select
            v-model="dateSort"
            :options="[
              { label: 'Mới nhất', value: 'newest' },
              { label: 'Cũ nhất', value: 'oldest' },
            ]"
            optionLabel="label"
            optionValue="value"
            placeholder="Sắp xếp"
            class="sort-select"
          />
        </div>
      </div>

      <!-- Collection Category Tabs — SelectButton (students only) -->
      <!--
        Replaces three individual Buttons with active/outlined toggle pattern.
        SelectButton is semantically the correct segmented-control component.
      -->
      <div v-if="isStudent" class="collection-tabs">
        <SelectButton
          v-model="collectionFilter"
          :options="collectionTabOptions"
          optionLabel="label"
          optionValue="value"
          class="collection-select-btn"
          aria-label="Bộ lọc bộ sưu tập"
        />
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div
          class="stat-card"
          @click="setActiveFilter('all')"
          :class="{ 'stat-active': activeFilter === 'all' }"
        >
          <div class="stat-icon stat-primary">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
              />
              <polyline points="14,2 14,8 20,8" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ getStatusCount("all") }}</div>
            <div class="stat-label">Tổng số hồ sơ</div>
          </div>
        </div>

        <div
          class="stat-card"
          v-if="isStudent"
          @click="setActiveFilter('draft')"
          :class="{ 'stat-active': activeFilter === 'draft' }"
        >
          <div class="stat-icon stat-info">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
              />
              <polyline points="14,2 14,8 20,8" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ getStatusCount("draft") }}</div>
            <div class="stat-label">Bản nháp</div>
          </div>
        </div>

        <div
          class="stat-card"
          @click="setActiveFilter('submitted')"
          :class="{ 'stat-active': activeFilter === 'submitted' }"
        >
          <div class="stat-icon stat-warning">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22,4 12,14.01 9,11.01" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ getStatusCount("submitted") }}</div>
            <div
              class="stat-label"
              v-if="authStore.user?.role === 'instructor'"
            >
              Chưa Chấm
            </div>
            <div class="stat-label" v-else>Đã nộp</div>
          </div>
        </div>
      </div>

      <!-- ── Main Cases List ──────────────────────────────── -->
      <main class="cases-main">
        <div class="container">
          <div class="loading" v-if="loading">
            <p>Đang tải hồ sơ bệnh án...</p>
          </div>

          <div class="error" v-if="error">
            <p>{{ error }}</p>
            <Button
              @click="() => loadCases(1)"
              label="Thử lại"
              icon="pi pi-refresh"
              severity="danger"
            />
          </div>

          <!-- Cases Grid — PrimeVue Card per case -->
          <div class="cases-grid" v-if="!loading && !error">
            <div v-if="filteredCases.length === 0" class="empty-state">
              <p>
                Không tìm thấy hồ sơ bệnh án nào phù hợp với tiêu chí tìm kiếm.
              </p>
              <p v-if="cases.length > 0">
                Có {{ cases.length }} hồ sơ trong cơ sở dữ liệu nhưng không khớp
                với bộ lọc hiện tại.
              </p>
            </div>

            <!--
              PrimeVue Card for each case.
              Border-radius fix: overflow:hidden + unified radius on wrapper and body.
            -->
            <Card
              v-for="case_ in filteredCases"
              :key="case_.id"
              :class="['case-card-prime', { 'saved-case': case_.cloned_from }]"
            >
              <!-- Card title slot: case title + status badges -->
              <template #title>
                <div class="case-header-row">
                  <h3 class="case-title">{{ case_.title }}</h3>
                  <div class="header-badges">
                    <!-- Instructor Template Badge -->
                    <Tag
                      v-if="
                        case_.created_by_role === 'instructor' &&
                        !case_.cloned_from
                      "
                      value="Hồ sơ mẫu"
                      class="template-tag"
                      title="Hồ sơ mẫu từ giảng viên"
                    />
                    <!-- Saved/Cloned Badge -->
                    <Tag
                      v-if="case_.cloned_from"
                      value="Đã lưu"
                      class="saved-tag"
                      title="Hồ sơ đã lưu từ giảng viên"
                    />
                    <!-- Status Badge -->
                    <Tag
                      :class="['status-tag', case_.case_status]"
                      :value="getStatusLabel(case_.case_status)"
                    />
                  </div>
                </div>
              </template>

              <!-- Card content slot: meta info + cloned origin -->
              <template #content>
                <!-- Cloned-from info -->
                <div v-if="case_.cloned_from" class="cloned-from-info">
                  <span class="cloned-label">Nguồn gốc:</span>
                  <span class="cloned-title">{{
                    case_.cloned_from_title
                  }}</span>
                  <span
                    v-if="case_.cloned_from_instructor_name"
                    class="cloned-author"
                  >
                    (bởi {{ case_.cloned_from_instructor_name }})
                  </span>
                </div>

                <div class="case-meta">
                  <p><strong>Bệnh nhân:</strong> {{ case_.patient_name }}</p>
                  <p><strong>Tuổi:</strong> {{ case_.patient_age }}</p>
                  <p><strong>Chuyên khoa:</strong> {{ case_.specialty }}</p>
                  <p>
                    <strong>Ngày tạo:</strong>
                    {{ formatDate(case_.created_at) }}
                  </p>
                </div>
              </template>

              <!-- Card footer slot: action buttons -->
              <template #footer>
                <div class="case-actions">
                  <Button
                    @click="router.push(`/cases/${case_.id}`)"
                    label="Xem chi tiết"
                    size="small"
                    icon="pi pi-eye"
                  />

                  <!-- Save to Collection (template cases, not owner, not cloned) -->
                  <Button
                    v-if="
                      case_.created_by_role === 'instructor' &&
                      !isOwner(case_) &&
                      !case_.cloned_from
                    "
                    @click="openCloneDialog(case_)"
                    severity="success"
                    size="small"
                    label="Lưu"
                    icon="pi pi-download"
                    title="Lưu vào bộ sưu tập của bạn"
                  />

                  <!-- Sharing Button (instructors) -->
                  <Button
                    v-if="authStore.user?.role === 'instructor'"
                    @click="openSharingPanel(case_)"
                    severity="secondary"
                    size="small"
                    label="Chia sẻ"
                    icon="pi pi-share-alt"
                    title="Chia sẻ ca bệnh"
                  />

                  <!--
                    SplitButton replaces the Button+Menu toggle pattern.
                    Main action: export PDF. Dropdown: all format options.
                    `toggleExportMenu` / `showExportMenu` remain in script (unused
                    in template) — no logic was removed.
                  -->
                  <SplitButton
                    label="Xuất file"
                    icon="pi pi-file-export"
                    size="small"
                    outlined
                    :model="[
                      {
                        label: 'PDF',
                        icon: 'pi pi-file-pdf',
                        command: () => exportCase(case_, 'pdf'),
                      },
                      {
                        label: 'Word',
                        icon: 'pi pi-file-word',
                        command: () => exportCase(case_, 'word'),
                      },
                      {
                        label: 'PowerPoint',
                        icon: 'pi pi-file',
                        command: () => exportCase(case_, 'powerpoint'),
                      },
                    ]"
                    @click="exportCase(case_, 'pdf')"
                    class="export-split-btn"
                  />
                </div>
              </template>
            </Card>
          </div>

          <div
            class="empty-state"
            v-if="!loading && !error && filteredCases.length === 0"
          >
            <h3>Không tìm thấy hồ sơ bệnh án</h3>
            <p>
              {{
                searchQuery
                  ? "Thử điều chỉnh từ khóa tìm kiếm"
                  : "Không có hồ sơ bệnh án nào phù hợp với bộ lọc hiện tại"
              }}
            </p>
          </div>

          <!-- Pagination -->
          <div
            v-if="!loading && !error && pagination.total_pages > 1"
            class="pagination-wrapper"
          >
            <Paginator
              :first="(currentPage - 1) * itemsPerPage"
              :rows="itemsPerPage"
              :totalRecords="totalCases"
              class="cases-paginator"
              @page="onPageChange"
            />
          </div>
        </div>
      </main>

      <!-- ── Clone Case Dialog ──────────────────────────── -->
      <CloneCaseDialog
        :isOpen="showCloneDialog"
        :caseId="Number(cloneCaseId)"
        @close="showCloneDialog = false"
        @success="handleCloneSuccess"
      />

      <!-- ── Case Detail Modal ──────────────────────────── -->
      <Dialog
        :visible="!!(selectedCase || loading)"
        :header="selectedCase?.title || 'Đang tải...'"
        :modal="true"
        :closable="true"
        @update:visible="closeModal"
        class="case-detail-dialog w-full md:w-3/4 lg:w-2/3"
      >
        <div class="modal-content">
          <div v-if="loading && !selectedCase" class="loading-modal">
            <p>Đang tải thông tin hồ sơ...</p>
          </div>

          <div v-if="selectedCase && !loading" class="case-detail">
            <!-- Patient Information -->
            <section class="patient-info">
              <h3>🏥 Thông tin bệnh nhân</h3>
              <div class="info-grid">
                <div class="info-item">
                  <strong>Tên bệnh nhân:</strong>
                  {{ selectedCase.patient_name }}
                </div>
                <div class="info-item">
                  <strong>Tuổi:</strong> {{ selectedCase.patient_age }}
                </div>
                <div class="info-item">
                  <strong>Giới tính:</strong>
                  {{ selectedCase.patient_gender === "male" ? "Nam" : "Nữ" }}
                </div>
                <div class="info-item">
                  <strong>Số hồ sơ:</strong>
                  {{ selectedCase.medical_record_number }}
                </div>
                <div class="info-item">
                  <strong>Chuyên khoa:</strong> {{ selectedCase.specialty }}
                </div>
                <div class="info-item" v-if="selectedCase.admission_date">
                  <strong>Ngày nhập viện:</strong>
                  {{ formatDate(selectedCase.admission_date) }}
                </div>
              </div>
            </section>

            <!-- Clinical History -->
            <section
              v-if="selectedCase.clinical_history"
              class="clinical-section"
            >
              <h3>📋 Tiền sử lâm sàng</h3>
              <div class="clinical-subsection">
                <h4>Lý do khám</h4>
                <p>{{ selectedCase.clinical_history.chief_complaint }}</p>
              </div>
              <div class="clinical-subsection">
                <h4>Bệnh sử</h4>
                <p class="formatted-text">
                  {{ selectedCase.clinical_history.history_present_illness }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.clinical_history.past_medical_history"
              >
                <h4>Tiền sử bệnh</h4>
                <p>{{ selectedCase.clinical_history.past_medical_history }}</p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.clinical_history.family_history"
              >
                <h4>Tiền sử gia đình</h4>
                <p>{{ selectedCase.clinical_history.family_history }}</p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.clinical_history.medications"
              >
                <h4>Thuốc đang dùng</h4>
                <p>{{ selectedCase.clinical_history.medications }}</p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.clinical_history.allergies"
              >
                <h4>Dị ứng</h4>
                <p>{{ selectedCase.clinical_history.allergies }}</p>
              </div>
            </section>

            <!-- Physical Examination -->
            <section
              v-if="selectedCase.physical_examination"
              class="clinical-section"
            >
              <h3>🩺 Khám lâm sàng</h3>
              <div class="clinical-subsection">
                <h4>Tình trạng chung</h4>
                <p>
                  {{ selectedCase.physical_examination.general_appearance }}
                </p>
              </div>
              <div class="clinical-subsection">
                <h4>Sinh hiệu</h4>
                <p>{{ selectedCase.physical_examination.vital_signs }}</p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.physical_examination.cardiovascular"
              >
                <h4>Tim mạch</h4>
                <p class="formatted-text">
                  {{ selectedCase.physical_examination.cardiovascular }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.physical_examination.respiratory"
              >
                <h4>Hô hấp</h4>
                <p class="formatted-text">
                  {{ selectedCase.physical_examination.respiratory }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.physical_examination.abdominal"
              >
                <h4>Bụng</h4>
                <p class="formatted-text">
                  {{ selectedCase.physical_examination.abdominal }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.physical_examination.neurological"
              >
                <h4>Thần kinh</h4>
                <p>{{ selectedCase.physical_examination.neurological }}</p>
              </div>
            </section>

            <!-- Investigations -->
            <section
              v-if="selectedCase.detailed_investigations"
              class="clinical-section"
            >
              <h3>🧪 Cận lâm sàng</h3>
              <div
                class="clinical-subsection"
                v-if="selectedCase.detailed_investigations.laboratory_results"
              >
                <h4>Xét nghiệm</h4>
                <p class="formatted-text">
                  {{ selectedCase.detailed_investigations.laboratory_results }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.detailed_investigations.imaging_studies"
              >
                <h4>Chẩn đoán hình ảnh</h4>
                <p class="formatted-text">
                  {{ selectedCase.detailed_investigations.imaging_studies }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.detailed_investigations.ecg_findings"
              >
                <h4>Điện tâm đồ</h4>
                <p class="formatted-text">
                  {{ selectedCase.detailed_investigations.ecg_findings }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.detailed_investigations.biochemistry"
              >
                <h4>Sinh hóa</h4>
                <p class="formatted-text">
                  {{ selectedCase.detailed_investigations.biochemistry }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.detailed_investigations.hematology"
              >
                <h4>Huyết học</h4>
                <p class="formatted-text">
                  {{ selectedCase.detailed_investigations.hematology }}
                </p>
              </div>
            </section>

            <!-- Diagnosis and Management -->
            <section
              v-if="selectedCase.diagnosis_management"
              class="clinical-section"
            >
              <h3>💊 Chẩn đoán và điều trị</h3>
              <div class="clinical-subsection">
                <h4>Chẩn đoán chính</h4>
                <p>{{ selectedCase.diagnosis_management.primary_diagnosis }}</p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.diagnosis_management.differential_diagnosis"
              >
                <h4>Chẩn đoán phân biệt</h4>
                <p class="formatted-text">
                  {{ selectedCase.diagnosis_management.differential_diagnosis }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.diagnosis_management.treatment_plan"
              >
                <h4>Kế hoạch điều trị</h4>
                <p class="formatted-text">
                  {{ selectedCase.diagnosis_management.treatment_plan }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.diagnosis_management.medications_prescribed"
              >
                <h4>Thuốc kê đơn</h4>
                <p>
                  {{ selectedCase.diagnosis_management.medications_prescribed }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.diagnosis_management.procedures_performed"
              >
                <h4>Thủ thuật đã thực hiện</h4>
                <p>
                  {{ selectedCase.diagnosis_management.procedures_performed }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.diagnosis_management.prognosis"
              >
                <h4>Tiên lượng</h4>
                <p>{{ selectedCase.diagnosis_management.prognosis }}</p>
              </div>
            </section>

            <!-- Learning Outcomes -->
            <section
              v-if="selectedCase.learning_outcomes"
              class="clinical-section"
            >
              <h3>🎯 Mục tiêu học tập</h3>
              <div class="clinical-subsection">
                <h4>Mục tiêu học tập</h4>
                <p class="formatted-text">
                  {{ selectedCase.learning_outcomes.learning_objectives }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.learning_outcomes.key_concepts"
              >
                <h4>Khái niệm chính</h4>
                <p class="formatted-text">
                  {{ selectedCase.learning_outcomes.key_concepts }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.learning_outcomes.clinical_pearls"
              >
                <h4>Điểm lâm sàng quan trọng</h4>
                <p class="formatted-text">
                  {{ selectedCase.learning_outcomes.clinical_pearls }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.learning_outcomes.discussion_points"
              >
                <h4>Điểm thảo luận</h4>
                <p class="formatted-text">
                  {{ selectedCase.learning_outcomes.discussion_points }}
                </p>
              </div>
              <div
                class="clinical-subsection"
                v-if="selectedCase.learning_outcomes.references"
              >
                <h4>Tài liệu tham khảo</h4>
                <p class="formatted-text">
                  {{ selectedCase.learning_outcomes.references }}
                </p>
              </div>
            </section>

            <!-- Medical Attachments -->
            <section
              v-if="
                selectedCase.medical_attachments &&
                selectedCase.medical_attachments.length > 0
              "
              class="clinical-section"
            >
              <h3>📁 Tài liệu đính kèm y tế</h3>
              <div class="attachments-grid">
                <div
                  v-for="attachment in selectedCase.medical_attachments"
                  :key="attachment.id"
                  class="attachment-item"
                  :class="{ confidential: attachment.is_confidential }"
                >
                  <div class="attachment-header">
                    <div class="attachment-icon">
                      <i :class="getAttachmentIcon(attachment)"></i>
                    </div>
                    <div class="attachment-info">
                      <h4 class="attachment-title">{{ attachment.title }}</h4>
                      <p class="attachment-type">
                        {{ attachment.attachment_type_display }}
                      </p>
                      <p class="attachment-meta">
                        <span v-if="attachment.date_taken"
                          >📅 {{ formatDate(attachment.date_taken) }}</span
                        >
                        <span v-if="attachment.department_name"
                          >🏥 {{ attachment.department_name }}</span
                        >
                        <span>📏 {{ attachment.file_size_mb }} MB</span>
                      </p>
                    </div>
                    <div class="attachment-actions">
                      <Button
                        @click="downloadAttachment(attachment)"
                        icon="pi pi-download"
                        size="small"
                        :disabled="
                          attachment.is_confidential && !canViewConfidential
                        "
                        :title="
                          attachment.is_confidential && !canViewConfidential
                            ? 'Tài liệu bảo mật - Chỉ giảng viên được xem'
                            : 'Tải xuống'
                        "
                        class="download-btn-prime"
                        rounded
                      />
                    </div>
                  </div>

                  <div
                    v-if="attachment.description"
                    class="attachment-description"
                  >
                    <p><strong>Mô tả:</strong> {{ attachment.description }}</p>
                  </div>
                  <div
                    v-if="attachment.physician_notes"
                    class="attachment-notes"
                  >
                    <p>
                      <strong>Ghi chú bác sĩ:</strong>
                      {{ attachment.physician_notes }}
                    </p>
                  </div>
                  <div
                    v-if="attachment.is_confidential"
                    class="confidential-badge"
                  >
                    <i class="pi pi-lock"></i> Tài liệu bảo mật
                  </div>
                </div>
              </div>
            </section>

            <!-- Medical File Upload Section -->
            <section
              v-if="canUploadFiles"
              class="clinical-section upload-section"
            >
              <h3>📎 Thêm tài liệu y tế</h3>

              <Button
                v-if="!showUploadForm"
                @click="showUploadForm = true"
                label="Thêm tệp đính kèm"
                icon="pi pi-plus"
                severity="success"
                class="upload-toggle-btn"
              />

              <div v-if="showUploadForm" class="upload-form">
                <form
                  @submit.prevent="uploadMedicalFile"
                  enctype="multipart/form-data"
                >
                  <!-- File Selection
                       Workaround: hidden native input + PrimeVue Button trigger.
                       handleFileSelect(Event) signature is preserved unchanged. -->
                  <div class="form-group">
                    <label class="form-label">
                      <i class="pi pi-upload"></i> Chọn tệp:
                    </label>
                    <div class="file-choose-row">
                      <Button
                        type="button"
                        outlined
                        icon="pi pi-folder-open"
                        label="Chọn tệp"
                        class="file-choose-btn"
                        @click="() => (fileInput as HTMLInputElement)?.click()"
                      />
                      <span v-if="selectedFile" class="selected-file-name">
                        <i class="pi pi-file"></i> {{ selectedFile.name }}
                      </span>
                    </div>
                    <!-- Hidden native input — preserves handleFileSelect logic intact -->
                    <input
                      ref="fileInput"
                      type="file"
                      @change="handleFileSelect"
                      accept=".jpg,.jpeg,.png,.pdf,.doc,.docx,.dcm,.zip,.rar"
                      style="display: none"
                      required
                    />
                    <small class="form-text">
                      Hỗ trợ: JPG, PNG, PDF, DOC, DOCX, DICOM, ZIP, RAR (Max:
                      50MB)
                    </small>
                  </div>

                  <!-- Attachment Type — PrimeVue Select -->
                  <div class="form-group">
                    <label class="form-label">
                      <i class="pi pi-tag"></i> Loại tài liệu:
                    </label>
                    <Select
                      v-model="uploadForm.attachment_type"
                      :options="attachmentTypeOptions"
                      optionLabel="label"
                      optionValue="value"
                      placeholder="-- Chọn loại tài liệu --"
                      class="w-full"
                      required
                    />
                  </div>

                  <!-- Title — PrimeVue InputText -->
                  <div class="form-group">
                    <label class="form-label">
                      <i class="pi pi-pencil"></i> Tiêu đề:
                    </label>
                    <InputText
                      v-model="uploadForm.title"
                      placeholder="Nhập tiêu đề mô tả tài liệu..."
                      class="w-full"
                      required
                    />
                  </div>

                  <!-- Description — PrimeVue Textarea -->
                  <div class="form-group">
                    <div class="flex items-center gap-2 mb-1">
                      <label class="form-label mb-0">
                        <i class="pi pi-align-left"></i> Mô tả (tùy chọn):
                      </label>
                      <VoiceToText
                        v-model="uploadForm.description"
                        size="small"
                      />
                    </div>
                    <Textarea
                      v-model="uploadForm.description"
                      :rows="3"
                      placeholder="Mô tả chi tiết về tài liệu..."
                      class="w-full"
                      autoResize
                    />
                  </div>

                  <!-- Date Taken — PrimeVue DatePicker
                       Template-level string ↔ Date conversion.
                       uploadForm.date_taken (string "YYYY-MM-DD") is preserved in script. -->
                  <div class="form-group">
                    <label class="form-label">
                      <i class="pi pi-calendar"></i> Ngày thực hiện (tùy chọn):
                    </label>
                    <DatePicker
                      :modelValue="
                        uploadForm.date_taken
                          ? new Date(uploadForm.date_taken)
                          : null
                      "
                      @update:modelValue="
                        (d: any) => {
                          if (d instanceof Date) {
                            uploadForm.date_taken =
                              d.toISOString().split('T')[0] || '';
                          } else {
                            uploadForm.date_taken = '';
                          }
                        }
                      "
                      dateFormat="yy-mm-dd"
                      showButtonBar
                      class="w-full"
                      inputClass="w-full"
                    />
                  </div>

                  <!-- Physician Notes — PrimeVue Textarea -->
                  <div class="form-group">
                    <div class="flex items-center gap-2 mb-1">
                      <label class="form-label mb-0">
                        <i class="pi pi-user"></i> Ghi chú bác sĩ (tùy chọn):
                      </label>
                      <VoiceToText
                        v-model="uploadForm.physician_notes"
                        size="small"
                      />
                    </div>
                    <Textarea
                      v-model="uploadForm.physician_notes"
                      :rows="2"
                      placeholder="Ghi chú của bác sĩ về tài liệu..."
                      class="w-full"
                      autoResize
                    />
                  </div>

                  <!-- Confidential — PrimeVue Checkbox -->
                  <div class="form-group form-check">
                    <Checkbox
                      v-model="uploadForm.is_confidential"
                      inputId="is-confidential"
                      :binary="true"
                    />
                    <label for="is-confidential" class="form-check-label">
                      <i class="pi pi-lock"></i> Tài liệu bảo mật (chỉ giảng
                      viên xem được)
                    </label>
                  </div>

                  <!-- Upload Progress — ProgressBar not in approved list;
                       kept as styled div (original behaviour preserved) -->
                  <div v-if="uploadProgress > 0" class="upload-progress">
                    <div class="progress">
                      <div
                        class="progress-bar"
                        :style="{ width: uploadProgress + '%' }"
                        role="progressbar"
                      >
                        {{ Math.round(uploadProgress) }}%
                      </div>
                    </div>
                  </div>

                  <!-- Form Actions -->
                  <div class="form-actions">
                    <Button
                      type="submit"
                      :disabled="uploading"
                      :loading="uploading"
                      :label="uploading ? 'Đang tải lên...' : 'Tải lên'"
                      icon="pi pi-upload"
                      severity="success"
                    />
                    <Button
                      type="button"
                      @click="cancelUpload"
                      label="Hủy"
                      outlined
                      :disabled="uploading"
                    />
                  </div>
                </form>
              </div>
            </section>

            <!-- Legacy backward-compatibility sections -->
            <section
              v-if="!selectedCase.clinical_history && selectedCase.history"
            >
              <h3>Tiền sử (Cũ)</h3>
              <p>{{ selectedCase.history }}</p>
            </section>
            <section
              v-if="
                !selectedCase.physical_examination && selectedCase.examination
              "
            >
              <h3>Khám lâm sàng (Cũ)</h3>
              <p>{{ selectedCase.examination }}</p>
            </section>
            <section
              v-if="
                !selectedCase.detailed_investigations &&
                selectedCase.investigations
              "
            >
              <h3>Xét nghiệm (Cũ)</h3>
              <p>{{ selectedCase.investigations }}</p>
            </section>
            <section
              v-if="
                !selectedCase.diagnosis_management && selectedCase.diagnosis
              "
            >
              <h3>Chẩn đoán (Cũ)</h3>
              <p>{{ selectedCase.diagnosis }}</p>
            </section>
            <section
              v-if="
                !selectedCase.diagnosis_management && selectedCase.treatment
              "
            >
              <h3>Điều trị (Cũ)</h3>
              <p>{{ selectedCase.treatment }}</p>
            </section>
            <section
              v-if="
                !selectedCase.learning_outcomes &&
                selectedCase.learning_objectives
              "
            >
              <h3>Mục tiêu học tập (Cũ)</h3>
              <p>{{ selectedCase.learning_objectives }}</p>
            </section>

            <!-- Grading Section (Instructors Only)
                 Original had broken triple-nested duplicate <Button> tags.
                 Collapsed to correct single PrimeVue Button instances.
                 No JS handlers existed on these buttons — no logic changed. -->
            <section
              v-if="authStore.user?.role === 'instructor'"
              class="clinical-section grading-section"
            >
              <h3>📝 Chấm điểm và Đánh giá</h3>
              <div class="grading-form">
                <div class="grade-input-group">
                  <label>Điểm số (0-100):</label>
                  <InputNumber
                    :min="0"
                    :max="100"
                    placeholder="Nhập điểm"
                    class="grade-input-num"
                    showButtons
                  />
                </div>
                <div class="grade-input-group">
                  <label>Nhận xét:</label>
                  <Textarea
                    :rows="4"
                    placeholder="Nhập nhận xét đánh giá..."
                    class="grade-textarea w-full"
                    autoResize
                  />
                </div>
                <div class="grade-input-group">
                  <label>Điểm mạnh:</label>
                  <Textarea
                    :rows="3"
                    placeholder="Những điểm làm tốt..."
                    class="grade-textarea w-full"
                    autoResize
                  />
                </div>
                <div class="grade-input-group">
                  <label>Cần cải thiện:</label>
                  <Textarea
                    :rows="3"
                    placeholder="Những điểm cần cải thiện..."
                    class="grade-textarea w-full"
                    autoResize
                  />
                </div>
                <div class="grade-actions">
                  <Button icon="pi pi-save" label="Lưu đánh giá" />
                  <Button
                    icon="pi pi-check"
                    label="Hoàn thành chấm điểm"
                    severity="success"
                  />
                </div>
              </div>
            </section>

            <!-- Grade Display (Students Only) -->
            <section
              v-if="authStore.user?.role === 'student' && selectedCase.grade"
              class="clinical-section grade-display-section"
            >
              <h3>📊 Kết quả đánh giá</h3>
              <div class="grade-display">
                <div class="grade-score">
                  <span class="score-label">Điểm số:</span>
                  <span class="score-value"
                    >{{ selectedCase.grade.score }}/100</span
                  >
                  <span class="score-letter">
                    {{
                      selectedCase.grade.letter_grade ||
                      getLetterGrade(selectedCase.grade.score)
                    }}
                  </span>
                </div>
                <div
                  class="grade-feedback"
                  v-if="selectedCase.grade.evaluation_notes"
                >
                  <h4>Nhận xét của giảng viên:</h4>
                  <p>{{ selectedCase.grade.evaluation_notes }}</p>
                </div>
                <div class="grade-feedback" v-if="selectedCase.grade.strengths">
                  <h4>Điểm mạnh:</h4>
                  <p>{{ selectedCase.grade.strengths }}</p>
                </div>
                <div
                  class="grade-feedback"
                  v-if="selectedCase.grade.weaknesses"
                >
                  <h4>Cần cải thiện:</h4>
                  <p>{{ selectedCase.grade.weaknesses }}</p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </Dialog>

      <!-- Case Sharing Panel Modal -->
      <Dialog
        :visible="showSharingPanel && !!selectedCaseForSharing"
        :header="`🔗 Chia sẻ ca bệnh: ${selectedCaseForSharing?.title || ''}`"
        :modal="true"
        :closable="true"
        @update:visible="closeSharingPanel"
        class="w-full md:w-2/3"
      >
        <CaseSharingPanel
          v-if="selectedCaseForSharing"
          :case-id="selectedCaseForSharing.id"
        />
      </Dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useCasesStore } from "@/stores/cases";
import { useChoices } from "@/composables/useChoices";
import { requireRoles } from "@/composables/useAuthorize";
import { exportService } from "@/services/export.ts";
import { casesService } from "@/services/cases";
// PrimeVue components
import Button from "primevue/button";
import SplitButton from "primevue/splitbutton";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import SelectButton from "primevue/selectbutton";
import InputNumber from "primevue/inputnumber";
import DatePicker from "primevue/datepicker";
import Checkbox from "primevue/checkbox";
import Tag from "primevue/tag";
import Card from "primevue/card";
import Dialog from "primevue/dialog";
import Menu from "primevue/menu";
import Paginator from "primevue/paginator";
import CaseSharingPanel from "@/components/CaseSharingPanel.vue";
import CloneCaseDialog from "@/components/CloneCaseDialog.vue";
import VoiceToText from "@/components/VoiceToText.vue";
import SearchAutocomplete from "@/components/SearchAutocomplete.vue";

const router = useRouter();
const authStore = useAuthStore();
const casesStore = useCasesStore();
const { specialties, loading: choicesLoading } = useChoices();

const searchQuery = ref("");
const activeFilter = ref("all");
const specialtyFilter = ref("");
const dateSort = ref("newest");
const selectedCase = ref<Record<string, any> | null>(null);
const showExportMenu = ref<number | string | null>(null);
const exporting = ref(false);

// Collection filter for students (all, my-cases, saved)
const collectionFilter = ref<"all" | "my-cases" | "saved">("all");

// Options for SelectButton collection tabs
const collectionTabOptions = computed(() => [
  { label: `Tất cả (${cases.value.length})`, value: "all" },
  { label: `Hồ sơ của tôi (${myCasesCount.value})`, value: "my-cases" },
  { label: `Hồ sơ đã lưu (${savedCasesCount.value})`, value: "saved" },
]);

// Attachment type options for Select component
const attachmentTypeOptions = [
  { label: "📷 Ảnh chụp X-quang", value: "x_ray" },
  { label: "🧪 Phiếu xét nghiệm", value: "lab_report" },
  { label: "🔬 Chụp CT/Scanner", value: "ct_scan" },
  { label: "🧠 Chụp MRI", value: "mri_scan" },
  { label: "📡 Siêu âm", value: "ultrasound" },
  { label: "📸 Ảnh chụp chấn thương", value: "injury_photo" },
  { label: "⚕️ Ảnh phẫu thuật", value: "surgical_photo" },
  { label: "🔬 Tiêu bản bệnh học", value: "pathology_slide" },
  { label: "💊 Đơn thuốc", value: "prescription" },
  { label: "📋 Tóm tắt xuất viện", value: "discharge_summary" },
  { label: "💓 Dấu hiệu sinh tồn", value: "vital_signs" },
  { label: "❤️ Điện tâm đồ", value: "ekg_ecg" },
  { label: "🔍 Nội soi", value: "endoscopy" },
  { label: "🧬 Kết quả sinh thiết", value: "biopsy_report" },
  { label: "📜 Giấy chứng nhận y tế", value: "medical_certificate" },
  { label: "📄 Khác", value: "other" },
];

// Clone dialog state
const showCloneDialog = ref(false);
const cloneCaseId = ref<number | undefined>(undefined);

// Case sharing state
const showSharingPanel = ref(false);
const selectedCaseForSharing = ref<Record<string, any> | null>(null);

// Pagination state
const currentPage = ref(1);
const itemsPerPage = ref(10);

// Statistics state for accurate counts
const statistics = ref<{
  total_cases: number;
  by_status: { case_status: string; count: number }[];
} | null>(null);
const statsLoading = ref(false);
const trueTotalCases = ref<number | null>(null);

// Medical file upload state
const showUploadForm = ref(false);
const uploading = ref(false);
const uploadProgress = ref(0);
const selectedFile = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

const uploadForm = ref({
  attachment_type: "",
  title: "",
  description: "",
  date_taken: "",
  physician_notes: "",
  is_confidential: false,
});

// Role-based status tabs
const statusTabs = computed(() => {
  if (authStore.user?.role === "instructor") {
    return [
      { value: "all", label: "Tất cả hồ sơ" },
      { value: "submitted", label: "Chờ chấm / Đã chấm" },
    ];
  } else {
    return [
      { value: "all", label: "Tất cả hồ sơ" },
      { value: "draft", label: "Bản nháp" },
      { value: "submitted", label: "Đã nộp / Đã chấm" },
    ];
  }
});

const loading = computed(() => casesStore.loading);
const error = computed(() => casesStore.error);
const cases = computed(() => casesStore.cases);
const pagination = computed(() => casesStore.pagination);
const totalCases = computed(() => casesStore.pagination.count);

const myCasesCount = computed(() => {
  return cases.value.filter(
    (c) => !c.cloned_from && c.created_by_id === authStore.user?.id,
  ).length;
});

const savedCasesCount = computed(() => {
  return cases.value.filter((c) => c.cloned_from).length;
});

const currentCollectionCases = computed(() => {
  if (!isStudent.value) return cases.value;

  if (collectionFilter.value === "my-cases") {
    return cases.value.filter(
      (c) => !c.cloned_from && c.created_by_id === authStore.user?.id,
    );
  } else if (collectionFilter.value === "saved") {
    return cases.value.filter((c) => c.cloned_from);
  }
  return cases.value;
});

const filteredCases = computed(() => {
  let filtered = cases.value;

  // Teachers should NEVER see draft cases
  if (authStore.user?.role === "instructor") {
    filtered = filtered.filter((c) => c.case_status !== "draft");
  }

  // Filter by collection type (for students)
  if (isStudent.value && collectionFilter.value !== "all") {
    if (collectionFilter.value === "my-cases") {
      filtered = filtered.filter(
        (c) => !c.cloned_from && c.created_by_id === authStore.user?.id,
      );
    } else if (collectionFilter.value === "saved") {
      filtered = filtered.filter((c) => c.cloned_from);
    }
  }

  // Filter by status
  if (activeFilter.value !== "all") {
    if (activeFilter.value === "submitted") {
      if (authStore.user?.role === "instructor") {
        filtered = filtered.filter((c) => c.case_status === "submitted");
      } else {
        filtered = filtered.filter(
          (c) =>
            c.case_status === "submitted" ||
            c.case_status === "reviewed" ||
            c.case_status === "approved",
        );
      }
    } else {
      filtered = filtered.filter((c) => c.case_status === activeFilter.value);
    }
  }

  // Filter by specialty
  if (specialtyFilter.value) {
    filtered = filtered.filter((c) => c.specialty === specialtyFilter.value);
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (c) =>
        c.title.toLowerCase().includes(query) ||
        c.specialty.toLowerCase().includes(query) ||
        c.patient_name.toLowerCase().includes(query) ||
        (c.keywords && c.keywords.toLowerCase().includes(query)) ||
        (c.diagnosis && c.diagnosis.toLowerCase().includes(query)),
    );
  }

  // Sort by date
  if (dateSort.value) {
    filtered = [...filtered].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();

      if (dateSort.value === "newest") {
        return dateB - dateA;
      } else if (dateSort.value === "oldest") {
        return dateA - dateB;
      }
      return 0;
    });
  }

  return filtered;
});

const canViewConfidential = computed(() => {
  return (
    authStore.user &&
    (authStore.user.role === "instructor" || authStore.user.role === "admin")
  );
});

const isStudent = computed(() => {
  return authStore.user && authStore.user.role === "student";
});

const canUploadFiles = computed(() => {
  return (
    selectedCase.value &&
    (selectedCase.value.student_id === authStore.user?.id ||
      authStore.user?.role === "instructor" ||
      authStore.user?.role === "admin")
  );
});

async function loadStatistics() {
  statsLoading.value = true;
  try {
    const response = await casesService.getCaseSummaryStatistics();
    statistics.value = {
      total_cases: response.summary?.total_cases || 0,
      by_status: response.distributions?.by_status || [],
    };
  } catch (err) {
    console.error("Failed to load statistics:", err);
  } finally {
    statsLoading.value = false;
  }
}

async function loadCases(page: number = 1) {
  try {
    const params: any = { page };

    if (activeFilter.value !== "all") {
      if (
        activeFilter.value === "submitted" &&
        authStore.user?.role === "instructor"
      ) {
        params.case_status = "submitted";
      } else if (activeFilter.value !== "submitted") {
        params.case_status = activeFilter.value;
      }
    }

    if (specialtyFilter.value) {
      params.specialty = specialtyFilter.value;
    }

    if (searchQuery.value) {
      params.search = searchQuery.value;
    }

    await casesStore.fetchCases(params);
    currentPage.value = page;
    if (
      activeFilter.value === "all" &&
      !specialtyFilter.value &&
      !searchQuery.value
    ) {
      trueTotalCases.value = casesStore.pagination.count;
    }
    await loadStatistics();
  } catch (err) {
    console.error("Failed to load cases:", err);
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= pagination.value.total_pages) {
    loadCases(page);
  }
}

function onPageChange(event: { page: number; rows: number }) {
  // Check if rows per page changed (rows dropdown was used)
  const rowsChanged = event.rows !== itemsPerPage.value;
  itemsPerPage.value = event.rows;

  // If rows per page changed, always reset to page 1
  if (rowsChanged) {
    currentPage.value = 1;
    loadCases(1);
    return;
  }

  // Otherwise, handle normal page navigation
  const page = event.page + 1; // Convert 0-based to 1-based
  const maxPages = pagination.value.total_pages || 1;

  // Validate page is within bounds
  if (page < 1 || page > maxPages) {
    currentPage.value = 1;
    return;
  }

  currentPage.value = page;
  loadCases(page);
}

function setActiveFilter(filter: string) {
  if (activeFilter.value !== filter) {
    activeFilter.value = filter;
    loadCases(1);
  }
}

loadCases(1);

function applyFilters() {
  // Filters are applied reactively through computed property
}

function toggleExportMenu(caseId: string) {
  showExportMenu.value = showExportMenu.value === caseId ? null : caseId;
}

async function exportCase(caseItem: any, format: string) {
  if (exporting.value) return;

  exporting.value = true;
  showExportMenu.value = null;

  try {
    if (typeof (exportService as any).exportCase === "function") {
      await (exportService as any).exportCase(
        caseItem.id.toString(),
        format,
        caseItem.title,
      );
    } else if (typeof (exportService as any).quickExport === "function") {
      await (exportService as any).quickExport(
        caseItem.id,
        format === "powerpoint" ? "ppt" : format,
      );
    } else {
      throw new Error("No export function available");
    }
    alert(
      `Đã xuất hồ sơ "${caseItem.title}" sang ${format.toUpperCase()} thành công!`,
    );
  } catch (error) {
    console.error("Export failed:", error);
    alert("Có lỗi xảy ra khi xuất file. Vui lòng thử lại.");
  } finally {
    exporting.value = false;
  }
}

async function viewCase(case_: any) {
  try {
    await casesStore.fetchCase(case_.id);
    selectedCase.value = casesStore.currentCase;

    console.log("=== CASE DATA DEBUG ===");
    console.log("Full case:", selectedCase.value);
    console.log(
      "Has clinical_history?",
      !!selectedCase.value?.clinical_history,
    );
    console.log("clinical_history:", selectedCase.value?.clinical_history);
    console.log(
      "Has physical_examination?",
      !!selectedCase.value?.physical_examination,
    );
    console.log(
      "physical_examination:",
      selectedCase.value?.physical_examination,
    );
    console.log(
      "Has detailed_investigations?",
      !!selectedCase.value?.detailed_investigations,
    );
    console.log(
      "Has diagnosis_management?",
      !!selectedCase.value?.diagnosis_management,
    );
    console.log(
      "Has learning_outcomes?",
      !!selectedCase.value?.learning_outcomes,
    );
  } catch (error) {
    console.error("Failed to load case details:", error);
    selectedCase.value = case_;
  }
}

function openSharingPanel(case_: any) {
  selectedCaseForSharing.value = case_;
  showSharingPanel.value = true;
}

function closeSharingPanel() {
  showSharingPanel.value = false;
  selectedCaseForSharing.value = null;
}

function openCloneDialog(case_: any) {
  cloneCaseId.value = case_.id;
  showCloneDialog.value = true;
}

function handleCloneSuccess(clonedCase: any) {
  loadCases();
  collectionFilter.value = "saved";
  alert(
    `Đã lưu hồ sơ "${clonedCase.title}" vào bộ sưu tập của bạn thành công!`,
  );
}

function isOwner(case_: any): boolean {
  return (
    case_.student === authStore.user?.id ||
    authStore.user?.role === "instructor"
  );
}

function closeModal() {
  selectedCase.value = null;
  casesStore.clearCurrentCase();
}

async function logout() {
  await authStore.logout();
  router.push("/");
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("vi-VN");
}

function getLetterGrade(score: number) {
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  if (score >= 60) return "D";
  return "F";
}

function getStatusLabel(status: string) {
  const statusMap: Record<string, string> = {
    draft: "Bản nháp",
    submitted: "Đã nộp",
    reviewed: "Đã duyệt",
    approved: "Đã phê duyệt",
  };
  return statusMap[status] || status;
}

function getStatusCount(status: string) {
  if (isStudent.value && collectionFilter.value !== "all") {
    const baseCases = currentCollectionCases.value;

    if (status === "all") {
      if (trueTotalCases.value !== null) {
        return trueTotalCases.value;
      }
      if (statistics.value?.total_cases) {
        return statistics.value.total_cases;
      }
      return pagination.value.count || cases.value.length;
    }
    return baseCases.filter((case_) => case_.case_status === status).length;
  }

  if (searchQuery.value.trim()) {
    const searchResults = cases.value;

    if (status === "all") {
      return searchResults.length;
    }

    if (status === "submitted") {
      if (authStore.user?.role === "instructor") {
        return searchResults.filter(
          (case_) => case_.case_status === "submitted",
        ).length;
      } else {
        return searchResults.filter(
          (case_) =>
            case_.case_status === "submitted" ||
            case_.case_status === "reviewed" ||
            case_.case_status === "approved",
        ).length;
      }
    }

    return searchResults.filter((case_) => case_.case_status === status).length;
  }

  if (status === "all") {
    if (statistics.value?.total_cases) {
      return statistics.value.total_cases;
    }
    return pagination.value.count || cases.value.length;
  }

  if (statistics.value) {
    if (status === "submitted") {
      const byStatus = statistics.value.by_status;
      if (authStore.user?.role === "instructor") {
        return byStatus.find((s) => s.case_status === "submitted")?.count || 0;
      } else {
        const submittedCount =
          byStatus.find((s) => s.case_status === "submitted")?.count || 0;
        const reviewedCount =
          byStatus.find((s) => s.case_status === "reviewed")?.count || 0;
        const approvedCount =
          byStatus.find((s) => s.case_status === "approved")?.count || 0;
        return submittedCount + reviewedCount + approvedCount;
      }
    }
    const statusItem = statistics.value.by_status.find(
      (s) => s.case_status === status,
    );
    return statusItem?.count || 0;
  }

  const baseCases = cases.value;
  if (status === "submitted") {
    if (authStore.user?.role === "instructor") {
      return baseCases.filter((case_) => case_.case_status === "submitted")
        .length;
    }
    return baseCases.filter(
      (case_) =>
        case_.case_status === "submitted" ||
        case_.case_status === "reviewed" ||
        case_.case_status === "approved",
    ).length;
  }
  return baseCases.filter((case_) => case_.case_status === status).length;
}

function getAttachmentIcon(attachment: any) {
  const iconMap: Record<string, string> = {
    x_ray: "fas fa-x-ray",
    lab_report: "fas fa-vial",
    ct_scan: "fas fa-lungs",
    mri_scan: "fas fa-brain",
    ultrasound: "fas fa-heartbeat",
    injury_photo: "fas fa-camera-medical",
    surgical_photo: "fas fa-scalpel",
    pathology_slide: "fas fa-microscope",
    prescription: "fas fa-prescription",
    discharge_summary: "fas fa-file-medical-alt",
    vital_signs: "fas fa-chart-line",
    ekg_ecg: "fas fa-heartbeat",
    endoscopy: "fas fa-eye",
    biopsy_report: "fas fa-dna",
    medical_certificate: "fas fa-certificate",
    other: "fas fa-file-medical",
  };
  return iconMap[attachment.attachment_type] || "fas fa-file-medical";
}

async function downloadAttachment(attachment: any) {
  if (attachment.is_confidential && !canViewConfidential.value) {
    alert("Bạn không có quyền xem tài liệu bảo mật này.");
    return;
  }

  try {
    const response = await casesService.downloadAttachment(attachment.id);

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute(
      "download",
      attachment.original_filename ||
        `${attachment.title}.${attachment.file_extension}`,
    );
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error downloading attachment:", error);
    alert("Lỗi khi tải xuống tệp");
  }
}

function handleFileSelect(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    selectedFile.value = file;

    if (!uploadForm.value.title) {
      uploadForm.value.title = file.name.split(".")[0] ?? "";
    }

    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
      alert("Tệp quá lớn! Vui lòng chọn tệp nhỏ hơn 50MB.");
      resetFileInput();
      return;
    }
  }
}

async function uploadMedicalFile() {
  if (!selectedFile.value || !selectedCase.value) {
    alert("Vui lòng chọn tệp và đảm bảo đã chọn ca bệnh!");
    return;
  }

  uploading.value = true;
  uploadProgress.value = 0;

  try {
    const formData = new FormData();
    formData.append("file", selectedFile.value);
    formData.append("attachment_type", uploadForm.value.attachment_type);
    formData.append("title", uploadForm.value.title);
    formData.append("description", uploadForm.value.description || "");
    formData.append("physician_notes", uploadForm.value.physician_notes || "");
    formData.append("is_confidential", `${uploadForm.value.is_confidential}`);

    if (uploadForm.value.date_taken) {
      formData.append("date_taken", uploadForm.value.date_taken);
    }

    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += Math.random() * 20;
      }
    }, 200);

    const response = await casesService.uploadAttachment(
      selectedCase.value.id,
      formData,
    );

    clearInterval(progressInterval);
    uploadProgress.value = 100;

    if (!selectedCase.value.medical_attachments) {
      selectedCase.value.medical_attachments = [];
    }
    selectedCase.value.medical_attachments.push(response);

    resetUploadForm();
    alert("Tải lên thành công!");
  } catch (error: any) {
    console.error("Upload error:", error);
    alert(
      "Lỗi khi tải lên tệp: " +
        (error.response?.data?.message || error.message),
    );
  } finally {
    uploading.value = false;
    uploadProgress.value = 0;
  }
}

function cancelUpload() {
  resetUploadForm();
}

function resetUploadForm() {
  showUploadForm.value = false;
  uploading.value = false;
  uploadProgress.value = 0;
  selectedFile.value = null;

  uploadForm.value = {
    attachment_type: "",
    title: "",
    description: "",
    date_taken: "",
    physician_notes: "",
    is_confidential: false,
  };

  resetFileInput();
}

function resetFileInput() {
  if (fileInput.value) {
    fileInput.value.value = "";
  }
  selectedFile.value = null;
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  requireRoles(["student", "instructor"]);

  loadCases();
});
</script>

<style scoped>
/* ── Page Header ───────────────────────────────────────── */
.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  border-bottom: 1px solid var(--border);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  color: var(--foreground);
  font-size: 1.875rem;
  font-weight: 700;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* ── Filters Section ───────────────────────────────────── */
.filters-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--card);
  border-radius: 12px;
  box-shadow: 0 1px 3px var(--shadow-grey);
  border: 1px solid var(--border);
}

.search-and-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: stretch;
}

.search-container {
  position: relative;
  flex: 1;
  min-width: 200px;
}

.filter-options {
  display: flex;
  gap: 1rem;
}

:deep(.specialty-select.p-select),
:deep(.sort-select.p-select) {
  min-height: 2.75rem;
  border-radius: 10px;
  font-size: 0.9rem;
}

:deep(.specialty-select.p-select) {
  min-width: 200px;
}
:deep(.sort-select.p-select) {
  min-width: 130px;
}

/* ── Collection Tabs (SelectButton) ────────────────────── */
/*
  Replaces three manually-toggled Buttons.
  Active item: dark background + light text (same visual language as PublicFeed).
*/
.collection-tabs {
  margin-bottom: 1.5rem;
}

:deep(.collection-select-btn.p-selectbutton) {
  background: transparent;
  border: none;
  gap: 0.5rem;
  display: flex;
  flex-wrap: wrap;
}

:deep(.collection-select-btn .p-togglebutton) {
  padding: 0.6rem 1.1rem;
  border-radius: 25px !important;
  background: var(--secondary) !important;
  border: 2px solid var(--border) !important;
  color: var(--muted-foreground) !important;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

:deep(.collection-select-btn .p-togglebutton:hover) {
  background: var(--accent) !important;
  border-color: var(--foreground) !important;
  color: var(--foreground) !important;
}

:deep(.collection-select-btn .p-togglebutton.p-togglebutton-checked) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border-color: transparent !important;
  color: white !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

:deep(
  .collection-select-btn .p-togglebutton.p-togglebutton-checked .p-button-label
) {
  color: white !important;
}

/* ── Stats Grid ────────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--card);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px var(--shadow-grey);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s;
  cursor: pointer;
  border: 2px solid transparent;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px var(--shadow-grey);
}

.stat-card.stat-active {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--shadow-blue-hover);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-primary {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}
.stat-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}
.stat-warning {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}
.stat-info {
  background: linear-gradient(135deg, #f89249 0%, #f1b780 100%);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--foreground);
  line-height: 1;
}

.stat-label {
  color: var(--muted-foreground);
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* ── Loading / Error ───────────────────────────────────── */
.loading {
  text-align: center;
  padding: 3rem;
  color: var(--muted-foreground);
}

.error {
  text-align: center;
  padding: 2rem;
  margin: 2rem auto;
  max-width: 500px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #991b1b;
}

.error p {
  margin: 0 0 1.5rem 0;
}

/* ── Cases Grid ────────────────────────────────────────── */
.cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

/* ── Case Card (PrimeVue Card) ─────────────────────────── */
/*
  Border-radius fix:
    PrimeVue Card's nested elements (body, title, content, footer) have their own
    border-radius that creates acute corner stacks. Solution: overflow:hidden on
    the card wrapper + zero radius on all internal elements so they stay within
    the card's clipping boundary.
*/
:deep(.case-card-prime.p-card) {
  border: 1px solid var(--border);
  border-radius: 12px !important;
  overflow: hidden; /* clips all internal content to card borders */
  background: var(--card);
  box-shadow: 0 2px 4px var(--shadow-grey);
  transition: all 0.2s ease;
  position: relative;
}

:deep(.case-card-prime.p-card .p-card-body) {
  padding: 0;
  border-radius: 0 !important; /* no internal radius; clipped by card overflow */
}

:deep(.case-card-prime.p-card .p-card-title) {
  padding: 1.25rem 1.5rem 0;
  margin-bottom: 0;
  border-radius: 0 !important;
}

:deep(.case-card-prime.p-card .p-card-content) {
  padding: 0.75rem 1.5rem;
  border-radius: 0 !important;
}

:deep(.case-card-prime.p-card .p-card-footer) {
  padding: 0.75rem 1.5rem 1.25rem;
  border-top: 1px solid var(--border);
  border-radius: 0 !important;
}

:deep(.case-card-prime.p-card:hover) {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px var(--shadow-grey);
  border-color: var(--primary);
}

/* Saved case: green left accent */
:deep(.case-card-prime.saved-case.p-card) {
  border-left: 4px solid #10b981;
  background: linear-gradient(
    135deg,
    rgba(16, 185, 129, 0.04) 0%,
    var(--card) 100%
  );
}

.case-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.case-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--foreground);
  line-height: 1.4;
  flex: 1;
}

.header-badges {
  display: flex;
  gap: 0.4rem;
  align-items: center;
  flex-wrap: wrap;
  flex-shrink: 0;
}

/* ── Status Tags ───────────────────────────────────────── */
/*
  PrimeVue Tag is used for all status / classification badges.
  globals.css .p-tag rules provide the default styling.
  Status-specific colour overrides are below.
*/
:deep(.status-tag.p-tag.draft) {
  background-color: #fef3c7 !important;
  color: #92400e !important;
}

:deep(.status-tag.p-tag.submitted) {
  background-color: #dbeafe !important;
  color: #1e40af !important;
}

:deep(.status-tag.p-tag.reviewed) {
  background-color: #d1fae5 !important;
  color: #065f46 !important;
}

:deep(.status-tag.p-tag.approved) {
  background-color: #dcfce7 !important;
  color: #14532d !important;
}

:deep(.template-tag.p-tag) {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
  color: white !important;
  border-radius: 12px !important;
  font-size: 0.72rem;
  font-weight: 600;
}

:deep(.saved-tag.p-tag) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
  color: white !important;
  border-radius: 12px !important;
  font-size: 0.72rem;
  font-weight: 600;
}

.cloned-from-info {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.75rem;
  font-size: 0.85rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: center;
}

.cloned-label {
  color: #166534;
  font-weight: 600;
}
.cloned-title {
  color: #15803d;
  font-weight: 500;
}
.cloned-author {
  color: #16a34a;
  font-style: italic;
}

.case-meta p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: var(--muted-foreground);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.case-meta strong {
  color: var(--foreground);
}

.case-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
}

/* SplitButton export — override default border-radius for modern look */
:deep(.export-split-btn.p-splitbutton .p-button) {
  border-radius: 8px 0 0 8px !important;
}

:deep(.export-split-btn.p-splitbutton .p-splitbutton-dropdown) {
  border-radius: 0 8px 8px 0 !important;
}

/* ── Empty State ───────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--muted-foreground);
}

/* ── Pagination ────────────────────────────────────────── */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 1.5rem 0;
}

:deep(.cases-paginator) {
  background: transparent !important;
  border: none !important;
}

:deep(.cases-paginator .p-paginator-page.p-highlight) {
  background: var(--primary) !important;
  color: var(--primary-foreground) !important;
  border-color: var(--primary) !important;
  border-radius: 8px !important;
}

:deep(.cases-paginator .p-paginator-page),
:deep(.cases-paginator .p-paginator-prev),
:deep(.cases-paginator .p-paginator-next),
:deep(.cases-paginator .p-paginator-first),
:deep(.cases-paginator .p-paginator-last) {
  border-radius: 8px !important;
  color: var(--foreground) !important;
  min-width: 2.5rem !important;
  height: 2.5rem !important;
}

:deep(.cases-paginator .p-paginator-page:hover),
:deep(.cases-paginator .p-paginator-prev:hover),
:deep(.cases-paginator .p-paginator-next:hover) {
  background: var(--secondary) !important;
  border-color: var(--primary) !important;
}

/* ── Case Detail Dialog ────────────────────────────────── */
:deep(.case-detail-dialog .p-dialog) {
  border-radius: 16px !important;
  overflow: hidden;
}

:deep(.case-detail-dialog .p-dialog-header) {
  border-radius: 16px 16px 0 0 !important;
}

.modal-content {
  padding: 1.5rem;
  overflow-y: auto;
}

.loading-modal {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  color: var(--muted-foreground);
  font-size: 1.1rem;
}

/* ── Clinical Sections ─────────────────────────────────── */
.patient-info {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 10px;
  border-left: 4px solid #3b82f6;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.info-item {
  background: var(--card);
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--border);
  font-size: 0.9rem;
  color: var(--foreground);
}

.clinical-section {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.clinical-section h3 {
  color: var(--foreground);
  font-size: 1.125rem;
  margin: 0 0 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.clinical-subsection {
  margin-bottom: 1.25rem;
  padding: 0.875rem 1rem;
  background: var(--secondary);
  border-radius: 8px;
  border-left: 3px solid var(--muted);
}

.clinical-subsection:last-child {
  margin-bottom: 0;
}

.clinical-subsection h4 {
  margin: 0 0 0.5rem;
  color: var(--foreground);
  font-size: 0.9rem;
  font-weight: 600;
}

.clinical-subsection p {
  margin: 0;
  color: var(--muted-foreground);
  line-height: 1.6;
  font-size: 0.9rem;
}

.formatted-text {
  white-space: pre-line;
  word-wrap: break-word;
}

/* ── Attachments ───────────────────────────────────────── */
.attachments-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
}

.attachment-item {
  background: var(--secondary);
  border: 2px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  transition: all 0.2s ease;
  position: relative;
}

.attachment-item:hover {
  border-color: var(--primary);
  box-shadow: 0 4px 12px var(--shadow-blue-hover);
}

.attachment-item.confidential {
  border-color: var(--destructive);
  background: #fef2f2;
}

.attachment-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.attachment-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
}

.attachment-item.confidential .attachment-icon {
  background: var(--destructive);
}

.attachment-info {
  flex: 1;
  min-width: 0;
}

.attachment-title {
  margin: 0 0 0.25rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--foreground);
  word-wrap: break-word;
}

.attachment-type {
  margin: 0 0 0.5rem;
  font-size: 0.825rem;
  color: var(--muted-foreground);
  font-weight: 500;
}

.attachment-meta {
  margin: 0;
  font-size: 0.75rem;
  color: var(--muted-foreground);
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.attachment-actions {
  flex-shrink: 0;
}

/* Download button override — PrimeVue Button rounded */
:deep(.download-btn-prime.p-button) {
  width: 36px !important;
  height: 36px !important;
  padding: 0 !important;
}

.attachment-description,
.attachment-notes {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: var(--card);
  border-radius: 6px;
  border: 1px solid var(--border);
}

.attachment-description p,
.attachment-notes p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--muted-foreground);
  line-height: 1.5;
}

.confidential-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: var(--destructive);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* ── Upload Form ───────────────────────────────────────── */
.upload-section {
  border-left: 4px solid #16a34a;
}

.upload-toggle-btn {
  margin-bottom: 0;
}

.upload-form {
  margin-top: 1rem;
  padding: 1.5rem;
  background: var(--secondary);
  border: 2px dashed var(--border);
  border-radius: 10px;
  transition: border-color 0.2s ease;
}

.upload-form:hover {
  border-color: #16a34a;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--foreground);
  font-size: 0.875rem;
}

.form-label.mb-0 {
  margin-bottom: 0;
}

.form-text {
  display: block;
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: var(--muted-foreground);
}

/* File choose row */
.file-choose-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 0.375rem;
}

.selected-file-name {
  font-size: 0.875rem;
  color: var(--foreground);
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.form-check {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  margin-bottom: 1rem;
}

.form-check-label {
  font-size: 0.875rem;
  color: var(--foreground);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  cursor: pointer;
}

/* Upload progress bar — ProgressBar not in approved list; keep styled div */
.upload-progress {
  margin: 1rem 0;
}

.progress {
  width: 100%;
  height: 1rem;
  background: var(--muted);
  border-radius: 0.5rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #16a34a, #22c55e);
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

/* PrimeVue Textarea / InputText / Select / InputNumber full-width */
:deep(.w-full.p-inputtext),
:deep(.w-full.p-textarea),
:deep(.w-full.p-select),
:deep(.w-full.p-inputnumber) {
  width: 100%;
}

/* ── Grading Section ───────────────────────────────────── */
.grading-section {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
}

.grading-form {
  background: var(--card);
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid var(--border);
}

.grade-input-group {
  margin-bottom: 1.25rem;
}

.grade-input-group label {
  display: block;
  font-weight: 600;
  color: var(--foreground);
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

:deep(.grade-input-num.p-inputnumber) {
  width: 160px;
}

:deep(.grade-textarea.p-textarea) {
  resize: vertical;
  font-size: 0.875rem;
  font-family: inherit;
}

.grade-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

/* ── Grade Display Section ─────────────────────────────── */
.grade-display-section {
  background: #dbeafe;
  border-left: 4px solid #3b82f6;
}

.grade-display {
  background: var(--card);
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid var(--border);
}

.grade-score {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  border-radius: 10px;
  margin-bottom: 1.5rem;
}

.score-label {
  font-size: 1rem;
  font-weight: 500;
}
.score-value {
  font-size: 2.5rem;
  font-weight: 700;
}

.score-letter {
  font-size: 2rem;
  font-weight: 700;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
}

.grade-feedback {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--secondary);
  border-radius: 8px;
  border-left: 3px solid #3b82f6;
}

.grade-feedback h4 {
  color: #1e40af;
  font-size: 0.9rem;
  font-weight: 600;
  margin: 0 0 0.75rem;
}

.grade-feedback p {
  color: var(--foreground);
  line-height: 1.6;
  margin: 0;
}

/* ── Responsive ────────────────────────────────────────── */
@media (max-width: 768px) {
  .search-and-filters {
    flex-direction: column;
  }
  .filter-options {
    width: 100%;
    flex-direction: column;
  }
  :deep(.specialty-select.p-select),
  :deep(.sort-select.p-select) {
    width: 100%;
  }
  .attachments-grid {
    grid-template-columns: 1fr;
  }
  .attachment-header {
    flex-direction: column;
    align-items: stretch;
  }
  .form-actions {
    flex-direction: column;
  }
}
</style>
