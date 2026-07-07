// Auto-aligned with phase5_response_contract — do not edit by hand unless syncing Python models.

export type BudgetTier = "low" | "medium" | "high";

export type RecommendationSource = "openai" | "fallback";

export type ErrorCode =
  | "validation_error"
  | "no_matches"
  | "openai_error"
  | "server_error";

export interface UserPreferences {
  location: string;
  budget: BudgetTier;
  cuisine: string;
  min_rating: number;
  additional_notes?: string | null;
}

export interface RecommendationRequest {
  location: string;
  budget: BudgetTier;
  cuisine: string;
  min_rating: number;
  additional_notes?: string | null;
}

export interface Recommendation {
  rank: number;
  restaurant_id: string;
  name: string;
  cuisine: string;
  rating: number;
  estimated_cost: string | number;
  explanation: string;
}

export interface RecommendationResponse {
  summary?: string | null;
  recommendations: Recommendation[];
  source: RecommendationSource;
  preferences?: UserPreferences | null;
  total_matches?: number | null;
}

export interface FieldError {
  field: string;
  message: string;
}

export interface ErrorDetails {
  errors?: FieldError[] | null;
  extra?: Record<string, unknown> | null;
}

export interface ErrorResponse {
  message: string;
  code: ErrorCode;
  details?: ErrorDetails | Record<string, unknown> | null;
}
