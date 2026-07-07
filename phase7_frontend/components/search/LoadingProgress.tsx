"use client";

const steps = [
  "Filtering restaurants in your area",
  "Matching your taste profile",
  "AI ranking top picks",
];

export function LoadingProgress({ activeStep = 2 }: { activeStep?: number }) {
  return (
    <div className="mx-auto max-w-xl space-y-8 py-16 text-center">
      <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-brand-soft text-2xl font-bold text-brand">
        BW
      </div>
      <div>
        <h1 className="font-display text-3xl font-bold text-ink">Finding the best spots for you…</h1>
        <p className="mt-2 text-muted">This usually takes a few seconds</p>
      </div>

      <div className="space-y-3 text-left">
        {steps.map((step, index) => {
          const done = index < activeStep;
          const current = index === activeStep;
          return (
            <div
              key={step}
              className={`rounded-2xl border px-4 py-3 text-sm ${
                done
                  ? "border-emerald-200 bg-tip text-emerald-900"
                  : current
                    ? "border-brand bg-brand-soft text-brand"
                    : "border-gray-200 bg-white text-muted"
              }`}
            >
              {step}
            </div>
          );
        })}
      </div>

      <div className="space-y-3">
        {[1, 2, 3].map((item) => (
          <div key={item} className="h-24 animate-pulse rounded-2xl bg-gray-200" />
        ))}
      </div>
    </div>
  );
}
