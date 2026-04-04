# Anti-Detection, Anti-Spam & Anti-Shadow-Ban Strategy Guide v3.0

**v3.0 UPDATE:** Major revision based on Google's 2025-2026 algorithm changes. Previous strategy of systematic accent/apostrophe dropping was CAUSING detection. New strategy focuses on realistic phone typing behavior, mandatory specificity, and zero cross-review repetition.

---

## SECTION 1: GOOGLE SPAM FILTER TRIGGERS (what gets reviews removed or shadow-banned)

### Hard triggers (instant removal or flag):
- Multiple reviews from same IP in short time
- Reviews posted seconds/minutes apart (posting speed)
- Identical or near-identical text across businesses
- Reviews with URLs or links
- Reviews mentioning competitors by name
- Reviews with phone numbers or email addresses
- Reviews containing promotional language ("promo", "reduction", "code")
- Reviews that are copy-pasted (identical character patterns)
- Reviews from brand-new Google accounts with no history
- **NEW: Reviews with SYSTEMATIC accent/apostrophe dropping** — Google now detects when multiple reviews consistently drop accents the same way (bot signature)
- **NEW: Reviews that are TOO GENERIC** — content that could apply to any business type gets flagged as templated
- **NEW: Repeated phrases across reviews for same business** — even 4-word repeated phrases trigger the coordinated-review detector

### Soft triggers (accumulate into shadow-ban):
- All reviews being exactly the same star rating (all 5-star = suspicious)
- All reviews having similar word count (e.g., all 45-50 words)
- All reviews using similar sentence structure
- Reviews appearing on same day for same business
- Reviews with no profile photo on the account
- Reviews where the reviewer has only reviewed one business
- Reviews with perfect grammar and spelling (ironically)
- Reviews that read like marketing copy
- Repetitive praise phrases across reviews for same business
- **NEW: All reviews having the same accent/apostrophe pattern** — real people type differently, so uniform patterns = same source
- **NEW: Reviews lacking personal context** — real customers mention WHY they needed the service

### Shadow-ban indicators (reviews posted but not visible to public):
- Review shows in your account but not on the business page
- Review count on business page doesn't increase
- Review disappears after 24-48 hours

---

## SECTION 2: ACCENT & APOSTROPHE STRATEGY (CRITICAL v3.0 UPDATE)

### Why the old strategy failed:
The v2.0 strategy dropped 55-75% of accents and 65-85% of apostrophes in EVERY review. This created a DETECTABLE PATTERN:
- Google's algorithm saw that ALL reviews for the business had the same typing style
- Manual review teams saw consistent accent dropping as evidence of single-source generation
- Appeals failed because the pattern was obvious to human reviewers

### Why real French people keep accents:
1. **iPhone/Samsung French keyboard autocorrect** adds accents automatically for common words (été, très, après, problème, déçu, équipe)
2. **Predictive text** suggests accented versions first
3. **Only very fast/careless typers** consistently skip accents
4. **Even careless typers are inconsistent** — they might type "été" correctly but miss "problème"

### New accent/apostrophe strategy:
**Create a REALISTIC MIX that simulates different people with different phones and typing habits:**

| Typer Profile | Accent Retention | Apostrophe Retention | % of Batch |
|---------------|-----------------|---------------------|------------|
| Careful (iPhone autocorrect) | 85-95% | 90-100% | 35-40% |
| Average (some misses) | 60-75% | 70-85% | 30-35% |
| Sloppy (old phone/lazy) | 40-55% | 45-65% | 20-25% |
| Desktop/very careful | 95-100% | 95-100% | 5-10% |

**Key principle:** In any batch, reviews should look like they came from DIFFERENT DEVICES and DIFFERENT PEOPLE. Some will be nearly perfect French, some will be messy.

---

## SECTION 3: SPECIFICITY STRATEGY (NEW — ANTI-GENERIC)

### Why generic reviews get removed:
Google's content quality filter checks whether a review provides VALUE to future customers. If a review says nothing specific about the business, it adds no value and gets flagged.

**What Google's algorithm checks:**
1. Does the review mention service-specific vocabulary? (e.g., "tuiles", "faîtage", "solin" for roofing)
2. Does the review describe a specific interaction or outcome?
3. Could this exact review text be posted on any other business page?

