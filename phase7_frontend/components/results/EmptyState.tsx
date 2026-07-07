"use client";

import Link from "next/link";
import { SearchX } from "lucide-react";
import { AITipCard } from "@/components/shared/AICards";

export function EmptyState({
  filters = [],
}: {
  filters?: string[];
}) {
  return (
    <div className="card mx-auto max-w-2xl p-10 text-center">
      <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gray-100">
        <SearchX className="h-10 w-10 text-brand" />
      </div>
      <h2 className="text-3xl font-bold text-ink">No matches found</h2>
      <p className="mt-3 text-muted">
        Your filters may be too specific. Try relaxing them to discover more restaurants in this area.
      </p>

      {filters.length > 0 ? (
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          {filters.map((filter) => (
            <span
              key={filter}
              className="rounded-full border border-gray-200 px-3 py-1 text-sm text-muted"
            >
              {filter}
            </span>
          ))}
        </div>
      ) : null}

      <div className="mt-8 flex flex-wrap justify-center gap-3">
        <Link href="/search" className="rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white">
          Edit preferences
        </Link>
        <Link
          href="/search"
          className="rounded-xl border border-brand px-5 py-3 text-sm font-semibold text-brand"
        >
          Clear all filters
        </Link>
      </div>

      <div className="mt-8 text-left">
        <AITipCard>
          Expanding your radius or lowering the minimum rating might reveal more options nearby.
        </AITipCard>
      </div>
    </div>
  );
}
