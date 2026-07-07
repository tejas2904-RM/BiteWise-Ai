"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";
import { AISummaryBanner } from "@/components/shared/AICards";
import {
  RestaurantCardCompact,
  RestaurantCardFeatured,
  RestaurantCardMedium,
} from "@/components/results/RestaurantCards";
import { EmptyState } from "@/components/results/EmptyState";
import { loadResults, budgetLabel } from "@/lib/storage";
import type { RecommendationResponse } from "@/lib/types";

export default function ResultsContent() {
  const searchParams = useSearchParams();
  const isEmpty = searchParams.get("empty") === "1";
  const [data, setData] = useState<RecommendationResponse | null>(null);

  useEffect(() => {
    setData(loadResults());
  }, []);

  if (isEmpty) {
    return <EmptyState filters={["Chinese", "Medium budget", "4.0+ rating"]} />;
  }

  if (!data) {
    return (
      <div className="card p-10 text-center">
        <p className="text-muted">No results yet. Start a new search to get AI recommendations.</p>
        <Link href="/search" className="mt-4 inline-block rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white">
          Start new search
        </Link>
      </div>
    );
  }

  const prefs = data.preferences;
  const chips = prefs
    ? [prefs.location, prefs.cuisine, budgetLabel(prefs.budget), `${prefs.min_rating}+`]
    : [];

  const [featured, second, ...rest] = data.recommendations;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-bold text-ink">Curated for You</h1>
          <div className="mt-3 flex flex-wrap gap-2">
            {chips.map((chip) => (
              <span key={chip} className="rounded-full bg-white px-3 py-1 text-sm text-muted shadow-sm">
                {chip}
              </span>
            ))}
          </div>
        </div>
        <Link
          href="/search"
          className="inline-flex items-center gap-2 rounded-xl bg-brand px-4 py-2 text-sm font-semibold text-white"
        >
          <RefreshCw className="h-4 w-4" />
          Start new search
        </Link>
      </div>

      {data.summary ? <AISummaryBanner summary={data.summary} /> : null}

      <div className="space-y-6">
        {featured ? <RestaurantCardFeatured item={featured} /> : null}
        {second ? <RestaurantCardMedium item={second} /> : null}
        {rest.map((item) => (
          <RestaurantCardCompact key={item.restaurant_id} item={item} />
        ))}
      </div>

      <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-gray-200 pt-4 text-sm text-muted">
        <span>
          Showing {data.recommendations.length} AI-curated results
          {data.total_matches ? ` from over ${data.total_matches} matches` : ""}
          {data.source === "fallback" ? " (fallback ranking)" : ""}.
        </span>
        <div className="flex gap-4">
          <button type="button">Share Results</button>
          <button type="button">View on Map</button>
        </div>
      </footer>
    </div>
  );
}
