import { Lightbulb } from "lucide-react";

export function AITipCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-2xl border border-emerald-100 bg-tip p-4">
      <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-emerald-800">
        <Lightbulb className="h-4 w-4" />
        AI Tip
      </div>
      <p className="text-sm leading-relaxed text-emerald-900">{children}</p>
    </div>
  );
}

export function AISummaryBanner({ summary }: { summary: string }) {
  return (
    <div className="rounded-2xl border border-rose-100 bg-brand-soft p-6">
      <p className="mb-2 text-sm font-semibold text-brand">AI Recommendation Summary</p>
      <p className="leading-relaxed text-ink">{summary}</p>
    </div>
  );
}
