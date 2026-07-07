"use client";

import Link from "next/link";
import { CloudOff, RefreshCw } from "lucide-react";

export default function ErrorPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-surface px-6 py-16">
      <div className="card max-w-2xl p-10 text-center">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-brand-soft">
          <CloudOff className="h-8 w-8 text-brand" />
        </div>
        <h1 className="text-3xl font-bold text-ink">Couldn&apos;t get AI recommendations</h1>
        <p className="mt-3 text-muted">
          Our AI concierge is having trouble connecting to the recommendation service right now.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-2 rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white"
          >
            <RefreshCw className="h-4 w-4" />
            Try again
          </button>
          <Link
            href="/search"
            className="rounded-xl border border-brand px-5 py-3 text-sm font-semibold text-brand"
          >
            View fallback results
          </Link>
        </div>
        <div className="mt-8 rounded-2xl bg-gray-50 p-5 text-left">
          <p className="font-semibold text-ink">What happens next?</p>
          <p className="mt-2 text-sm text-muted">
            You can retry the request or start a new search. Fallback ranking may still return rating-based picks.
          </p>
          <div className="mt-4 space-y-2">
            <div className="h-12 animate-pulse rounded-xl bg-gray-200" />
            <div className="h-12 animate-pulse rounded-xl bg-gray-200" />
          </div>
        </div>
        <Link href="/search" className="mt-6 inline-block text-sm text-brand underline">
          Check system status
        </Link>
      </div>
    </main>
  );
}
