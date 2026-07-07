# Google Stitch UI Prompts — AI Restaurant Recommendation System

Use these prompts in [Google Stitch](https://stitch.withgoogle.com) to generate UI mockups for the Zomato-inspired, AI-powered restaurant recommendation app. Generated designs will be implemented in **Next.js** (see [PhaseWiseArchitecture.md](./PhaseWiseArchitecture.md)).

## How to use

1. Open Google Stitch and choose **Mobile** or **Web** (designs should translate to responsive Next.js pages).
2. Start with **Project context** (copy once) so designs stay consistent.
3. Generate **one screen per prompt** — avoid combining multiple screens in a single prompt.
4. Refine with the **Follow-up refinement prompts** at the bottom (one change at a time).
5. Export to Figma or HTML, then rebuild as Next.js components (`app/`, `components/`).

---

## Project context (paste first or include in every prompt)

```text
App name: BiteWise
Product: AI-powered restaurant recommendation app inspired by Zomato (India).
Frontend implementation: Next.js (App Router, TypeScript, Tailwind CSS) — designs should map to reusable React components.
Target users: Urban diners in Indian cities (e.g. Bangalore, Delhi) looking for personalized restaurant picks.
Core flow: User enters preferences → system filters restaurants → OpenAI ranks and explains top options → user compares results.
Brand vibe: Modern, trustworthy, food-forward, clean — not cluttered like a marketplace homepage.
Design system:
- Primary color: warm red/coral (#E23744, Zomato-adjacent but original)
- Secondary: deep charcoal text (#1C1C1C), soft gray backgrounds (#F5F5F5)
- Accent: amber for ratings (★), green for positive AI insights
- Typography: rounded sans-serif (similar to Inter or Poppins)
- Components: rounded cards (12–16px radius), soft shadows, generous whitespace
- Platform: mobile-first, 390px width, iOS-style status bar
Use realistic Indian restaurant dummy data (Bangalore, Chinese cuisine, ₹ symbols for cost).
```

---

## Screen 1 — Landing / Home

```text
Design a mobile landing screen for "BiteWise", an AI restaurant recommendation app.

Layout:
- Sticky top bar with app logo (fork + sparkle icon) and wordmark "BiteWise"
- Hero section with headline: "Find your perfect meal, powered by AI"
- Subtext: "Tell us what you crave. We'll recommend the best restaurants near you."
- Illustration area: minimal flat illustration of Indian city skyline + food icons (no stock photos)
- Primary CTA button (full width): "Get Recommendations"
- Secondary text link: "How it works"
- Bottom section with 3 small feature chips in a horizontal row: "Smart filters", "AI explanations", "Top-rated picks"

Style: warm, appetizing, minimal, lots of white space, coral primary button, dark text.
Include realistic placeholder content. No lorem ipsum.
```

---

## Screen 2 — Preference input form

```text
Design a mobile "Restaurant Preferences" form screen for BiteWise.

Layout (scrollable, stacked form):
- Header: back arrow + title "Your preferences"
- Short helper text: "We'll use these to find restaurants that match you."
- Form fields with clear labels:
  1. Location — text input, placeholder "Bangalore", map pin icon
  2. Cuisine — text input with cuisine icon, placeholder "Chinese"
  3. Budget — segmented control or dropdown: Low | Medium | High
  4. Minimum rating — slider or stepper from 0 to 5, default 4.0, star icon
  5. Additional notes — multiline textarea, placeholder "family-friendly, quick service"
- Sticky bottom primary CTA: "Find restaurants"
- Small validation hint area below submit (empty state, subtle gray)

Style: clean form UI, labeled inputs, coral accent on focused fields and CTA, card-style input containers on light gray background.
Pre-fill dummy values: Bangalore, Chinese, Medium, 4.0.
```

---

## Screen 3 — Loading / AI processing

```text
Design a mobile loading screen for BiteWise while AI recommendations are being generated.

Layout:
- Centered animated-style illustration (subtle pulse or sparkle around a plate icon — static mockup is fine)
- Headline: "Finding the best spots for you…"
- Three-step progress list (vertical):
  1. "Filtering restaurants in Bangalore" — checkmark (completed)
  2. "Matching your taste profile" — checkmark (completed)
  3. "AI is ranking top picks" — spinner (in progress)
- Subtext: "This usually takes a few seconds"
- Skeleton preview: 2 faded restaurant card placeholders below

Style: calm, reassuring, coral accent on active step, light background, no harsh loaders.
```

---

## Screen 4 — Recommendations results (main screen)

```text
Design a mobile recommendations results screen for BiteWise.

Layout:
- Sticky header: "Your matches" + filter chips row showing active preferences: "Bangalore · Chinese · ₹₹ · 4.0+"
- AI summary card at top (soft coral tint background):
  - Small "AI Summary" label with sparkle icon
  - Text: "Three strong Chinese options in Bangalore within your budget. ECHOES Koramangala leads on rating; Baar Union offers a lively bar vibe."
- Ranked restaurant cards (vertical list, 3 cards):

  Card #1 (highlighted):
  - Rank badge "1" in coral circle
  - Restaurant name: "ECHOES Koramangala"
  - Row: ★ 4.7 · Chinese · ₹750 for two
  - Location chip: "Koramangala, Bangalore"
  - AI explanation quote in italics: "Great for groups and families — high rating with varied Chinese-American menu."
  - Small chevron or "View details" link

  Card #2:
  - Rank "2", name "Baar Union", ★ 4.6, Chinese, ₹850, explanation snippet

  Card #3:
  - Rank "3", name "Pin Me Down", ★ 4.5, Chinese, ₹800, explanation snippet

- Bottom fixed button: "Start new search"

Style: card-based layout, clear hierarchy, star ratings in amber, cost in gray, AI explanations visually distinct from metadata.
Use realistic Indian restaurant names and rupee pricing.
```

---

## Screen 5 — Restaurant detail (optional expand)

```text
Design a mobile restaurant detail bottom sheet for BiteWise (slides up from results list).

Layout:
- Drag handle at top
- Restaurant hero: name "ECHOES Koramangala", large rating ★ 4.7, "750 reviews"
- Tags row: Chinese, American, Casual Dining, Medium budget
- Info rows with icons: location, cost for two ₹750, online order Yes
- Section "Why we recommend this" with AI icon and full explanation paragraph
- Primary CTA: "Open in Maps" (secondary style)
- Text button: "Back to results"

Style: bottom sheet modal, white surface, rounded top corners 24px, coral accents on rank badge and CTA outline.
```

---

## Screen 6 — Empty state (no matches)

```text
Design a mobile empty state screen for BiteWise when no restaurants match the filters.

Layout:
- Centered illustration: empty plate or map pin with question mark (friendly, not sad)
- Headline: "No matches found"
- Body: "We couldn't find restaurants in Bangalore for Chinese with a 4.5+ rating and medium budget. Try relaxing your filters."
- Suggestion chips (tappable): "Lower rating to 4.0", "Try nearby locality", "Change cuisine"
- Primary CTA: "Edit preferences"
- Secondary link: "Start over"

Style: light and helpful, soft gray illustration, coral CTA, no alarming red error styling.
```

---

## Screen 7 — Error state (OpenAI / network failure)

```text
Design a mobile error state screen for BiteWise when the AI recommendation service fails.

Layout:
- Centered icon: cloud with warning (subtle, not aggressive)
- Headline: "Couldn't get AI recommendations"
- Body: "We're having trouble reaching our recommendation service. You can try again or view basic ranked results."
- Small info card showing fallback message: "Showing rating-based picks instead"
- Primary CTA: "Try again"
- Secondary CTA: "View fallback results"

Style: neutral error tone (amber/warm gray, not bright red), reassuring copy, clear recovery actions.
```

---

## Web dashboard variant (Next.js desktop layout)

```text
Design a desktop web app (1440px) for BiteWise — this will be implemented as a Next.js App Router layout.

Layout:
- Left sidebar (240px): logo, nav items — Home, New search, History
- Main content (2-column on large screens):
  - Left column (40%): preference form (location, cuisine, budget, rating, notes) + "Get recommendations" button
  - Right column (60%): results panel with AI summary banner + 3 restaurant cards in a vertical list
- Top bar: user avatar placeholder, city selector "Bangalore"

Style: modern SaaS dashboard, white cards on #F8F8F8 background, coral primary actions, responsive grid.
Include same dummy data as mobile results screen.
```

---

## Dummy data reference (use across all screens)

| Field | Sample value |
|-------|----------------|
| Location | Bangalore |
| Cuisine | Chinese |
| Budget | Medium (₹₹) |
| Min rating | 4.0 |
| Notes | family-friendly, quick service |
| Restaurant 1 | ECHOES Koramangala — ★ 4.7 — ₹750 — Chinese, American |
| Restaurant 2 | Baar Union — ★ 4.6 — ₹850 — Chinese, Asian |
| Restaurant 3 | Pin Me Down — ★ 4.5 — ₹800 — Chinese, Cafe |

---

## Follow-up refinement prompts (use one at a time)

**Dark mode**
```text
Convert this screen to dark mode. Background #121212, cards #1E1E1E, text white, keep coral #E23744 as primary accent. Ensure WCAG 2.1 contrast on body text.
```

**Typography**
```text
Use Poppins for headings and Inter for body text. Increase line height on AI explanation text for readability.
```

**More premium feel**
```text
Make the UI feel more premium: softer shadows, more padding, subtle gradient on hero and summary card, refined icon style.
```

**Accessibility**
```text
Increase tap target sizes to 44px minimum, add visible focus states on form fields, ensure color is not the only indicator for rating or budget tier.
```

**Localization**
```text
Add Indian context: use ₹ for currency, show locality names like Koramangala and Indiranagar, keep labels in English.
```

**Results card polish**
```text
On the recommendations screen only: add a small restaurant thumbnail placeholder on each card, show rank badge overlapping the image corner, and truncate AI explanation to 2 lines with "Read more".
```

---

## Screen checklist for Phase 5

| Screen | Phase | Next.js route (planned) | Stitch prompt |
|--------|-------|---------------------------|---------------|
| Landing | Entry | `app/page.tsx` | Screen 1 |
| Preference form | Phase 2 | `app/search/page.tsx` | Screen 2 |
| Loading state | Phase 3–4 | `app/search/loading.tsx` | Screen 3 |
| Recommendations list | Phase 5 | `app/results/page.tsx` | Screen 4 |
| Empty state | Phase 5 | `app/results` (empty UI) | Screen 6 |
| Error state | Phase 5 | `app/error.tsx` | Screen 7 |

---

## Related documents

- [Problem Statement](./Problemstatment.md)
- [Phase-Wise Architecture](./PhaseWiseArchitecture.md)
