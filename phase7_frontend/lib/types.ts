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

export interface ErrorResponse {
  message: string;
  code: ErrorCode;
  details?: {
    errors?: { field: string; message: string }[];
  };
}

export interface RestaurantDetail {
  id: string;
  name: string;
  location: string;
  city: string;
  locality: string;
  cuisines: string[];
  cost_for_two: number;
  budget_tier: string;
  rating: number;
  address?: string | null;
  votes?: number | null;
  rest_type?: string | null;
  online_order?: boolean | null;
  book_table?: boolean | null;
}

export interface SearchHistoryItem {
  location: string;
  cuisine: string;
  budget: string;
  min_rating: number;
  additional_notes?: string | null;
  searched_at: string;
}
