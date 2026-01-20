/**
 * TypeScript interfaces for Instructor Case features
 */

export interface InstructorCase {
  id: number;
  title: string;
  summary: string;
  specialty: string;
  is_public: boolean;
  approved: boolean;
  cloned_from?: number | null;
  cloned_from_title?: string | null;
  cloned_from_instructor_name?: string | null;
  // Author/student info (from list serializer)
  student_name?: string;
  created_by_name?: string;
  created_by_id?: number;
  medical_sections?: MedicalSection[];
  created_by?: User;
  created_at: string;
  updated_at: string;
}

export interface MedicalSection {
  id: number;
  case: number;
  section_type: 'chief_complaint' | 'hpi' | 'physical_exam' | 'assessment' | 'plan';
  content: string;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_instructor: boolean;
}

export interface InstructorCaseAuditLog {
  id: number;
  case: number;
  changed_by: User;
  change_type: 'create' | 'update' | 'approve' | 'clone';
  summary: string;
  diff?: Record<string, any>;
  timestamp: string;
}

export interface CloneCaseRequest {
  title?: string;
  owner?: number | null;
  adjust_fields?: Record<string, any>;
}

export interface CloneCaseResponse extends InstructorCase {
  cloned_from: number;
}

export interface CreateInstructorCaseRequest {
  title: string;
  summary: string;
  specialty: string;
  // Required patient fields (matching backend Case model)
  patient_name: string;
  patient_age: number | null;
  patient_gender: string;
  // Repository ID (foreign key to Repository model)
  repository: number | null;
  // Optional fields
  medical_sections?: MedicalSection[];
  tags?: string[];
  is_public?: boolean;
}

export interface ListCasesParams {
  page?: number;
  page_size?: number;
  ordering?: string;
  search?: string;
}

export interface CaseListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: InstructorCase[];
}