### How to make reviews specific:
Every review must include at least 2 specificity elements:

**Element 1: Service-specific vocabulary** (MANDATORY)
Use 2-4 terms from the business type vocabulary. For roofing: `tuiles`, `ardoises`, `faîtage`, `gouttière`, `solin`, `zinguerie`, `démoussage`, `hydrofuge`. NOT just "toit" or "toiture".

**Element 2: Concrete outcome** (highly recommended)
- NOT: "bon travail" → YES: "plus aucune fuite depuis la pluie de la semaine dernière"
- NOT: "résultat nickel" → YES: "les tuiles sont bien alignées et le zinc brille"
- NOT: "content du résultat" → YES: "la gouttière évacue bien même quand il pleut fort"

**Element 3: Interaction detail** (use in 40%+ of reviews)
- "il a pris des photos du toit avant de commencer"
- "Mohamed m'a bien expliqué pourquoi le solin fuyait"
- "ils ont protégé la terrasse avec une bâche pendant les travaux"

**Element 4: Personal context** (use in 50%+ of reviews)
- WHY they needed the service: "suite aux grosses pluies de février"
- Life situation: "on venait d'acheter la maison"
- Previous experience: "après un premier couvreur qui avait mal fait"

---

## SECTION 4: AI CONTENT DETECTION BYPASS — DEEP STRATEGY

### Why AI detectors flag text:
AI detectors (GPTZero, Originality.ai, ZeroGPT, Copyleaks) look for:
1. **Perplexity** — How predictable is the next word? AI text is MORE predictable. Human text is LESS predictable.
2. **Burstiness** — Humans write in bursts (short sentence, then long, then medium). AI writes uniformly.
3. **Token patterns** — AI tends to use certain word combinations more frequently.
4. **Vocabulary distribution** — AI uses a "safe middle" vocabulary. Humans use weird specific words.
5. **Sentence structure** — AI alternates but in a PATTERN. Humans are truly random.

### How we beat each detection vector:

#### A. INCREASE PERPLEXITY (make next word unpredictable)
- Use unexpected word choices: `nickel` instead of `parfait`, `au top` instead of `excellent`
- Drop words that would "normally" follow: instead of `le travail a été très bien fait` say `le boulot est nickel`
- Use spoken French shortcuts that AI models don't naturally produce: `ya`, `quon`, `ça`
- Insert filler words in unexpected positions: `franchement le toit ça va maintenant`
- Use regional expressions when appropriate: `pas mal du tout`, `ça roule`, `impec`

#### B. MAXIMIZE BURSTINESS (varied sentence rhythm)
- Pattern to follow in EVERY review: SHORT. LONG with detail and explanation that flows naturally. MEDIUM.
- Example rhythm: `travail propre. le couvreur est arrivé tôt le matin et a tout fini avant midi sans laisser de déchets sur le terrain. tarif correct et équipe sympa.`
- NEVER: three medium sentences in a row. NEVER: all short. NEVER: all long.
- Ideal mix per review: 1 sentence under 8 words + 1 sentence over 15 words + 1-2 medium sentences

#### C. BREAK TOKEN PATTERNS
- Never write `je recommande cette entreprise` — too common in AI output
- Never write `le travail a été fait dans les règles de l'art` — classic AI phrase
- Avoid `de plus` — use `en plus` or nothing
- Avoid `néanmoins` or `cependant` — use `mais bon` or `après`
- Avoid `en ce qui concerne` — NEVER in a casual review
- Avoid `il est important de noter` — NEVER
- Avoid starting consecutive sentences with the same word
- Avoid `tout d'abord... ensuite... enfin` structure — feels like essay writing

#### D. USE HUMAN-SPECIFIC VOCABULARY
Words that AI rarely generates but humans commonly use in French reviews:
- `nickel`, `top`, `au poil`, `impec`, `ouf`, `dingue`, `relou`
- `ça envoie`, `ça déchire`, `trop bien`, `au top du top`
- `bof`, `mouais`, `meh`, `pas ouf`, `moyen moyen`
- `galère`, `la lose`, `la cata`, `n'importe quoi`
- `rdv` instead of `rendez-vous`
- `tel` instead of `téléphone`
- `aprem` instead of `après-midi`
- Abbreviations: `tjs` (toujours), `bcp` (beaucoup) — use VERY sparingly, max 1 per review

