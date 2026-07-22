# VedAI SaaS Architecture & Methodology Documentation

VedAI is designed to build a bridges between traditional Vedic Astrological models (Jyotish) and modern AI technologies. A core objective of the platform is **scientific boundaries maintenance**.

## 1. The Three Tiers of Information

The application strictly separates and labels three distinct classes of data:

### Tier 1: Deterministic Astronomical Calculations (Facts)
- **What it is**: Hard physical coordinates of celestial objects (longitude, latitude, house cusps, ascendant degree) at the exact moment and location of birth.
- **Methodology**: Computed using mathematical models representing Keplerian orbital nodes, corrected by subtraction of the **Lahiri Ayanamsha** (precession constant) to translate coordinates from the tropical frames into the sidereal frame.
- **Scientific status**: Fully verified astronomical physics.
- **UI Treatment**: Highlighted with technical badges, raw degrees, decimal representations, and a note indicating "Verified Astronomical coordinates".

### Tier 2: Traditional Interpretations (Literature & Texts)
- **What it is**: Textual mappings explaining what these astronomical positions represent according to classical Sanskrit literature, primarily Parashara rules (Brihat Parashara Hora Shastra).
- **Methodology**: Structured matching engine mapping calculated planetary house and sign placements to static text templates compiled from classical scripts.
- **Scientific status**: Historical cultural literature and symbolic interpretations. Not scientifically verified predictions.
- **UI Treatment**: Styled inside card containers representing historical parchment symbols, marked as "Traditional Text Mappings".

### Tier 3: AI-Generated Explanations (Synthesis & Contextualization)
- **What it is**: Contextualized, readable narrative synthesis compiled by Google Gemini that explains the relation between various planetary positions and offers self-reflective advice.
- **Methodology**: Large language model parsing parameters through structured prompting guidelines that mandate the inclusion of spiritual/psychological disclaimers and prohibit definitive, scientific-sounding physical predictions.
- **Scientific status**: Conversational synthesis intended for introspective self-reflection. Not scientifically verified.
- **UI Treatment**: Wrapped inside cards with AI symbols, marked "AI Spiritual Synthesis".

---

## 2. Platform Service Architecture

The project is structured in a monorepo pattern:

- `packages/shared`: Common TypeScript types and validation boundaries shared between Next.js clients.
- `packages/ui`: Shared styling tokens representing dark premium elements (deep space base, glassmorphic cards, gold/purple highlights).
- `packages/astrology-engine`: Clean Python implementation computing sidereal degrees.
- `packages/ai-engine`: Gemini HTTP API client managing system-prompt structures and disclaimer enforcement.
- `packages/report-engine`: Report compiler converting JSON report structures into PDF reports (using `fpdf2`).
- `apps/api`: FastAPI web portal running:
  - Database Models (SQLAlchemy + SQLite/Postgres)
  - Repositories (Encapsulating DB calls)
  - Service orchestrators (Connecting engines to DB)
  - Controllers/Routes (User JWT auth, profiles, charts, chat history, reports)
- `apps/web`: Next.js 15 client dashboard (landing, birth forms, chat window, tabbed report panel).
- `apps/admin`: Next.js 15 operational console showing active user tables and calculation performance metrics.

---

## 3. Legal Disclaimers & Ethics Policy

VedAI maintains a strict policy regarding predictions. A prominent disclaimer is appended to all PDF downloads, AI explanations, and chat sessions:

> **Disclaimer**: Vedic Astrology (Jyotish) is a traditional system of symbolic analysis and reflection. Interpretations are based on classical texts and modern archetypal synthesis. Astrological insights are intended for self-reflection and personal growth, and are not scientifically verified predictions, nor should they substitute for professional financial, legal, or medical advice.
