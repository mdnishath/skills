# french-review — Universal French Google Review Writer v3.0

Write authentic French Google My Business reviews for any local business. Supports 30+ industries with Google algorithm bypass, anti-AI-detection, and appeal-proof content strategies.

## Quick Start

```
/french-review 5 five-star reviews for "Business Name" business-type in City
```

## What's New in v3.0

v3.0 is a major update based on Google's 2025-2026 algorithm changes. The previous approach of systematic accent/apostrophe dropping was causing reviews to be flagged and removed.

| Area | v2.0 | v3.0 |
|------|------|------|
| Accents | Drop 55-75% (created bot pattern) | Realistic phone autocorrect — most reviews keep 85%+ accents |
| Apostrophes | Drop 65-85% (created bot pattern) | Varied by persona — careful/average/sloppy typers |
| Detail Level | 1 generic detail | 2+ specificity layers (exact service, business name, outcomes) |
| Cross-Review | Basic variation | Zero phrase repetition across entire batch |
| Appeals | Not addressed | Rule 18: appeal-proof content with personal context |
| Total Rules | 16 | 18 |

## Features

- **18 strict writing rules** for maximum authenticity
- **Realistic phone typing simulation** — accents/apostrophes match how real French people type on phones with autocorrect
- **Mandatory specificity** — every review mentions exact service details, not generic praise
- **Zero repetition engine** — no phrase of 4+ words appears twice in any batch
- **Persona system** — each review gets a unique fictional persona (age, gender, perspective, typing style, phone type)
- **Burstiness engine** — 4 sentence rhythm patterns that beat AI detection
- **Anti-fingerprinting** — no two reviews share the same writing pattern
- **Appeal-proof content** — personal context, service vocabulary, concrete outcomes
- **Stealth mode** — maximum anti-detection with one keyword
- **30+ business types** with industry-specific French vocabulary

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill — 18 rules, persona system, batch protocol, output format |
| `references/business-vocabulary.md` | Industry vocabulary for 30+ business types |
| `references/example-reviews.md` | 35+ gold-standard examples with realistic accent handling |
| `references/opening-templates.md` | 90+ varied opening sentences by star rating |
| `references/anti-detection-strategy.md` | Google bypass, AI detection, appeal-proofing, posting strategy |

## Usage

All input in English. All review output in French.

```
# Basic
/french-review 5 five-star reviews for "Plomberie Martin" plumber in Lyon

# Mixed ratings
/french-review 10 reviews for "Le Bistrot" restaurant, 7 five-star, 2 four-star, 1 three-star

# Stealth mode (max anti-detection)
/french-review 8 reviews for "Garage Auto Plus" mechanic, stealth mode

# With seasonal context
/french-review 6 reviews for "Couverture Martin" roofing in Toulouse, winter storm context

# Negative reviews
/french-review 3 one-star reviews for "Toitures Dupont" roofing company
```

## Supported Business Types

Roofing, Plumbing, Electrical, Tree Services, Carpet/Rug Cleaning, General Renovation, Restaurants, Bakeries, Hair Salons, Auto Mechanics, Moving Companies, Cleaning Services, Landscaping, Locksmiths, Painters, Heating/HVAC, Carpentry, Masonry, Hotels, Real Estate, Driving Schools, Veterinarians, Dentists, Photographers, Catering, Dry Cleaning — and any custom type you describe.

## Anti-Detection Layers

| Layer | What It Does |
|-------|-------------|
| Realistic accents | Simulates phone autocorrect — varied retention rates per review |
| Zero repetition | No phrase appears twice across the batch |
| Mandatory specificity | Every review mentions exact service details |
| Persona diversity | Each review sounds like a different person |
| Burstiness patterns | Varied sentence rhythm beats AI analysis |
| Appeal-proof content | Personal context + service vocabulary |
| Stealth mode | Maximum randomness when activated |

## Install

Copy this folder to your Claude Code skills directory:

```bash
# macOS/Linux
cp -r french-review ~/.claude/skills/french-review

# Windows
xcopy /E /I french-review %USERPROFILE%\.claude\skills\french-review
```

Restart Claude Code. The skill auto-detects on startup.

## Customization

- Add new business types: edit `references/business-vocabulary.md`
- Add opening templates: edit `references/opening-templates.md`
- Add example reviews: edit `references/example-reviews.md`
- Adjust anti-detection rules: edit `references/anti-detection-strategy.md`
- Change core rules: edit `SKILL.md` (careful — rules are tuned together)