#### E. ENTROPY INJECTION (randomness)
- Occasionally misspell a common word slightly: `vraiement` instead of `vraiment` (very rare, max 1 per 5 reviews)
- Randomly capitalize or not at start of review (some people don't capitalize first word)
- Sometimes start with lowercase, sometimes uppercase — vary across batch
- Occasionally use a number: `2 jours`, `3 fois`, `en 1h` instead of spelled out
- Space inconsistencies: sometimes tight, sometimes extra space after comma

---

## SECTION 5: ZERO REPETITION STRATEGY (NEW — CRITICAL)

### Why cross-review repetition kills reviews:
Google's coordinated-review detector compares all reviews for a business and flags when:
- The same phrase of 4+ words appears in multiple reviews
- The same sentence structure is used across reviews
- The same emotional arc appears (positive context → praise → recommendation)
- The same filler words appear in the same positions

### Repetition avoidance techniques:

#### A. PHRASE SUBSTITUTION MAP
For every common praise, have 5+ unique alternatives:

| Concept | Alternatives (use only ONE per batch) |
|---------|--------------------------------------|
| Good work | `boulot propre`, `bien fait`, `résultat nickel`, `du bon travail`, `c'est du solide`, `travail soigné` |
| I recommend | `à recommander`, `j'y referai appel`, `bonne adresse`, `on les rappellera`, `je garde le numéro`, just end without recommending |
| Nice team | `bon contact`, `le gars était sympa`, `personnel agréable`, `bonne ambiance`, `ils sont accueillants`, `équipe pro` |
| Good price | `correct niveau budget`, `pas de surprise sur la facture`, `devis respecté`, `tarif raisonnable`, `honnête pour le boulot fait` |
| Fast service | `intervention rapide`, `ils sont venus vite`, `réactifs`, `pas eu à attendre longtemps`, `dispo rapidement` |
| Clean work | `chantier propre après`, `ils ont tout nettoyé`, `pas de dégâts`, `tout était rangé en partant`, `rien à nettoyer après` |

#### B. STRUCTURE VARIATION
Never use the same sentence skeleton twice:
- "le [métier] est [venu/arrivé] [quand] et [résultat]" — use this structure ONCE max
- "[Service] fait en [durée], [qualité], [prix]" — use this structure ONCE max
- "suite à [problème], [action], [résultat]" — use this structure ONCE max

#### C. ENDING VARIATION
Each review must end differently. Never repeat an ending type:
- Recommendation: `je recommande` / `à recommander` / `bonne adresse`
- Future intention: `on refera appel` / `j'y retournerai` / `je garde le numéro`
- Result statement: `plus aucun problème depuis` / `tout fonctionne nickel` / `le résultat est là`
- Feeling: `vraiment content` / `pas déçu` / `soulagé`
- Abrupt (no conclusion): just stop after last fact
- Warning (negative): `à éviter` / `fuyez` / `plus jamais`

---

## SECTION 6: ANTI-SPAM POSTING STRATEGY (for the user, not the text)

### Posting rhythm recommendations:
- Maximum 2 reviews per business per day
- Space reviews at least 4-6 hours apart
- Never post all reviews for one business on the same day
- Alternate between businesses when posting batches
- Best posting times: 9-11am, 2-4pm, 7-9pm (when real people post)
- Avoid posting at 3am or midnight (suspicious timing)

### Account health rules:
- Each Google account should review multiple businesses (not just target ones)
- Mix in real reviews for real businesses you visited
- Accounts should have profile photos
- Accounts should have some Google Maps activity (photos, questions answered)
- Don't use brand-new accounts — let them age at least 2-4 weeks
- One account should NOT post more than 3-5 reviews per week

### Location considerations (CRITICAL):
- **IP Address:** Review should come from an IP address in the same COUNTRY as the business, ideally same region
- **GPS data:** If posting from a phone, Google checks if the device was near the business location
- **Device history:** Google tracks if the account has Google Maps activity in the area
- **VPN warning:** Using VPN to France is NOT enough — Google can detect VPN IPs and flags them
- **Best practice:** If possible, have reviews posted by people who are actually IN France or the target country

### Batch diversification:
- In a batch of 10 reviews for same business: vary word count from 25 to 75
- Never have two consecutive reviews with same star rating
- Mix sentence count: some reviews 2 sentences, some 4 sentences
- Alternate between male/female perspectives
- Alternate between single person and couple/family
- **CRITICAL: Vary accent/apostrophe patterns dramatically across the batch**

---

## SECTION 7: CONTENT FINGERPRINT AVOIDANCE

### What creates a "fingerprint" (pattern that links reviews together):
- Same writing style across all reviews
- Same sentence structure templates
- **Same accent/apostrophe dropping pattern** (v3.0: this is now the #1 fingerprint)
- Same vocabulary set used repeatedly
- Same way of ending reviews
- Reviews that all mention the same specific detail type
- Same level of specificity (all equally detailed or all equally vague)
- Same emotional intensity across reviews

### How to avoid fingerprinting:

#### Vary accent handling dramatically PER review:
- Review 1: nearly perfect accents (careful typer with autocorrect)
- Review 2: many missing accents (sloppy typer, old phone)
- Review 3: mostly correct with occasional misses
- Review 4: perfect accents (desktop user)
- **KEY: The VARIATION itself is what makes it realistic**

#### Vary apostrophe handling PER review:
- Review 1: all apostrophes present (autocorrect)
- Review 2: most missing (fast typing)
- Review 3: mixed (inconsistent, like real people)

#### Vary specificity level:
- Some reviews are very detailed (long, specific)
- Some are brief and punchy (short, focused)
- This is natural — some people write long reviews, others short

#### Vary ending patterns:
- NEVER end two consecutive reviews the same way
- Mix all ending types across the batch

#### Vary perspective:
- `je` (solo customer)
- `on` (couple/family, most common)
- `nous` (slightly more formal couple)
- `ma femme et moi` (specific)
- `mon mari a appelé` (female perspective)
- `mes parents ont fait appel` (younger person)

---

## SECTION 8: SEASONAL AND CONTEXTUAL REALISM

### Make reviews feel time-appropriate:
- Winter (Nov-Feb): mention cold, heating issues, urgency before holidays, storm damage
- Spring (Mar-May): mention renovation season, garden work, spring cleaning
- Summer (Jun-Aug): mention before-vacation repairs, AC needs, terrace work
- Fall (Sep-Oct): mention back-to-school, pre-winter preparation, leaf cleanup

### Location-specific realism:
- Paris/Ile-de-France: mention `appartement`, `immeuble`, `copropriété`, `syndic`
- South (Marseille, Nice, Toulouse): mention heat, `mistral`, terrasse, sun damage
- North (Lille, Strasbourg): mention rain, cold, humidity, insulation
- Belgium: slightly different vocabulary, mention `commune` instead of `mairie`
- Rural: mention `maison`, `terrain`, `voisin`, distance traveled by the company

### Life event contexts (makes reviews feel real):
- `suite à notre emménagement`
- `avant de vendre la maison`
- `après la naissance du bébé on voulait que tout soit nickel`
- `suite au décès de mon père j'ai dû vider la maison`
- `pour préparer le mariage de ma fille`
- `après les travaux du voisin qui ont abîmé notre mur`
- `avant l'arrivée de la belle famille`
- `on venait d'acheter et le toit était en mauvais état`
- `suite aux grosses pluies du mois dernier`
- `notre voisin nous avait recommandé de faire vérifier avant l'hiver`

---

## SECTION 9: APPEAL-PROOFING CHECKLIST (NEW)

Before submitting any review, verify it would survive a Google manual appeal review:

- [ ] Review mentions service-specific vocabulary (not just generic praise)
- [ ] Review includes at least 2 specificity layers
- [ ] Review has a personal context (why the person needed the service)
- [ ] Accent/apostrophe pattern is DIFFERENT from other reviews in the batch
- [ ] No phrase of 4+ words is repeated from any other review
- [ ] Review could NOT be mistaken for a template
- [ ] Review reads like a real person typed it on their phone
- [ ] Word count is different from adjacent reviews
- [ ] Ending is different from adjacent reviews
- [ ] Review adds VALUE — a future customer would learn something from it
