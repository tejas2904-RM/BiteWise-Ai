import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-white">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
        <p className="font-display text-2xl font-bold text-brand">BiteWise</p>
        <nav className="hidden gap-6 text-sm text-muted md:flex">
          <Link href="/" className="border-b-2 border-brand text-ink">
            Home
          </Link>
          <Link href="/search">Explore</Link>
          <Link href="/results">Cuisines</Link>
        </nav>
      </header>

      <section className="mx-auto grid max-w-6xl gap-10 px-6 py-12 lg:grid-cols-2 lg:items-center">
        <div>
          <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700">
            New: AI Curation 2.0
          </span>
          <h1 className="mt-4 font-display text-5xl font-bold leading-tight text-ink">
            Find your perfect meal, powered by <span className="text-brand">AI</span>
          </h1>
          <p className="mt-4 max-w-xl text-lg text-muted">
            Tell us what you crave. BiteWise filters thousands of restaurants and explains the best matches for you.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href="/search"
              className="inline-flex items-center gap-2 rounded-xl bg-brand px-5 py-3 font-semibold text-white"
            >
              Get Recommendations
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/results"
              className="rounded-xl border border-gray-200 px-5 py-3 font-semibold text-ink"
            >
              View AI Analysis
            </Link>
          </div>
          <div className="mt-6 flex flex-wrap gap-2">
            {["Smart filters", "AI explanations", "Top-rated picks"].map((chip) => (
              <span key={chip} className="rounded-full bg-gray-100 px-3 py-1 text-sm text-muted">
                {chip}
              </span>
            ))}
          </div>
        </div>

        <div className="card relative min-h-80 overflow-hidden bg-gradient-to-br from-brand-soft to-white p-8">
          <Sparkles className="h-10 w-10 text-brand" />
          <p className="mt-6 text-2xl font-bold text-ink">Taste of India · AI Pick</p>
          <p className="mt-2 text-muted">Personalized rankings with OpenAI explanations</p>
        </div>
      </section>

      <section className="bg-surface px-6 py-16">
        <div className="mx-auto max-w-6xl">
          <h2 className="font-display text-3xl font-bold text-ink">Why BiteWise?</h2>
          <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {[
              "Deep flavor analysis across cuisines",
              "Smart concierge powered by OpenAI",
              "Real-time data from Zomato dataset",
              "Curated collections for every mood",
            ].map((item) => (
              <div key={item} className="card p-5">
                <p className="font-semibold text-ink">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-gray-200 px-6 py-8 text-center text-sm text-muted">
        © 2024 BiteWise AI Concierge. All tastes reserved.
      </footer>
    </main>
  );
}
