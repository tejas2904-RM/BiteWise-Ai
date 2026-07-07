"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchRecommendations } from "@/lib/api";
import { consumePendingRequest, saveResults } from "@/lib/storage";
import { LoadingProgress } from "@/components/search/LoadingProgress";

export default function SearchLoadingPage() {
  const router = useRouter();
  const [step, setStep] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setStep(1), 600),
      setTimeout(() => setStep(2), 1200),
    ];

    async function run() {
      const request = consumePendingRequest();
      if (!request) {
        router.replace("/search");
        return;
      }

      try {
        const response = await fetchRecommendations(request, { topN: 5 });
        saveResults(response);
        router.replace("/results");
      } catch (error) {
        const err = error as { code?: string; status?: number };
        if (err.code === "no_matches") {
          router.replace("/results?empty=1");
          return;
        }
        router.replace("/error");
      }
    }

    run();

    return () => timers.forEach(clearTimeout);
  }, [router]);

  return <LoadingProgress activeStep={step} />;
}
