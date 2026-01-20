<template>
  <div class="cases-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 v-if="isStudent">Hồ sơ Bệnh án Lâm sàng</h1>
        <h1 v-else-if="authStore.user?.role === 'instructor'">Chấm điểm Bệnh án</h1>
        <h1 v-else>Quản lý Bệnh án</h1>
        <div class="header-actions">
          <router-link v-if="isStudent" to="/cases/create" class="btn btn-primary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="16" />
              <line x1="8" y1="12" x2="16" y2="12" />
            </svg>
            Tạo hồ sơ mới
          </router-link>
          <router-link v-if="authStore.user?.role === 'instructor'" to="/cases/create" class="btn btn-secondary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="16" />
              <line x1="8" y1="12" x2="16" y2="12" />
            </svg>
            Tạo hồ sơ mẫu
          </router-link>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="search-and-filters">
        <div class="search-container">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            class="search-icon">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input v-model="searchQuery" @input="handleSearch" type="text"
            placeholder="Tìm kiếm hồ sơ bệnh án theo tên, chuyên khoa, bệnh nhân..." class="search-input" />
        </div>

        <div class="filter-options">
          <select v-model="specialtyFilter" @change="applyFilters" class="filter-select" :disabled="choicesLoading">
            <option value="">{{ choicesLoading ? 'Đang tải...' : 'Tất cả chuyên khoa' }}</option>
            <option v-for="s in specialties" :key="s.id" :value="s.name">
              {{ s.name }}
            </option>
          </select>

          <select v-model="dateSort" class="filter-select">
            <option selected value="newest">Mới nhất</option>
            <option value="oldest">Cũ nhất</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Collection Category Tabs (Students only) -->
    <div v-if="isStudent" class="collection-tabs">
      <button class="collection-tab" :class="{ active: collectionFilter === 'all' }" @click="collectionFilter = 'all'">
        📁 Tất cả ({{ cases.length }})
      </button>
      <button class="collection-tab" :class="{ active: collectionFilter === 'my-cases' }"
        @click="collectionFilter = 'my-cases'">
        ✏️ Hồ sơ của tôi ({{ myCasesCount }})
      </button>
      <button class="collection-tab" :class="{ active: collectionFilter === 'saved' }"
        @click="collectionFilter = 'saved'">
        📥 Hồ sơ đã lưu ({{ savedCasesCount }})
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card" @click="setActiveFilter('all')" :class="{ 'stat-active': activeFilter === 'all' }">
        <div class="stat-icon stat-primary">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14,2 14,8 20,8" />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ getStatusCount('all') }}</div>
          <div class="stat-label">Tổng số hồ sơ</div>
        </div>
      </div>

      <div class="stat-card" v-if="isStudent" @click="setActiveFilter('draft')"
        :class="{ 'stat-active': activeFilter === 'draft' }">
        <div class="stat-icon stat-info">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
            <polyline points="14,2 14,8 20,8" />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ getStatusCount('draft') }}</div>
          <div class="stat-label">Bản nháp</div>
        </div>
      </div>

      <div class="stat-card" @click="setActiveFilter('submitted')"
        :class="{ 'stat-active': activeFilter === 'submitted' }">
        <div class="stat-icon stat-warning">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22,4 12,14.01 9,11.01" />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ getStatusCount('submitted') }}</div>
          <div class="stat-label" v-if="authStore.user?.role === 'instructor'">Chưa Chấm</div>
          <div class="stat-label" v-else>Đã nộp</div>
        </div>
      </div>
    </div>



    <main class="cases-main">
      <div class="container">
        <div class="loading" v-if="loading">
          <p>Đang tải hồ sơ bệnh án...</p>
        </div>

        <div class="error" v-if="error">
          <p>{{ error }}</p>
          <button @click="() => loadCases(1)" class="btn btn-primary">Thử lại</button>
        </div>



        <div class="cases-grid" v-if="!loading && !error">
          <div v-if="filteredCases.length === 0" class="empty-state">
            <p>Không tìm thấy hồ sơ bệnh án nào phù hợp với tiêu chí tìm kiếm.</p>
            <p v-if="cases.length > 0">Có {{ cases.length }} hồ sơ trong cơ sở dữ liệu nhưng không khớp với bộ lọc hiện
              tại.</p>
          </div>
          <div v-for="case_ in filteredCases" :key="case_.id" class="case-card"
            :class="{ 'saved-case': case_.cloned_from }">
            <div class="case-header">
              <h3>{{ case_.title }}</h3>
              <div class="header-badges">
                <!-- Instructor Template Badge -->
                <span v-if="case_.created_by_role === 'instructor' && !case_.cloned_from" class="template-badge" title="Hồ sơ mẫu từ giảng viên">
                  📚 Hồ sơ mẫu
                </span>
                <!-- Saved/Cloned Case Badge -->
                <span v-if="case_.cloned_from" class="saved-badge" title="Hồ sơ đã lưu từ giảng viên">
                  📥 Đã lưu
                </span>
                <span :class="['status-badge', case_.case_status]">
                  {{ getStatusLabel(case_.case_status) }}
                </span>
              </div>
            </div>

            <!-- Original Author Info for Cloned Cases -->
            <div v-if="case_.cloned_from" class="cloned-from-info">
              <span class="cloned-label">📚 Nguồn gốc:</span>
              <span class="cloned-title">{{ case_.cloned_from_title }}</span>
              <span v-if="case_.cloned_from_instructor_name" class="cloned-author">
                (bởi {{ case_.cloned_from_instructor_name }})
              </span>
            </div>

            <div class="case-meta">
              <p><strong>Bệnh nhân:</strong> {{ case_.patient_name }}</p>
              <p><strong>Tuổi:</strong> {{ case_.patient_age }}</p>
              <p><strong>Chuyên khoa:</strong> {{ case_.specialty }}</p>
              <p><strong>Ngày tạo:</strong> {{ formatDate(case_.created_at) }}</p>
            </div>

            <div class="case-actions">
              <button @click="router.push(`/cases/${case_.id}`)" class="btn btn-primary btn-sm">
                Xem chi tiết
              </button>
              <!-- Save to Collection Button for Template Cases (not cloned yet, not owner) -->
              <button v-if="case_.created_by_role === 'instructor' && !isOwner(case_) && !case_.cloned_from"
                @click="openCloneDialog(case_)" class="btn btn-success btn-sm" title="Lưu vào bộ sưu tập của bạn">
                📥 Lưu
              </button>
              <!-- Case Sharing Button for Instructors -->
              <button v-if="authStore.user?.role === 'instructor'" @click="openSharingPanel(case_)"
                class="btn btn-secondary btn-sm" title="Chia sẻ ca bệnh">
                🔗 Chia sẻ
              </button>
              <div class="export-dropdown">
                <button @click="toggleExportMenu(case_.id)" class="btn btn-outline btn-sm">
                  📄 Xuất file
                </button>
                <div v-if="showExportMenu === case_.id" class="export-menu">
                  <button @click="exportCase(case_, 'pdf')" class="export-option">PDF</button>
                  <button @click="exportCase(case_, 'word')" class="export-option">Word</button>
                  <button @click="exportCase(case_, 'powerpoint')" class="export-option">PowerPoint</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="empty-state" v-if="!loading && !error && filteredCases.length === 0">
          <h3>Không tìm thấy hồ sơ bệnh án</h3>
          <p>{{ searchQuery
            ? 'Thử điều chỉnh từ khóa tìm kiếm'
            : 'Không có hồ sơ bệnh án nào phù hợp với bộ lọc hiện tại' }}</p>
        </div>

        <!-- Pagination -->
        <div v-if="!loading && !error && pagination.total_pages > 1" class="pagination">
          <button class="pagination-btn" :disabled="currentPage === 1" @click="goToPage(1)" title="Trang đầu">
            «
          </button>
          <button class="pagination-btn" :disabled="!pagination.previous" @click="goToPage(currentPage - 1)"
            title="Trang trước">
            ‹
          </button>

          <template v-for="page in paginationPages" :key="page">
            <span v-if="page === '...'" class="pagination-ellipsis">...</span>
            <button v-else class="pagination-btn" :class="{ active: currentPage === page }"
              @click="goToPage(page as number)">
              {{ page }}
            </button>
          </template>

          <button class="pagination-btn" :disabled="!pagination.next" @click="goToPage(currentPage + 1)"
            title="Trang sau">
            ›
          </button>
          <button class="pagination-btn" :disabled="currentPage === pagination.total_pages"
            @click="goToPage(pagination.total_pages)" title="Trang cuối">
            »
          </button>

          <span class="pagination-info">
            Trang {{ currentPage }} / {{ pagination.total_pages }} ({{ totalCases }} hồ sơ)
          </span>
        </div>
      </div>
    </main>

    <!-- Clone Case Dialog -->
    <CloneCaseDialog :isOpen="showCloneDialog" :caseId="Number(cloneCaseId)" @close="showCloneDialog = false"
      @success="handleCloneSuccess" />

    <!-- Case Detail Modal -->
    <div v-if="selectedCase || loading" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedCase?.title || 'Đang tải...' }}</h2>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>

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
                  <strong>Tên bệnh nhân:</strong> {{ selectedCase.patient_name }}
                </div>
                <div class="info-item">
                  <strong>Tuổi:</strong> {{ selectedCase.patient_age }}
                </div>
                <div class="info-item">
                  <strong>Giới tính:</strong> {{ selectedCase.patient_gender === 'male' ? 'Nam' : 'Nữ' }}
                </div>
                <div class="info-item">
                  <strong>Số hồ sơ:</strong> {{ selectedCase.medical_record_number }}
                </div>
                <div class="info-item">
                  <strong>Chuyên khoa:</strong> {{ selectedCase.specialty }}
                </div>
                <div class="info-item" v-if="selectedCase.admission_date">
                  <strong>Ngày nhập viện:</strong> {{ formatDate(selectedCase.admission_date) }}
                </div>
              </div>
            </section>

            <!-- Clinical History Section -->
            <section v-if="selectedCase.clinical_history" class="clinical-section">
              <h3>📋 Tiền sử lâm sàng</h3>
              <div class="clinical-subsection">
                <h4>Lý do khám</h4>
                <p>{{ selectedCase.clinical_history.chief_complaint }}</p>
              </div>
              <div class="clinical-subsection">
                <h4>Bệnh sử</h4>
                <p class="formatted-text">{{ selectedCase.clinical_history.history_present_illness }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.clinical_history.past_medical_history">
                <h4>Tiền sử bệnh</h4>
                <p>{{ selectedCase.clinical_history.past_medical_history }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.clinical_history.family_history">
                <h4>Tiền sử gia đình</h4>
                <p>{{ selectedCase.clinical_history.family_history }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.clinical_history.medications">
                <h4>Thuốc đang dùng</h4>
                <p>{{ selectedCase.clinical_history.medications }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.clinical_history.allergies">
                <h4>Dị ứng</h4>
                <p>{{ selectedCase.clinical_history.allergies }}</p>
              </div>
            </section>

            <!-- Physical Examination Section -->
            <section v-if="selectedCase.physical_examination" class="clinical-section">
              <h3>🩺 Khám lâm sàng</h3>
              <div class="clinical-subsection">
                <h4>Tình trạng chung</h4>
                <p>{{ selectedCase.physical_examination.general_appearance }}</p>
              </div>
              <div class="clinical-subsection">
                <h4>Sinh hiệu</h4>
                <p>{{ selectedCase.physical_examination.vital_signs }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.physical_examination.cardiovascular">
                <h4>Tim mạch</h4>
                <p class="formatted-text">{{ selectedCase.physical_examination.cardiovascular }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.physical_examination.respiratory">
                <h4>Hô hấp</h4>
                <p class="formatted-text">{{ selectedCase.physical_examination.respiratory }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.physical_examination.abdominal">
                <h4>Bụng</h4>
                <p class="formatted-text">{{ selectedCase.physical_examination.abdominal }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.physical_examination.neurological">
                <h4>Thần kinh</h4>
                <p>{{ selectedCase.physical_examination.neurological }}</p>
              </div>
            </section>

            <!-- Investigations Section -->
            <section v-if="selectedCase.detailed_investigations" class="clinical-section">
              <h3>🧪 Cận lâm sàng</h3>
              <div class="clinical-subsection" v-if="selectedCase.detailed_investigations.laboratory_results">
                <h4>Xét nghiệm</h4>
                <p class="formatted-text">{{ selectedCase.detailed_investigations.laboratory_results }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.detailed_investigations.imaging_studies">
                <h4>Chẩn đoán hình ảnh</h4>
                <p class="formatted-text">{{ selectedCase.detailed_investigations.imaging_studies }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.detailed_investigations.ecg_findings">
                <h4>Điện tâm đồ</h4>
                <p class="formatted-text">{{ selectedCase.detailed_investigations.ecg_findings }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.detailed_investigations.biochemistry">
                <h4>Sinh hóa</h4>
                <p class="formatted-text">{{ selectedCase.detailed_investigations.biochemistry }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.detailed_investigations.hematology">
                <h4>Huyết học</h4>
                <p class="formatted-text">{{ selectedCase.detailed_investigations.hematology }}</p>
              </div>
            </section>

            <!-- Diagnosis and Management Section -->
            <section v-if="selectedCase.diagnosis_management" class="clinical-section">
              <h3>💊 Chẩn đoán và điều trị</h3>
              <div class="clinical-subsection">
                <h4>Chẩn đoán chính</h4>
                <p>{{ selectedCase.diagnosis_management.primary_diagnosis }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.diagnosis_management.differential_diagnosis">
                <h4>Chẩn đoán phân biệt</h4>
                <p class="formatted-text">{{ selectedCase.diagnosis_management.differential_diagnosis }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.diagnosis_management.treatment_plan">
                <h4>Kế hoạch điều trị</h4>
                <p class="formatted-text">{{ selectedCase.diagnosis_management.treatment_plan }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.diagnosis_management.medications_prescribed">
                <h4>Thuốc kê đơn</h4>
                <p>{{ selectedCase.diagnosis_management.medications_prescribed }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.diagnosis_management.procedures_performed">
                <h4>Thủ thuật đã thực hiện</h4>
                <p>{{ selectedCase.diagnosis_management.procedures_performed }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.diagnosis_management.prognosis">
                <h4>Tiên lượng</h4>
                <p>{{ selectedCase.diagnosis_management.prognosis }}</p>
              </div>
            </section>

            <!-- Learning Outcomes Section -->
            <section v-if="selectedCase.learning_outcomes" class="clinical-section">
              <h3>🎯 Mục tiêu học tập</h3>
              <div class="clinical-subsection">
                <h4>Mục tiêu học tập</h4>
                <p class="formatted-text">{{ selectedCase.learning_outcomes.learning_objectives }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.learning_outcomes.key_concepts">
                <h4>Khái niệm chính</h4>
                <p class="formatted-text">{{ selectedCase.learning_outcomes.key_concepts }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.learning_outcomes.clinical_pearls">
                <h4>Điểm lâm sàng quan trọng</h4>
                <p class="formatted-text">{{ selectedCase.learning_outcomes.clinical_pearls }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.learning_outcomes.discussion_points">
                <h4>Điểm thảo luận</h4>
                <p class="formatted-text">{{ selectedCase.learning_outcomes.discussion_points }}</p>
              </div>
              <div class="clinical-subsection" v-if="selectedCase.learning_outcomes.references">
                <h4>Tài liệu tham khảo</h4>
                <p class="formatted-text">{{ selectedCase.learning_outcomes.references }}</p>
              </div>
            </section>

            <!-- Medical Attachments Section -->
            <section v-if="selectedCase.medical_attachments && selectedCase.medical_attachments.length > 0"
              class="clinical-section">
              <h3>📁 Tài liệu đính kèm y tế</h3>
              <div class="attachments-grid">
                <div v-for="attachment in selectedCase.medical_attachments" :key="attachment.id" class="attachment-item"
                  :class="{ 'confidential': attachment.is_confidential }">
                  <div class="attachment-header">
                    <div class="attachment-icon">
                      <i :class="getAttachmentIcon(attachment)"></i>
                    </div>
                    <div class="attachment-info">
                      <h4 class="attachment-title">{{ attachment.title }}</h4>
                      <p class="attachment-type">{{ attachment.attachment_type_display }}</p>
                      <p class="attachment-meta">
                        <span v-if="attachment.date_taken">📅 {{ formatDate(attachment.date_taken) }}</span>
                        <span v-if="attachment.department_name">🏥 {{ attachment.department_name }}</span>
                        <span>📏 {{ attachment.file_size_mb }} MB</span>
                      </p>
                    </div>
                    <div class="attachment-actions">
                      <button @click="downloadAttachment(attachment)" class="download-btn"
                        :disabled="attachment.is_confidential && !canViewConfidential"
                        :title="attachment.is_confidential && !canViewConfidential ? 'Tài liệu bảo mật - Chỉ giảng viên được xem' : 'Tải xuống'">
                        <i class="fas fa-download"></i>
                      </button>
                    </div>
                  </div>

                  <div v-if="attachment.description" class="attachment-description">
                    <p><strong>Mô tả:</strong> {{ attachment.description }}</p>
                  </div>

                  <div v-if="attachment.physician_notes" class="attachment-notes">
                    <p><strong>Ghi chú bác sĩ:</strong> {{ attachment.physician_notes }}</p>
                  </div>

                  <div v-if="attachment.is_confidential" class="confidential-badge">
                    <i class="fas fa-lock"></i> Tài liệu bảo mật
                  </div>
                </div>
              </div>
            </section>

            <!-- Medical File Upload Section -->
            <section v-if="canUploadFiles" class="clinical-section upload-section">
              <h3>📎 Thêm tài liệu y tế</h3>

              <!-- Upload Toggle Button -->
              <button v-if="!showUploadForm" @click="showUploadForm = true" class="btn btn-primary upload-toggle-btn">
                <i class="fas fa-plus"></i> Thêm tệp đính kèm
              </button>

              <!-- Upload Form -->
              <div v-if="showUploadForm" class="upload-form">
                <form @submit.prevent="uploadMedicalFile" enctype="multipart/form-data">
                  <!-- File Selection -->
                  <div class="form-group">
                    <label for="medical-file" class="form-label">
                      <i class="fas fa-file-upload"></i> Chọn tệp:
                    </label>
                    <input id="medical-file" ref="fileInput" type="file" @change="handleFileSelect"
                      accept=".jpg,.jpeg,.png,.pdf,.doc,.docx,.dcm,.zip,.rar" class="form-control" required />
                    <small class="form-text">
                      Hỗ trợ: JPG, PNG, PDF, DOC, DOCX, DICOM, ZIP, RAR (Max: 50MB)
                    </small>
                  </div>

                  <!-- Attachment Type -->
                  <div class="form-group">
                    <label for="attachment-type" class="form-label">
                      <i class="fas fa-tags"></i> Loại tài liệu:
                    </label>
                    <select id="attachment-type" v-model="uploadForm.attachment_type" class="form-control" required>
                      <option value="">-- Chọn loại tài liệu --</option>
                      <option value="x_ray">📷 Ảnh chụp X-quang</option>
                      <option value="lab_report">🧪 Phiếu xét nghiệm</option>
                      <option value="ct_scan">🔬 Chụp CT/Scanner</option>
                      <option value="mri_scan">🧠 Chụp MRI</option>
                      <option value="ultrasound">📡 Siêu âm</option>
                      <option value="injury_photo">📸 Ảnh chụp chấn thương</option>
                      <option value="surgical_photo">⚕️ Ảnh phẫu thuật</option>
                      <option value="pathology_slide">🔬 Tiêu bản bệnh học</option>
                      <option value="prescription">💊 Đơn thuốc</option>
                      <option value="discharge_summary">📋 Tóm tắt xuất viện</option>
                      <option value="vital_signs">💓 Dấu hiệu sinh tồn</option>
                      <option value="ekg_ecg">❤️ Điện tâm đồ</option>
                      <option value="endoscopy">🔍 Nội soi</option>
                      <option value="biopsy_report">🧬 Kết quả sinh thiết</option>
                      <option value="medical_certificate">📜 Giấy chứng nhận y tế</option>
                      <option value="other">📄 Khác</option>
                    </select>
                  </div>

                  <!-- Title -->
                  <div class="form-group">
                    <label for="attachment-title" class="form-label">
                      <i class="fas fa-text-width"></i> Tiêu đề:
                    </label>
                    <input id="attachment-title" v-model="uploadForm.title" type="text" class="form-control"
                      placeholder="Nhập tiêu đề mô tả tài liệu..." required />
                  </div>

                  <!-- Description -->
                  <div class="form-group">
                    <label for="attachment-description" class="form-label">
                      <i class="fas fa-align-left"></i> Mô tả (tùy chọn):
                    </label>
                    <textarea id="attachment-description" v-model="uploadForm.description" class="form-control" rows="3"
                      placeholder="Mô tả chi tiết về tài liệu..."></textarea>
                  </div>

                  <!-- Date Taken -->
                  <div class="form-group">
                    <label for="date-taken" class="form-label">
                      <i class="fas fa-calendar"></i> Ngày thực hiện (tùy chọn):
                    </label>
                    <input id="date-taken" v-model="uploadForm.date_taken" type="date" class="form-control" />
                  </div>

                  <!-- Physician Notes -->
                  <div class="form-group">
                    <label for="physician-notes" class="form-label">
                      <i class="fas fa-user-md"></i> Ghi chú bác sĩ (tùy chọn):
                    </label>
                    <textarea id="physician-notes" v-model="uploadForm.physician_notes" class="form-control" rows="2"
                      placeholder="Ghi chú của bác sĩ về tài liệu..."></textarea>
                  </div>

                  <!-- Confidential Checkbox -->
                  <div class="form-group form-check">
                    <input id="is-confidential" v-model="uploadForm.is_confidential" type="checkbox"
                      class="form-check-input" />
                    <label for="is-confidential" class="form-check-label">
                      <i class="fas fa-lock"></i> Tài liệu bảo mật (chỉ giảng viên xem được)
                    </label>
                  </div>

                  <!-- Upload Progress -->
                  <div v-if="uploadProgress > 0" class="upload-progress">
                    <div class="progress">
                      <div class="progress-bar" :style="{ width: uploadProgress + '%' }" role="progressbar">
                        {{ uploadProgress }}%
                      </div>
                    </div>
                  </div>

                  <!-- Form Actions -->
                  <div class="form-actions">
                    <button type="submit" :disabled="uploading" class="btn btn-success">
                      <i class="fas fa-upload" v-if="!uploading"></i>
                      <i class="fas fa-spinner fa-spin" v-if="uploading"></i>
                      {{ uploading ? 'Đang tải lên...' : 'Tải lên' }}
                    </button>
                    <button type="button" @click="cancelUpload" class="btn btn-secondary" :disabled="uploading">
                      Hủy
                    </button>
                  </div>
                </form>
              </div>
            </section>

            <!-- Legacy sections for backward compatibility -->
            <section v-if="!selectedCase.clinical_history && selectedCase.history">
              <h3>Tiền sử (Cũ)</h3>
              <p>{{ selectedCase.history }}</p>
            </section>

            <section v-if="!selectedCase.physical_examination && selectedCase.examination">
              <h3>Khám lâm sàng (Cũ)</h3>
              <p>{{ selectedCase.examination }}</p>
            </section>

            <section v-if="!selectedCase.detailed_investigations && selectedCase.investigations">
              <h3>Xét nghiệm (Cũ)</h3>
              <p>{{ selectedCase.investigations }}</p>
            </section>

            <section v-if="!selectedCase.diagnosis_management && selectedCase.diagnosis">
              <h3>Chẩn đoán (Cũ)</h3>
              <p>{{ selectedCase.diagnosis }}</p>
            </section>

            <section v-if="!selectedCase.diagnosis_management && selectedCase.treatment">
              <h3>Điều trị (Cũ)</h3>
              <p>{{ selectedCase.treatment }}</p>
            </section>

            <section v-if="!selectedCase.learning_outcomes && selectedCase.learning_objectives">
              <h3>Mục tiêu học tập (Cũ)</h3>
              <p>{{ selectedCase.learning_objectives }}</p>
            </section>

            <!-- Grading Section (Instructors Only) -->
            <section v-if="authStore.user?.role === 'instructor'" class="clinical-section grading-section">
              <h3>📝 Chấm điểm và Đánh giá</h3>
              <div class="grading-form">
                <div class="grade-input-group">
                  <label>Điểm số (0-100):</label>
                  <input type="number" min="0" max="100" placeholder="Nhập điểm" class="grade-input" />
                </div>
                <div class="grade-input-group">
                  <label>Nhận xét:</label>
                  <textarea rows="4" placeholder="Nhập nhận xét đánh giá..." class="grade-textarea"></textarea>
                </div>
                <div class="grade-input-group">
                  <label>Điểm mạnh:</label>
                  <textarea rows="3" placeholder="Những điểm làm tốt..." class="grade-textarea"></textarea>
                </div>
                <div class="grade-input-group">
                  <label>Cần cải thiện:</label>
                  <textarea rows="3" placeholder="Những điểm cần cải thiện..." class="grade-textarea"></textarea>
                </div>
                <div class="grade-actions">
                  <button class="btn btn-primary">
                    <i class="fas fa-save"></i> Lưu đánh giá
                  </button>
                  <button class="btn btn-success">
                    <i class="fas fa-check"></i> Hoàn thành chấm điểm
                  </button>
                </div>
              </div>
            </section>

            <!-- Grade Display (Students Only) -->
            <section v-if="authStore.user?.role === 'student' && selectedCase.grade"
              class="clinical-section grade-display-section">
              <h3>📊 Kết quả đánh giá</h3>
              <div class="grade-display">
                <div class="grade-score">
                  <span class="score-label">Điểm số:</span>
                  <span class="score-value">{{ selectedCase.grade.score }}/100</span>
                  <span class="score-letter">{{ selectedCase.grade.letter_grade ||
                    getLetterGrade(selectedCase.grade.score) }}</span>
                </div>
                <div class="grade-feedback" v-if="selectedCase.grade.evaluation_notes">
                  <h4>Nhận xét của giảng viên:</h4>
                  <p>{{ selectedCase.grade.evaluation_notes }}</p>
                </div>
                <div class="grade-feedback" v-if="selectedCase.grade.strengths">
                  <h4>Điểm mạnh:</h4>
                  <p>{{ selectedCase.grade.strengths }}</p>
                </div>
                <div class="grade-feedback" v-if="selectedCase.grade.weaknesses">
                  <h4>Cần cải thiện:</h4>
                  <p>{{ selectedCase.grade.weaknesses }}</p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>

    <!-- Case Sharing Panel Modal -->
    <div v-if="showSharingPanel && selectedCaseForSharing" class="modal-overlay" @click="closeSharingPanel">
      <div class="modal sharing-modal" @click.stop>
        <div class="modal-header">
          <h2>🔗 Chia sẻ ca bệnh: {{ selectedCaseForSharing.title }}</h2>
          <button @click="closeSharingPanel" class="close-btn">&times;</button>
        </div>
        <div class="modal-content">
          <CaseSharingPanel :case-id="selectedCaseForSharing.id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCasesStore } from '@/stores/cases'
import { useChoices } from '@/composables/useChoices'
import { requireRoles } from '@/composables/useAuthorize'
// Use the TypeScript export service which exposes exportCase convenience method
import { exportService } from '@/services/export.ts'
import { casesService } from '@/services/cases'
import CaseSharingPanel from '@/components/CaseSharingPanel.vue'
import CloneCaseDialog from '@/components/CloneCaseDialog.vue'

const router = useRouter()
const authStore = useAuthStore()
const casesStore = useCasesStore()
const { specialties, loading: choicesLoading } = useChoices()

const searchQuery = ref('')
const activeFilter = ref('all')
const specialtyFilter = ref('')
const dateSort = ref('newest')
const selectedCase = ref<Record<string, any> | null>(null)
const showExportMenu = ref<number | string | null>(null)
const exporting = ref(false)

// Collection filter for students (all, my-cases, saved)
const collectionFilter = ref<'all' | 'my-cases' | 'saved'>('all')

// Clone dialog state
const showCloneDialog = ref(false)
const cloneCaseId = ref<number | undefined>(undefined)

// Case sharing state
const showSharingPanel = ref(false)
const selectedCaseForSharing = ref<Record<string, any> | null>(null)

// Pagination state
const currentPage = ref(1)

// Statistics state for accurate counts
const statistics = ref<{
  total_cases: number;
  by_status: { case_status: string; count: number }[];
} | null>(null)
const statsLoading = ref(false)

// Medical file upload state
const showUploadForm = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const uploadForm = ref({
  attachment_type: '',
  title: '',
  description: '',
  date_taken: '',
  physician_notes: '',
  is_confidential: false
})

// Role-based status tabs
const statusTabs = computed(() => {
  if (authStore.user?.role === 'instructor') {
    // Teachers see: all cases, submitted/graded combined
    return [
      { value: 'all', label: 'Tất cả hồ sơ' },
      { value: 'submitted', label: 'Chờ chấm / Đã chấm' }
    ]
  } else {
    // Students see: all, draft, submitted/graded combined
    return [
      { value: 'all', label: 'Tất cả hồ sơ' },
      { value: 'draft', label: 'Bản nháp' },
      { value: 'submitted', label: 'Đã nộp / Đã chấm' }
    ]
  }
})

const loading = computed(() => casesStore.loading)
const error = computed(() => casesStore.error)
const cases = computed(() => casesStore.cases)
const pagination = computed(() => casesStore.pagination)
const totalCases = computed(() => casesStore.pagination.count)

// Computed properties for collection categorization
const myCasesCount = computed(() => {
  return cases.value.filter(c => !c.cloned_from && c.created_by_id === authStore.user?.id).length
})

const savedCasesCount = computed(() => {
  return cases.value.filter(c => c.cloned_from).length
})

// Get cases based on current collection filter (for stats)
const currentCollectionCases = computed(() => {
  if (!isStudent.value) return cases.value

  if (collectionFilter.value === 'my-cases') {
    return cases.value.filter(c => !c.cloned_from && c.created_by_id === authStore.user?.id)
  } else if (collectionFilter.value === 'saved') {
    return cases.value.filter(c => c.cloned_from)
  }
  return cases.value
})

const filteredCases = computed(() => {
  let filtered = cases.value

  // Teachers should NEVER see draft cases
  if (authStore.user?.role === 'instructor') {
    filtered = filtered.filter(c => c.case_status !== 'draft')
  }

  // Filter by collection type (for students)
  if (isStudent.value && collectionFilter.value !== 'all') {
    if (collectionFilter.value === 'my-cases') {
      // My own cases (not cloned)
      filtered = filtered.filter(c => !c.cloned_from && c.created_by_id === authStore.user?.id)
    } else if (collectionFilter.value === 'saved') {
      // Saved/cloned cases from instructors
      filtered = filtered.filter(c => c.cloned_from)
    }
  }

  // Filter by status
  if (activeFilter.value !== 'all') {
    if (activeFilter.value === 'submitted') {
      // For instructors: only show ungraded cases (submitted status only)
      // For students: show all submitted cases including reviewed/approved
      if (authStore.user?.role === 'instructor') {
        filtered = filtered.filter(c => c.case_status === 'submitted')
      } else {
        filtered = filtered.filter(c =>
          c.case_status === 'submitted' ||
          c.case_status === 'reviewed' ||
          c.case_status === 'approved'
        )
      }
    } else {
      filtered = filtered.filter(c => c.case_status === activeFilter.value)
    }
  }

  // Filter by specialty
  if (specialtyFilter.value) {
    filtered = filtered.filter(c => c.specialty === specialtyFilter.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(c =>
      c.title.toLowerCase().includes(query) ||
      c.specialty.toLowerCase().includes(query) ||
      c.patient_name.toLowerCase().includes(query) ||
      (c.keywords && c.keywords.toLowerCase().includes(query)) ||
      (c.diagnosis && c.diagnosis.toLowerCase().includes(query))
    )
  }

  // Sort by date
  if (dateSort.value) {
    filtered = [...filtered].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime()
      const dateB = new Date(b.created_at).getTime()

      if (dateSort.value === 'newest') {
        return dateB - dateA // Newest first
      } else if (dateSort.value === 'oldest') {
        return dateA - dateB // Oldest first
      }
      return 0
    })
  }

  return filtered
})

const canViewConfidential = computed(() => {
  // Only instructors and administrators can view confidential attachments
  return authStore.user && (authStore.user.role === 'instructor' || authStore.user.role === 'admin')
})

const isStudent = computed(() => {
  return authStore.user && authStore.user.role === 'student'
})

const canUploadFiles = computed(() => {
  // Users can upload files to their own cases or if they have edit permissions
  return selectedCase.value && (
    selectedCase.value.student_id === authStore.user?.id ||
    authStore.user?.role === 'instructor' ||
    authStore.user?.role === 'admin'
  )
})

async function loadStatistics() {
  statsLoading.value = true
  try {
    const response = await casesService.getCaseSummaryStatistics()
    // Parse the response format from backend
    statistics.value = {
      total_cases: response.summary?.total_cases || 0,
      by_status: response.distributions?.by_status || []
    }
  } catch (err) {
    console.error('Failed to load statistics:', err)
  } finally {
    statsLoading.value = false
  }
}

async function loadCases(page: number = 1) {
  try {
    const params: any = { page }
    
    // Pass status filter to backend API for proper filtering
    if (activeFilter.value !== 'all') {
      if (activeFilter.value === 'submitted' && authStore.user?.role === 'instructor') {
        // Instructors: filter only ungraded (submitted) cases
        params.case_status = 'submitted'
      } else if (activeFilter.value !== 'submitted') {
        // Other filters pass directly
        params.case_status = activeFilter.value
      }
      // For students with 'submitted' filter, don't pass to API - client-side handles it
    }
    
    // Pass specialty filter if set
    if (specialtyFilter.value) {
      params.specialty = specialtyFilter.value
    }
    
    // Pass search query if set
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    await casesStore.fetchCases(params)
    currentPage.value = page
    // Load fresh statistics when cases are loaded
    await loadStatistics()
  } catch (err) {
    console.error('Failed to load cases:', err)
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= pagination.value.total_pages) {
    loadCases(page)
  }
}

// Handle stat card filter click - reload cases from API with new filter
function setActiveFilter(filter: string) {
  if (activeFilter.value !== filter) {
    activeFilter.value = filter
    loadCases(1) // Reload from page 1 with new filter
  }
}

const paginationPages = computed(() => {
  const total = pagination.value.total_pages
  const current = currentPage.value
  const pages: (number | string)[] = []

  if (total <= 7) {
    // Show all pages if 7 or fewer
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)

    if (current > 3) {
      pages.push('...')
    }

    // Show pages around current
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i)
    }

    if (current < total - 2) {
      pages.push('...')
    }

    // Always show last page
    pages.push(total)
  }

  return pages
})

function handleSearch() {
  // Debounce search if needed
  // For now, search is reactive through computed property
}

function applyFilters() {
  // Filters are applied reactively through computed property
  // This function can be used for analytics or additional processing
}

function toggleExportMenu(caseId: string) {
  showExportMenu.value = showExportMenu.value === caseId ? null : caseId
}

async function exportCase(caseItem: any, format: string) {
  if (exporting.value) return

  exporting.value = true
  showExportMenu.value = null

  try {
    // Prefer TS service exportCase if available, fallback to quickExport
    if (typeof (exportService as any).exportCase === 'function') {
      await (exportService as any).exportCase(caseItem.id.toString(), format, caseItem.title)
    } else if (typeof (exportService as any).quickExport === 'function') {
      await (exportService as any).quickExport(caseItem.id, format === 'powerpoint' ? 'ppt' : format)
    } else {
      throw new Error('No export function available')
    }
    // Show success message
    alert(`Đã xuất hồ sơ "${caseItem.title}" sang ${format.toUpperCase()} thành công!`)
  } catch (error) {
    console.error('Export failed:', error)
    alert('Có lỗi xảy ra khi xuất file. Vui lòng thử lại.')
  } finally {
    exporting.value = false
  }
}

async function viewCase(case_: any) {
  try {
    // Fetch full case details instead of using list data
    await casesStore.fetchCase(case_.id)
    selectedCase.value = casesStore.currentCase

    // DEBUG: Log the case data to see what's being returned
    console.log('=== CASE DATA DEBUG ===')
    console.log('Full case:', selectedCase.value)
    console.log('Has clinical_history?', !!selectedCase.value?.clinical_history)
    console.log('clinical_history:', selectedCase.value?.clinical_history)
    console.log('Has physical_examination?', !!selectedCase.value?.physical_examination)
    console.log('physical_examination:', selectedCase.value?.physical_examination)
    console.log('Has detailed_investigations?', !!selectedCase.value?.detailed_investigations)
    console.log('Has diagnosis_management?', !!selectedCase.value?.diagnosis_management)
    console.log('Has learning_outcomes?', !!selectedCase.value?.learning_outcomes)
  } catch (error) {
    console.error('Failed to load case details:', error)
    // Fallback to list data if detail fetch fails
    selectedCase.value = case_
  }
}

// Case sharing functions
function openSharingPanel(case_: any) {
  selectedCaseForSharing.value = case_
  showSharingPanel.value = true
}

function closeSharingPanel() {
  showSharingPanel.value = false
  selectedCaseForSharing.value = null
}

// Clone case functions
function openCloneDialog(case_: any) {
  cloneCaseId.value = case_.id
  showCloneDialog.value = true
}

function handleCloneSuccess(clonedCase: any) {
  // Refresh the case list
  loadCases()
  // Switch to "saved" collection view to show the newly saved case
  collectionFilter.value = 'saved'
  // Show success message
  alert(`Đã lưu hồ sơ "${clonedCase.title}" vào bộ sưu tập của bạn thành công!`)
  // Optionally navigate to the new case
  // router.push(`/cases/${clonedCase.id}`)
}

function isOwner(case_: any): boolean {
  return case_.student === authStore.user?.id || authStore.user?.role === 'instructor'
}

function closeModal() {
  selectedCase.value = null
  casesStore.clearCurrentCase()
}

async function logout() {
  await authStore.logout()
  router.push('/')
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('vi-VN')
}

function getLetterGrade(score: number) {
  if (score >= 90) return 'A'
  if (score >= 80) return 'B'
  if (score >= 70) return 'C'
  if (score >= 60) return 'D'
  return 'F'
}

function getStatusLabel(status: string) {
  const statusMap: Record<string, string> = {
    'draft': 'Bản nháp',
    'submitted': 'Đã nộp',
    'reviewed': 'Đã duyệt',
    'approved': 'Đã phê duyệt'
  }
  return statusMap[status] || status
}

function getStatusCount(status: string) {
  // For collection filters (my-cases, saved), use local filtering on current page
  if (isStudent.value && collectionFilter.value !== 'all') {
    const baseCases = currentCollectionCases.value
    if (status === 'all') {
      return baseCases.length
    }
    if (status === 'submitted') {
      return baseCases.filter(case_ =>
        case_.case_status === 'submitted' ||
        case_.case_status === 'reviewed' ||
        case_.case_status === 'approved'
      ).length
    }
    return baseCases.filter(case_ => case_.case_status === status).length
  }

  // For 'all' status, use statistics.total_cases (unfiltered count from backend)
  // Fall back to pagination.count only when no filter is active
  if (status === 'all') {
    // If we have statistics, use the total_cases (always unfiltered)
    if (statistics.value?.total_cases) {
      return statistics.value.total_cases
    }
    // Fallback to pagination count (only accurate when no filter is active)
    return pagination.value.count || cases.value.length
  }

  // Use statistics from backend for status-specific counts across all pages
  if (statistics.value) {
    if (status === 'submitted') {
      const byStatus = statistics.value.by_status
      // For instructors: only count ungraded cases (submitted status only)
      // For students: count all submitted + reviewed + approved
      if (authStore.user?.role === 'instructor') {
        return byStatus.find(s => s.case_status === 'submitted')?.count || 0
      } else {
        const submittedCount = byStatus.find(s => s.case_status === 'submitted')?.count || 0
        const reviewedCount = byStatus.find(s => s.case_status === 'reviewed')?.count || 0
        const approvedCount = byStatus.find(s => s.case_status === 'approved')?.count || 0
        return submittedCount + reviewedCount + approvedCount
      }
    }
    const statusItem = statistics.value.by_status.find(s => s.case_status === status)
    return statusItem?.count || 0
  }
  
  // Fallback to local filtering if statistics not loaded
  const baseCases = cases.value
  if (status === 'submitted') {
    // For instructors: only count ungraded cases
    if (authStore.user?.role === 'instructor') {
      return baseCases.filter(case_ => case_.case_status === 'submitted').length
    }
    return baseCases.filter(case_ =>
      case_.case_status === 'submitted' ||
      case_.case_status === 'reviewed' ||
      case_.case_status === 'approved'
    ).length
  }
  return baseCases.filter(case_ => case_.case_status === status).length
}

function getAttachmentIcon(attachment: any) {
  const iconMap: Record<string, string> = {
    'x_ray': 'fas fa-x-ray',
    'lab_report': 'fas fa-vial',
    'ct_scan': 'fas fa-lungs',
    'mri_scan': 'fas fa-brain',
    'ultrasound': 'fas fa-heartbeat',
    'injury_photo': 'fas fa-camera-medical',
    'surgical_photo': 'fas fa-scalpel',
    'pathology_slide': 'fas fa-microscope',
    'prescription': 'fas fa-prescription',
    'discharge_summary': 'fas fa-file-medical-alt',
    'vital_signs': 'fas fa-chart-line',
    'ekg_ecg': 'fas fa-heartbeat',
    'endoscopy': 'fas fa-eye',
    'biopsy_report': 'fas fa-dna',
    'medical_certificate': 'fas fa-certificate',
    'other': 'fas fa-file-medical'
  }
  return iconMap[attachment.attachment_type] || 'fas fa-file-medical'
}

async function downloadAttachment(attachment: any) {
  if (attachment.is_confidential && !canViewConfidential.value) {
    alert('Bạn không có quyền xem tài liệu bảo mật này.')
    return
  }

  try {
    const response = await casesService.downloadAttachment(attachment.id)

    // Create blob link to download
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', attachment.original_filename || `${attachment.title}.${attachment.file_extension}`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error downloading attachment:', error)
    alert('Lỗi khi tải xuống tệp')
  }
}

function handleFileSelect(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    selectedFile.value = file

    // Auto-fill title with filename if empty
    if (!uploadForm.value.title) {
      uploadForm.value.title = file.name.split('.')[0] ?? ''
    }

    // Validate file size (50MB max)
    const maxSize = 50 * 1024 * 1024 // 50MB in bytes
    if (file.size > maxSize) {
      alert('Tệp quá lớn! Vui lòng chọn tệp nhỏ hơn 50MB.')
      resetFileInput()
      return
    }
  }
}

async function uploadMedicalFile() {
  if (!selectedFile.value || !selectedCase.value) {
    alert('Vui lòng chọn tệp và đảm bảo đã chọn ca bệnh!')
    return
  }

  uploading.value = true
  uploadProgress.value = 0

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('attachment_type', uploadForm.value.attachment_type)
    formData.append('title', uploadForm.value.title)
    formData.append('description', uploadForm.value.description || '')
    formData.append('physician_notes', uploadForm.value.physician_notes || '')
    formData.append('is_confidential', `${uploadForm.value.is_confidential}`)

    if (uploadForm.value.date_taken) {
      formData.append('date_taken', uploadForm.value.date_taken)
    }

    // Simulate upload progress (you can implement real progress with axios onUploadProgress)
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += Math.random() * 20
      }
    }, 200)

    // Upload file
    const response = await casesService.uploadAttachment(selectedCase.value.id, formData)

    clearInterval(progressInterval)
    uploadProgress.value = 100

    // Add the new attachment to the current case
    if (!selectedCase.value.medical_attachments) {
      selectedCase.value.medical_attachments = []
    }
    selectedCase.value.medical_attachments.push(response)

    // Reset form
    resetUploadForm()
    alert('Tải lên thành công!')

  } catch (error: any) {
    console.error('Upload error:', error)
    alert('Lỗi khi tải lên tệp: ' + (error.response?.data?.message || error.message))
  } finally {
    uploading.value = false
    uploadProgress.value = 0
  }
}

function cancelUpload() {
  resetUploadForm()
}

function resetUploadForm() {
  showUploadForm.value = false
  uploading.value = false
  uploadProgress.value = 0
  selectedFile.value = null

  // Reset form data
  uploadForm.value = {
    attachment_type: '',
    title: '',
    description: '',
    date_taken: '',
    physician_notes: '',
    is_confidential: false
  }

  resetFileInput()
}

function resetFileInput() {
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  selectedFile.value = null
}

onMounted(() => {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  // Component-level roles guard (student + instructor allowed)
  requireRoles(['student', 'instructor'])

  loadCases()
})
</script>

<style scoped>
/* Page Header */
.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  color: #1f2937;
  font-size: 1.875rem;
  font-weight: 700;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
  text-decoration: none;
  border: 1px solid transparent;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  transform: translateY(-1px);
}

/* Filters Section */
.filters-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.search-and-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-container {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-options {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background: white;
  min-width: 180px;
  font-size: 0.875rem;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-tabs {
  display: flex;
  gap: 0.25rem;
  background: #f9fafb;
  padding: 0.25rem;
  border-radius: 0.5rem;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #6b7280;
  font-weight: 500;
  font-size: 0.875rem;
}

.filter-tab:hover {
  background: white;
  color: #374151;
}

.filter-tab.active {
  background: white;
  color: #3b82f6;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.tab-count {
  background: #e5e7eb;
  color: #6b7280;
  padding: 0.125rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.filter-tab.active .tab-count {
  background: #dbeafe;
  color: #3b82f6;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s;
  cursor: pointer;
  border: 2px solid transparent;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.stat-card.stat-active {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
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
  color: #1f2937;
  line-height: 1;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* Cases Grid */
.loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.error {
  text-align: center;
  padding: 2rem;
  margin: 2rem auto;
  max-width: 500px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.75rem;
  color: #991b1b;
}

.error p {
  margin: 0 0 1.5rem 0;
  font-size: 1rem;
  line-height: 1.5;
}

.error .btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.error .btn:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.case-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
  border: 1px solid #f3f4f6;
}

.case-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: #e5e7eb;
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.case-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.125rem;
  line-height: 1.4;
  font-weight: 600;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.draft {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.submitted {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.reviewed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.approved {
  background: #dcfce7;
  color: #14532d;
}

.case-meta {
  margin-bottom: 1rem;
}

.case-meta p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.case-meta strong {
  color: #374151;
}

.case-actions {
  display: flex;
  gap: 0.5rem;
  position: relative;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.case-actions .btn {
  flex: 1;
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
}

.export-dropdown {
  position: relative;
}

.export-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  z-index: 1000;
  min-width: 160px;
  margin-top: 0.25rem;
  overflow: hidden;
}

.export-option {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 0.875rem;
  color: #374151;
}

.export-option:hover {
  background: #f9fafb;
  color: #111827;
}

.export-option:first-child {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.export-option:last-child {
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn-outline {
  background: transparent;
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.btn-outline:hover {
  background: #3b82f6;
  color: white;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

/* Pagination Styles */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding: 1rem;
  flex-wrap: wrap;
}

.pagination-btn {
  min-width: 2.5rem;
  height: 2.5rem;
  padding: 0 0.75rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border-color: #3b82f6;
}

.pagination-ellipsis {
  padding: 0 0.5rem;
  color: #6b7280;
}

.pagination-info {
  margin-left: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal {
  background: white;
  border-radius: 12px;
  max-width: 1000px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e1e5e9;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #374151;
}

.modal-content {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.loading-modal {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  color: #6b7280;
  font-size: 1.1rem;
}

.case-detail section {
  margin-bottom: 2rem;
}

.case-detail section h3 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.125rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.case-detail section p {
  margin: 0.5rem 0;
  line-height: 1.6;
  color: #4b5563;
}

/* Enhanced styles for detailed medical sections */
.patient-info {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.info-item {
  background: white;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.clinical-section {
  background: #fefefe;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.clinical-section h3 {
  color: #1f2937;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #3b82f6;
}

.clinical-subsection {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
  border-left: 3px solid #6b7280;
}

.clinical-subsection:last-child {
  margin-bottom: 0;
}

.clinical-subsection h4 {
  margin: 0 0 0.75rem 0;
  color: #374151;
  font-size: 1rem;
  font-weight: 600;
}

.clinical-subsection p {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
}

.formatted-text {
  white-space: pre-line;
  word-wrap: break-word;
}

/* Color coding for different sections */
.patient-info {
  border-left-color: #3b82f6;
  /* Blue */
}

.clinical-section:nth-child(2) {
  border-left: 4px solid #10b981;
  /* Green - Clinical History */
}

.clinical-section:nth-child(3) {
  border-left: 4px solid #f59e0b;
  /* Amber - Physical Examination */
}

.clinical-section:nth-child(4) {
  border-left: 4px solid #8b5cf6;
  /* Purple - Investigations */
}

.clinical-section:nth-child(5) {
  border-left: 4px solid #ef4444;
  /* Red - Diagnosis & Management */
}

.clinical-section:nth-child(6) {
  border-left: 4px solid #06b6d4;
  /* Cyan - Learning Outcomes */
}

/* Medical Attachments Styles */
.attachments-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
}

.attachment-item {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
  position: relative;
}

.attachment-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.attachment-item.confidential {
  border-color: #dc2626;
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
  background: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.1rem;
}

.attachment-item.confidential .attachment-icon {
  background: #dc2626;
}

.attachment-info {
  flex: 1;
  min-width: 0;
}

.attachment-title {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  word-wrap: break-word;
}

.attachment-type {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.attachment-meta {
  margin: 0;
  font-size: 0.75rem;
  color: #9ca3af;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.attachment-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.attachment-actions {
  flex-shrink: 0;
}

.download-btn {
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.download-btn:hover:not(:disabled) {
  background: #2563eb;
}

.download-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.attachment-description,
.attachment-notes {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.attachment-description p,
.attachment-notes p {
  margin: 0;
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.5;
}

.attachment-description strong,
.attachment-notes strong {
  color: #1f2937;
}

.confidential-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #dc2626;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .attachments-grid {
    grid-template-columns: 1fr;
  }

  .attachment-header {
    flex-direction: column;
    align-items: stretch;
  }

  .attachment-actions {
    align-self: flex-end;
  }
}

/* Upload Form Styles */
.upload-section {
  border-left: 4px solid #16a34a;
  /* Green for upload section */
}

.upload-toggle-btn {
  background: #16a34a;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.upload-toggle-btn:hover {
  background: #15803d;
}

.upload-form {
  margin-top: 1rem;
  padding: 1.5rem;
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
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
  color: #1f2937;
  font-size: 0.875rem;
}

.form-label i {
  margin-right: 0.5rem;
  color: #6b7280;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-text {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.form-check {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.form-check-input {
  width: 1rem;
  height: 1rem;
  margin: 0;
}

.form-check-label {
  font-size: 0.875rem;
  color: #374151;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.upload-progress {
  margin: 1rem 0;
}

.progress {
  width: 100%;
  height: 1rem;
  background: #e5e7eb;
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
  border-top: 1px solid #e5e7eb;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-success {
  background: #16a34a;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #15803d;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #4b5563;
}

/* Responsive upload form */
@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
    justify-content: center;
  }

  .upload-form {
    padding: 1rem;
  }
}

/* Grading Section Styles */
.grading-section {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
}

.grading-form {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.grade-input-group {
  margin-bottom: 1.5rem;
}

.grade-input-group label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.grade-input {
  width: 150px;
  padding: 0.75rem;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.grade-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.grade-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
}

.grade-textarea:focus {
  outline: none;
  border-color: #3b82f6;
}

.grade-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

/* Grade Display Styles */
.grade-display-section {
  background: #dbeafe;
  border-left: 4px solid #3b82f6;
}

.grade-display {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.grade-score {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  border-radius: 8px;
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
  background: #f9fafb;
  border-radius: 6px;
  border-left: 3px solid #3b82f6;
}

.grade-feedback h4 {
  color: #1e40af;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.grade-feedback p {
  color: #374151;
  line-height: 1.6;
  margin: 0;
}

/* Case Sharing Styles */
.btn.btn-secondary {
  background: #6366f1;
  color: white;
  border: 1px solid #6366f1;
}

.btn.btn-secondary:hover {
  background: #4f46e5;
  border-color: #4f46e5;
}

.sharing-modal {
  max-width: 1200px;
  width: 95vw;
  max-height: 90vh;
  overflow-y: auto;
}

.sharing-modal .modal-content {
  padding: 0;
}

/* Header Badges */
.header-badges {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

/* Filter Checkbox */
.filter-checkbox-group {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  white-space: nowrap;
}

.filter-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #3b82f6;
}

.filter-checkbox-group label {
  margin: 0;
  cursor: pointer;
  user-select: none;
}

/* Success Button */
.btn-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.btn-success:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
}

.btn-secondary {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.btn-secondary:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  transform: translateY(-1px);
}

/* Collection Category Tabs */
.collection-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding: 0 1rem;
  flex-wrap: wrap;
}

.collection-tab {
  padding: 0.75rem 1.25rem;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.collection-tab:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
}

.collection-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Saved Case Card Styling */
.case-card.saved-case {
  border-left: 4px solid #10b981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(255, 255, 255, 1) 100%);
}

.template-badge {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.saved-badge {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
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
</style>
