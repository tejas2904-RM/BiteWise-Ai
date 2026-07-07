"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Clock3,
  Home,
  Search,
  Sparkles,
  User,
} from "lucide-react";

const navItems = [
  { href: "/", label: "Home", icon: Home },
  { href: "/search", label: "New Search", icon: Search },
  { href: "/results", label: "History", icon: Clock3 },
  { href: "/search", label: "Profile", icon: User },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-60 shrink-0 flex-col border-r border-gray-200 bg-white lg:flex">
      <div className="border-b border-gray-100 px-6 py-6">
        <p className="font-display text-xl font-bold text-brand">BiteWise</p>
        <p className="text-sm text-muted">AI Concierge</p>
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-4">
        {navItems.map((item) => {
          const active =
            item.label === "New Search"
              ? pathname.startsWith("/search")
              : item.label === "Home"
                ? pathname === "/"
                : pathname.startsWith(item.href) && item.href !== "/";

          const Icon = item.icon;
          return (
            <Link
              key={item.label}
              href={item.href}
              className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                active
                  ? "bg-brand text-white"
                  : "text-ink hover:bg-gray-50"
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="space-y-4 p-4">
        <div className="rounded-2xl bg-brand-soft p-4">
          <p className="text-sm font-medium text-ink">Get smarter dining insights</p>
          <button className="mt-3 w-full rounded-xl bg-brand px-4 py-2 text-sm font-semibold text-white">
            Upgrade to Pro
          </button>
        </div>
        <div className="flex items-center gap-3 rounded-2xl border border-gray-100 p-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-brand text-sm font-bold text-white">
            AR
          </div>
          <div>
            <p className="text-sm font-semibold text-ink">Alex Robertson</p>
            <p className="text-xs text-muted">Member since 2023</p>
          </div>
        </div>
      </div>
    </aside>
  );
}

export function MobileNav() {
  const pathname = usePathname();

  return (
    <div className="flex gap-2 overflow-x-auto border-b border-gray-200 bg-white p-3 lg:hidden">
      {navItems.slice(0, 4).map((item) => {
        const active = pathname.startsWith(item.href) && item.href !== "/";
        return (
          <Link
            key={item.label}
            href={item.href}
            className={`whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium ${
              active ? "bg-brand text-white" : "bg-gray-100 text-ink"
            }`}
          >
            {item.label}
          </Link>
        );
      })}
    </div>
  );
}

export function TopBar({ location = "Bangalore" }: { location?: string }) {
  return (
    <header className="flex items-center justify-between border-b border-gray-200 bg-white px-6 py-4">
      <div className="flex items-center gap-2 text-sm text-muted">
        <Sparkles className="h-4 w-4 text-brand" />
        <span>{location}</span>
      </div>
      <div className="flex items-center gap-3">
        <div className="hidden h-9 w-48 rounded-full bg-gray-100 md:block" />
        <div className="h-9 w-9 rounded-full bg-brand-soft" />
      </div>
    </header>
  );
}
