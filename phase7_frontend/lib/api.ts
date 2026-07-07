import type {
  ErrorResponse,
  RecommendationRequest,
  RecommendationResponse,
  RestaurantDetail,
  SearchHistoryItem,
} from "./types";
import { getApiUrl } from "./env";

const API_URL = getApiUrl();

export class ApiError extends Error {
  status: number;
  code?: string;

  constructor(message: string, status: number, code?: string) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

async function parseError(response: Response): Promise<ApiError> {
  try {
    const body = (await response.json()) as ErrorResponse;
    return new ApiError(body.message, response.status, body.code);
  } catch {
    return new ApiError(response.statusText || "Request failed", response.status);
  }
}

export async function fetchRecommendations(
  request: RecommendationRequest,
  options?: { topN?: number; fallbackOnly?: boolean },
): Promise<RecommendationResponse> {
  const params = new URLSearchParams({
    top_n: String(options?.topN ?? 5),
    fallback_only: String(options?.fallbackOnly ?? false),
  });

  const response = await fetch(`${API_URL}/api/recommendations?${params}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    cache: "no-store",
  });

  if (!response.ok) {
    throw await parseError(response);
  }

  return response.json();
}

export async function fetchRestaurantDetail(id: string): Promise<RestaurantDetail> {
  const response = await fetch(`${API_URL}/api/restaurants/${id}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw await parseError(response);
  }

  return response.json();
}

export async function fetchSearchHistory(limit = 5): Promise<SearchHistoryItem[]> {
  const response = await fetch(`${API_URL}/api/search/history?limit=${limit}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    return [];
  }

  const body = await response.json();
  return body.items ?? [];
}

export async function fetchHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`, { cache: "no-store" });
    return response.ok;
  } catch {
    return false;
  }
}
