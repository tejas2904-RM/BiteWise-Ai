import { PreferenceForm } from "@/components/search/PreferenceForm";
import { SearchWidgets } from "@/components/search/SearchWidgets";

export default function SearchPage() {
  return (
    <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
      <PreferenceForm />
      <SearchWidgets />
    </div>
  );
}
