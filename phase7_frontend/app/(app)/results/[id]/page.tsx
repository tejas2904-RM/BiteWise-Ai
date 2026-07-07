import { notFound } from "next/navigation";
import { fetchRestaurantDetail } from "@/lib/api";
import { RestaurantDetailView } from "@/components/results/RestaurantDetailView";

export default async function RestaurantDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  try {
    const detail = await fetchRestaurantDetail(id);
    return <RestaurantDetailView detail={detail} />;
  } catch {
    notFound();
  }
}
