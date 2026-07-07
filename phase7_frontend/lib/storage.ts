import type { RecommendationRequest, RecommendationResponse } from "./types";

const REQUEST_KEY = "bitewise_pending_request";
const RESULTS_KEY = "bitewise_results";

export function savePendingRequest(request: RecommendationRequest): void {
  if (typeof window === "undefined") return;
  sessionStorage.setItem(REQUEST_KEY, JSON.stringify(request));
}

export function consumePendingRequest(): RecommendationRequest | null {
  if (typeof window === "undefined") return null;
  const raw = sessionStorage.getItem(REQUEST_KEY);
  if (!raw) return null;
  sessionStorage.removeItem(REQUEST_KEY);
  return JSON.parse(raw) as RecommendationRequest;
}

export function saveResults(results: RecommendationResponse): void {
  if (typeof window === "undefined") return;
  sessionStorage.setItem(RESULTS_KEY, JSON.stringify(results));
}

export function loadResults(): RecommendationResponse | null {
  if (typeof window === "undefined") return null;
  const raw = sessionStorage.getItem(RESULTS_KEY);
  if (!raw) return null;
  return JSON.parse(raw) as RecommendationResponse;
}

export function clearResults(): void {
  if (typeof window === "undefined") return;
  sessionStorage.removeItem(RESULTS_KEY);
}

export function budgetLabel(tier: string): string {
  if (tier === "low") return "$";
  if (tier === "high") return "$$$";
  return "$$";
}

export function formatCost(cost: string | number): string {
  const value = typeof cost === "number" ? cost : parseFloat(cost);
  if (Number.isNaN(value)) return String(cost);
  return `₹${Math.round(value)}`;
}
