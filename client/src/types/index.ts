export type ApplicationStatus =
  | "wishlist"
  | "applied"
  | "phone_screen"
  | "interview"
  | "offer"
  | "rejected"
  | "closed";

export type ApplicationPriority = "low" | "medium" | "high";

export type LanguagePreference = "en" | "ja";

export type InterviewFormat = "phone" | "video" | "onsite" | "take_home";

export interface User {
  id: string;
  email: string;
  full_name: string;
  preferred_language: LanguagePreference;
  created_at: string;
}

export interface StatusHistory {
  id: string;
  application: string;
  from_status: string;
  to_status: string;
  changed_at: string;
}

export interface Contact {
  id: string;
  application: string;
  name: string;
  role: string;
  email: string;
  linkedin_url?: string;
}

export interface Interview {
  id: string;
  application: string;
  round_number: number;
  interview_date: string;
  format: InterviewFormat;
  notes: string;
}

export interface Application {
  id: string;
  owner?: string;
  company_name: string;
  role_title: string;
  location?: string;
  salary_min?: number;
  salary_max?: number;
  job_url?: string;
  status: ApplicationStatus;
  priority: ApplicationPriority;
  applied_date?: string;
  follow_up_date?: string;
  notes: string;
  created_at: string;
  updated_at: string;

  // Nested serializers return these full objects
  contacts?: Contact[];
  interviews?: Interview[];
  history?: StatusHistory[];
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface TokenPair {
  access: string;
  refresh: string;
}

// Dashboard Stats Types
export interface DashboardStats {
  counts_by_stage: Record<ApplicationStatus, number>;
  response_rate: number;
  avg_days_to_response: number | null;
  top_companies: Array<{
    company_name: string;
    highest_stage: string;
    count: number;
  }>;
}

export interface ActivityStat {
  week: string;
  count: number;
}
