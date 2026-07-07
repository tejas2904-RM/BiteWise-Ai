import { AITipCard } from "@/components/shared/AICards";
import { fetchSearchHistory } from "@/lib/api";

export async function SearchWidgets() {
  const history = await fetchSearchHistory(4);

  return (
    <aside className="space-y-4">
      <AITipCard>
        Szechuan spots in Bangalore are trending for dinner. Try increasing your budget slightly for more authentic options.
      </AITipCard>

      <div className="card overflow-hidden">
        <div className="h-36 bg-gradient-to-br from-brand to-brand-light" />
        <div className="p-4">
          <p className="text-sm font-semibold text-ink">Popular Choice</p>
          <p className="text-sm text-muted">ECHOES Koramangala · Chinese</p>
        </div>
      </div>

      <div className="card p-4">
        <p className="font-semibold text-ink">Why Bangalore?</p>
        <p className="mt-2 text-sm text-muted">
          The Garden City boasts hundreds of high-rated restaurants curated by our local AI experts.
        </p>
      </div>

      <div className="card p-4">
        <p className="mb-3 font-semibold text-ink">Recent Searches</p>
        <div className="space-y-2">
          {history.length === 0 ? (
            <p className="text-sm text-muted">No recent searches yet.</p>
          ) : (
            history.map((item) => (
              <div key={`${item.searched_at}-${item.cuisine}`} className="rounded-xl bg-gray-50 px-3 py-2 text-sm text-ink">
                {item.cuisine} in {item.location}
              </div>
            ))
          )}
        </div>
      </div>
    </aside>
  );
}
