"use client";

import { Suspense } from "react";
import ResultsPage from "./ResultsContent";

export default function ResultsRoute() {
  return (
    <Suspense fallback={<div className="card p-10 text-center text-muted">Loading results…</div>}>
      <ResultsPage />
    </Suspense>
  );
}
