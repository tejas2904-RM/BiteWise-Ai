export const RESTAURANT_IMAGES = [
  "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80",
  "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&q=80",
  "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80",
  "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&q=80",
  "https://images.unsplash.com/photo-1466978913421-9ad636ef5ea1?w=800&q=80",
];

export function restaurantImage(index: number): string {
  return RESTAURANT_IMAGES[index % RESTAURANT_IMAGES.length];
}

export function restaurantImageForId(restaurantId: string): string {
  let hash = 0;
  for (let i = 0; i < restaurantId.length; i += 1) {
    hash = (hash + restaurantId.charCodeAt(i)) % RESTAURANT_IMAGES.length;
  }
  return RESTAURANT_IMAGES[hash];
}
