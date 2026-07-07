"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import type { RestaurantDetail } from "@/lib/types";
import { loadResults } from "@/lib/storage";
import { RestaurantDetailPanel } from "@/components/results/RestaurantCards";

export function RestaurantDetailView({ detail }: { detail: RestaurantDetail }) {
  const [explanation, setExplanation] = useState(
    "A strong match for your preferences with excellent ratings and a menu that fits your selected cuisine.",
  );

  useEffect(() => {
    const results = loadResults();
    const match = results?.recommendations.find(
      (item) => item.restaurant_id === detail.id,
    );
    if (match?.explanation) {
      setExplanation(match.explanation);
    }
  }, [detail.id]);

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted">Restaurant detail</p>
          <h1 className="font-display text-3xl font-bold text-ink">{detail.name}</h1>
          <p className="mt-1 text-muted">
            {detail.location} · ★ {detail.rating.toFixed(1)}
          </p>
        </div>
        <Link href="/results" className="text-sm font-semibold text-brand">
          Back to results
        </Link>
      </div>

      <RestaurantDetailPanel
        name={detail.name}
        cuisines={detail.cuisines}
        rating={detail.rating}
        explanation={explanation}
        address={detail.address}
        cost={detail.cost_for_two}
      />
    </div>
  );
}
