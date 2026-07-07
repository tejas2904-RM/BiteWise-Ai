"use client";

import Image from "next/image";
import Link from "next/link";
import { Heart, MapPin, Star } from "lucide-react";
import type { Recommendation } from "@/lib/types";
import { formatCost } from "@/lib/storage";
import { restaurantImageForId } from "@/lib/images";

function Rating({ value }: { value: number }) {
  return (
    <span className="inline-flex items-center gap-1 text-sm font-semibold text-amber-600">
      <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
      {value.toFixed(1)}
    </span>
  );
}

export function RestaurantCardFeatured({ item }: { item: Recommendation }) {
  return (
    <article className="card overflow-hidden">
      <div className="relative h-64 w-full">
        <Image
          src={restaurantImageForId(item.restaurant_id)}
          alt={item.name}
          fill
          className="object-cover"
        />
        <span className="absolute left-4 top-4 rounded-full bg-amber-400 px-3 py-1 text-xs font-bold text-ink">
          #{item.rank} Recommended
        </span>
      </div>
      <div className="space-y-4 p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-2xl font-bold text-ink">{item.name}</h3>
            <p className="mt-1 text-sm text-muted">
              {item.cuisine} · {formatCost(item.estimated_cost)} for two
            </p>
          </div>
          <Rating value={item.rating} />
        </div>
        <div className="rounded-2xl bg-tip p-4 text-sm leading-relaxed text-emerald-900">
          {item.explanation}
        </div>
        <div className="flex gap-3">
          <Link
            href={`/results/${item.restaurant_id}`}
            className="flex-1 rounded-xl bg-brand px-4 py-3 text-center text-sm font-semibold text-white"
          >
            Book a Table
          </Link>
          <button className="rounded-xl border border-gray-200 px-4 py-3 text-brand">
            <Heart className="h-4 w-4" />
          </button>
        </div>
      </div>
    </article>
  );
}

export function RestaurantCardMedium({ item }: { item: Recommendation }) {
  return (
    <article className="card overflow-hidden">
      <div className="relative h-48 w-full">
        <Image
          src={restaurantImageForId(item.restaurant_id)}
          alt={item.name}
          fill
          className="object-cover"
        />
        <span className="absolute left-4 top-4 rounded-full bg-sky-600 px-3 py-1 text-xs font-bold text-white">
          #{item.rank}
        </span>
      </div>
      <div className="space-y-4 p-5">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-ink">{item.name}</h3>
          <Rating value={item.rating} />
        </div>
        <p className="text-sm text-muted">{item.cuisine}</p>
        <div className="rounded-2xl bg-tip p-3 text-sm text-emerald-900">{item.explanation}</div>
        <Link
          href={`/results/${item.restaurant_id}`}
          className="block rounded-xl border border-brand px-4 py-3 text-center text-sm font-semibold text-brand"
        >
          View Details
        </Link>
      </div>
    </article>
  );
}

export function RestaurantCardCompact({ item }: { item: Recommendation }) {
  return (
    <article className="card flex flex-col gap-4 p-4 md:flex-row md:items-center">
      <div className="relative h-28 w-full shrink-0 overflow-hidden rounded-xl md:h-24 md:w-32">
        <Image
          src={restaurantImageForId(item.restaurant_id)}
          alt={item.name}
          fill
          className="object-cover"
        />
      </div>
      <div className="flex-1 space-y-2">
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-bold text-ink">{item.name}</h3>
          <Rating value={item.rating} />
        </div>
        <p className="text-sm text-muted">{item.cuisine}</p>
        <p className="text-sm text-muted line-clamp-2">{item.explanation}</p>
      </div>
      <div className="flex gap-2 md:flex-col">
        <Link
          href={`/results/${item.restaurant_id}`}
          className="rounded-xl border border-gray-200 px-4 py-2 text-center text-sm font-semibold text-ink"
        >
          View Menu
        </Link>
        <Link
          href={`/results/${item.restaurant_id}`}
          className="rounded-xl bg-brand px-4 py-2 text-center text-sm font-semibold text-white"
        >
          Book Now
        </Link>
      </div>
    </article>
  );
}

export function RestaurantDetailPanel({
  name,
  cuisines,
  rating,
  explanation,
  address,
  cost,
}: {
  name: string;
  cuisines: string[];
  rating: number;
  explanation: string;
  address?: string | null;
  cost: number;
}) {
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-2">
        {cuisines.map((tag) => (
          <span key={tag} className="rounded-full bg-gray-100 px-3 py-1 text-sm text-ink">
            {tag}
          </span>
        ))}
      </div>

      <div className="rounded-2xl border border-teal-100 bg-ai p-5">
        <p className="mb-2 text-sm font-semibold text-teal-800">Why we recommend this</p>
        <p className="text-sm leading-relaxed text-teal-900">{explanation}</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl bg-gray-50 p-4">
          <p className="text-sm font-semibold text-ink">Must Try</p>
          <p className="mt-2 text-sm text-muted">Chef&apos;s special tasting menu · ₹{Math.round(cost * 0.3)}</p>
        </div>
        <div className="rounded-2xl bg-gray-50 p-4">
          <p className="text-sm font-semibold text-ink">Perfect For</p>
          <p className="mt-2 text-sm text-muted">Family dinners, weekend brunch, casual meetups</p>
        </div>
      </div>

      {address ? (
        <div className="flex items-start gap-2 text-sm text-muted">
          <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-brand" />
          <span>{address}</span>
        </div>
      ) : null}

      <div className="flex flex-wrap gap-3">
        <button className="rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white">
          Open in Maps
        </button>
        <button className="rounded-xl border border-gray-200 px-5 py-3 text-sm font-semibold text-ink">
          Call Now
        </button>
        <button className="rounded-xl border border-gray-200 px-5 py-3 text-sm font-semibold text-ink">
          Share
        </button>
      </div>
    </div>
  );
}
