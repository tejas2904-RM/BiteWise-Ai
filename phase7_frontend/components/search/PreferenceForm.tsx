"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Sparkles } from "lucide-react";
import type { BudgetTier, RecommendationRequest } from "@/lib/types";
import { savePendingRequest } from "@/lib/storage";

const cuisines = ["Chinese", "Italian", "North Indian", "Mughlai", "Cafe", "Thai"];

export function PreferenceForm() {
  const router = useRouter();
  const [location, setLocation] = useState("Bangalore");
  const [cuisine, setCuisine] = useState("Chinese");
  const [budget, setBudget] = useState<BudgetTier>("medium");
  const [minRating, setMinRating] = useState(4.0);
  const [notes, setNotes] = useState("family-friendly, quick service");
  const [error, setError] = useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!location.trim() || !cuisine.trim()) {
      setError("Location and cuisine are required.");
      return;
    }

    const request: RecommendationRequest = {
      location: location.trim(),
      cuisine: cuisine.trim(),
      budget,
      min_rating: minRating,
      additional_notes: notes.trim() || null,
    };

    savePendingRequest(request);
    router.push("/search/loading");
  }

  return (
    <form onSubmit={handleSubmit} className="card space-y-5 p-6">
      <div>
        <h1 className="font-display text-3xl font-bold text-ink">Curate Your Experience</h1>
        <p className="mt-2 text-muted">
          Tell BiteWise what you&apos;re craving. Our AI analyzes local spots to find your perfect match.
        </p>
      </div>

      <label className="block space-y-2">
        <span className="text-sm font-semibold text-ink">Location</span>
        <input
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full rounded-xl border border-gray-200 px-4 py-3 outline-none focus:border-brand"
          placeholder="Bangalore"
        />
      </label>

      <label className="block space-y-2">
        <span className="text-sm font-semibold text-ink">Cuisine</span>
        <select
          value={cuisine}
          onChange={(e) => setCuisine(e.target.value)}
          className="w-full rounded-xl border border-gray-200 px-4 py-3 outline-none focus:border-brand"
        >
          {cuisines.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </label>

      <div className="space-y-2">
        <span className="text-sm font-semibold text-ink">Budget</span>
        <div className="grid grid-cols-3 gap-2">
          {([
            ["low", "$ Budget"],
            ["medium", "$$ Medium"],
            ["high", "$$$ Luxury"],
          ] as const).map(([value, label]) => (
            <button
              key={value}
              type="button"
              onClick={() => setBudget(value)}
              className={`rounded-xl border px-3 py-3 text-sm font-medium ${
                budget === value
                  ? "border-brand bg-brand-soft text-brand"
                  : "border-gray-200 text-muted"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      <label className="block space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-sm font-semibold text-ink">Minimum rating</span>
          <span className="text-sm font-semibold text-brand">{minRating.toFixed(1)}+</span>
        </div>
        <input
          type="range"
          min={3}
          max={5}
          step={0.1}
          value={minRating}
          onChange={(e) => setMinRating(parseFloat(e.target.value))}
          className="w-full accent-brand"
        />
      </label>

      <label className="block space-y-2">
        <span className="text-sm font-semibold text-ink">AI personalization notes</span>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={4}
          className="w-full rounded-xl border border-gray-200 px-4 py-3 outline-none focus:border-brand"
          placeholder="E.g., quiet place for a business dinner"
        />
      </label>

      {error ? <p className="text-sm text-brand">{error}</p> : null}

      <button
        type="submit"
        className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand px-4 py-3 font-semibold text-white hover:bg-brand-light"
      >
        <Sparkles className="h-4 w-4" />
        Find restaurants
      </button>
    </form>
  );
}
