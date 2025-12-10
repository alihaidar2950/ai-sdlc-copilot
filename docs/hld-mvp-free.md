# AI SDLC Co-Pilot — MVP High-Level Design (100% Free Stack)

**Version:** 1.0
**Author:** Ali Haidar
**Date:** 2025-12-10
**Status:** MVP Development
**Cost:** $0/month (all free tiers)

---

## Executive Summary

This is the **zero-cost MVP version** of AI SDLC Co-Pilot, designed for solo developers to build, test, and demo without spending any money. All infrastructure uses free tiers, and LLM calls use free APIs.

**Target audience:** Solo developers, portfolio projects, Upwork gigs, job interviews.

### What You Can Build for Free

| Capability | Status |
|------------|--------|
| Test case generation from requirements | ✅ |
| PyTest skeleton generation | ✅ |
| PR review with AI suggestions | ✅ |
| CI log parsing → GitHub Issues | ✅ |
| Web dashboard | ✅ |
| GitHub OAuth authentication | ✅ |

---

## Free Stack Overview

```mermaid
flowchart TB
    subgraph Frontend["Frontend - FREE"]
        VERCEL["Vercel Free Tier<br/>100GB bandwidth/mo"]
    end
    
    subgraph Backend["Backend - FREE"]
        RENDER["Render Free Tier<br/>750 hours/mo"]
        API["FastAPI"]
    end
    
    subgraph Database["Database - FREE"]
        SUPA_DB["Supabase Postgres<br/>500MB free"]
        UPSTASH["Upstash Redis<br/>10K commands/day"]
    end
    
    subgraph Storage["Storage - FREE"]
        SUPA_STORE["Supabase Storage<br/>1GB free"]
    end
    
    subgraph LLM["LLM - FREE"]
        GEMINI["Google Gemini 1.5 Flash<br/>15 RPM, 1M tokens/day"]
        GROQ["Groq Llama 3.1<br/>30 RPM, 14K req/day"]
        OLLAMA["Ollama Local<br/>Unlimited"]
    end
    
    subgraph Integrations["Integrations - FREE"]
        GITHUB["GitHub<br/>OAuth, Issues, PRs, Actions, Wiki"]
    end
    
    VERCEL --> RENDER
    RENDER --> API
    API --> SUPA_DB
    API --> UPSTASH
    API --> SUPA_STORE
    API --> GEMINI
    API --> GROQ
    API --> GITHUB
```

---

## Complete Free Tier Stack

| Component | Service | Free Tier Limits | Enough for MVP? |
|-----------|---------|------------------|-----------------|
| **Frontend Hosting** | Vercel | 100GB bandwidth, unlimited deploys | ✅ Plenty |
| **Backend Hosting** | Render | 750 hrs/mo, sleeps after 15min | ✅ OK for dev |
| **Database** | Supabase Postgres | 500MB, 2 projects | ✅ Plenty |
| **Cache/Queue** | Upstash Redis | 10K commands/day | ✅ Yes |
| **Object Storage** | Supabase Storage | 1GB | ✅ Yes |
| **Vector DB** | Chroma (local) | Unlimited | ✅ Yes |
| **LLM (Primary)** | Google Gemini 1.5 Flash | 15 RPM, 1M tokens/day | ✅ Plenty |
| **LLM (Backup)** | Groq Llama 3.1 70B | 30 RPM, 14K req/day | ✅ Plenty |
| **LLM (Offline)** | Ollama (local) | Unlimited | ✅ Yes |
| **Auth** | GitHub OAuth | Unlimited | ✅ Yes |
| **CI/CD** | GitHub Actions | 2000 mins/mo | ✅ Plenty |
| **Issue Tracking** | GitHub Issues | Unlimited | ✅ Yes |
| **Documentation** | GitHub Wiki/Markdown | Unlimited | ✅ Yes |
| **Monitoring** | Sentry | 5K errors/mo | ✅ Yes |
| **Uptime Monitoring** | UptimeRobot | 50 monitors | ✅ Yes |

**Total Monthly Cost: $0**

---

## MVP Scope (Free Tier Compatible)

### In-Scope Features

* ✅ Ingest requirements (Markdown, GitHub Issues) → generate test cases
* ✅ Generate PyTest skeleton files
* ✅ PR review with AI-powered suggestions
* ✅ Parse GitHub Actions logs → create GitHub Issues with repro steps
* ✅ Web dashboard for artifact review and approval
* ✅ GitHub OAuth authentication

### Out-of-Scope (Add in Production Version)

* ❌ Jira/Confluence integration
* ❌ Jenkins CI integration
* ❌ SSO (Okta/Azure AD)
* ❌ Multi-tenant billing
* ❌ High-availability deployment

---

## Architecture (Free Stack)

```mermaid
flowchart LR
    U["User"] -->|GitHub OAuth| FE["Vercel<br/>React Frontend"]
    FE --> API["Render<br/>FastAPI Backend"]
    API --> DB["Supabase<br/>Postgres"]
    API --> CACHE["Upstash<br/>Redis"]
    API --> STORE["Supabase<br/>Storage"]
    API --> LLM["Gemini / Groq<br/>Free APIs"]
    API --> GH["GitHub<br/>PRs, Issues, Actions"]
```

### Data Flow

```mermaid
flowchart TB
    subgraph Input["Input Sources"]
        REQ["Requirements<br/>Markdown/GitHub Issues"]
        PR["PR Diff<br/>GitHub"]
        LOGS["CI Logs<br/>GitHub Actions"]
    end
    
    subgraph Process["Processing - Free LLMs"]
        INGEST["Ingest and Parse"]
        LLM["Gemini 1.5 Flash<br/>or Groq Llama 3.1"]
        ANALYZE["Static Analysis<br/>flake8, bandit"]
    end
    
    subgraph Output["Generated Artifacts"]
        TC["Test Case JSON"]
        PYTEST["PyTest Skeleton"]
        REVIEW["PR Comments"]
        DEFECT["GitHub Issue"]
    end
    
    REQ --> INGEST
    PR --> INGEST
    LOGS --> INGEST
    INGEST --> LLM
    INGEST --> ANALYZE
    LLM --> TC
    TC --> PYTEST
    LLM --> REVIEW
    ANALYZE --> REVIEW
    LLM --> DEFECT
```

---

## Component Design (Free Stack)

### 1. Frontend (Vercel - Free)

* **Tech:** React + Vite, Tailwind CSS, React Query
* **Hosting:** Vercel free tier (100GB bandwidth/mo)
* **Features:** Dashboard, artifact viewer, approve/reject UI

### 2. Backend API (Render - Free)

* **Tech:** FastAPI, Pydantic, Python 3.11+
* **Hosting:** Render free tier (750 hours/mo, sleeps after 15min idle)
* **Note:** Cold starts take ~30 seconds after sleep

### 3. Database (Supabase - Free)

* **Tech:** PostgreSQL 15
* **Limits:** 500MB storage, 2 projects
* **Features:** Full SQL, REST API, real-time subscriptions

### 4. Cache/Queue (Upstash - Free)

* **Tech:** Redis
* **Limits:** 10,000 commands/day
* **Use:** Job queue, caching LLM responses

### 5. Object Storage (Supabase - Free)

* **Limits:** 1GB storage
* **Use:** Store generated pytest files, artifacts

### 6. Vector Database (Chroma - Free)

* **Tech:** Chroma (runs locally or in-process)
* **Cost:** Free (open source)
* **Use:** RAG context for historical issues/code

### 7. LLM Providers (All Free)

**Primary: Google Gemini 1.5 Flash**
```python
# Free API key: https://aistudio.google.com/app/apikey
import google.generativeai as genai

genai.configure(api_key="YOUR_FREE_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Generate test cases for...")
```

**Backup: Groq (Llama 3.1 70B)**
```python
# Free API key: https://console.groq.com/keys
from groq import Groq

client = Groq(api_key="YOUR_FREE_KEY")
response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "..."}]
)
```

**Offline: Ollama (Local)**
```bash
# Install: https://ollama.ai
ollama pull llama3.1:8b
# Use via REST API at localhost:11434
```

### 8. Authentication (GitHub OAuth - Free)

* Create OAuth App in GitHub Settings
* Free, unlimited users
* Get user's repos, post PR comments, create issues

### 9. CI/CD (GitHub Actions - Free)

* 2,000 minutes/month for private repos
* Unlimited for public repos
* Run tests, deploy to Render/Vercel

---

## LLM Strategy (Zero Cost)

```mermaid
flowchart TD
    REQ["Incoming Request"] --> CHECK{"Rate Limit<br/>Check"}
    CHECK -->|Under Limit| GEMINI["Gemini 1.5 Flash<br/>Primary - Free"]
    CHECK -->|Over Limit| GROQ["Groq Llama 3.1<br/>Fallback - Free"]
    GEMINI -->|Error| GROQ
    GROQ -->|Error| OLLAMA["Ollama Local<br/>Always Available"]
    GEMINI --> RESULT["Return Result"]
    GROQ --> RESULT
    OLLAMA --> RESULT
```

### LLM Provider Comparison (All Free)

| Provider | Model | RPM | Daily Limit | Quality | Speed |
|----------|-------|-----|-------------|---------|-------|
| **Gemini** | 1.5 Flash | 15 | 1M tokens | ⭐⭐⭐⭐ | Fast |
| **Gemini** | 1.5 Pro | 2 | 50 requests | ⭐⭐⭐⭐⭐ | Medium |
| **Groq** | Llama 3.1 70B | 30 | 14K requests | ⭐⭐⭐⭐ | Very Fast |
| **Groq** | Mixtral 8x7B | 30 | 14K requests | ⭐⭐⭐ | Very Fast |
| **Ollama** | Llama 3.1 8B | ∞ | ∞ | ⭐⭐⭐ | Depends on HW |

### Recommended Strategy

1. **Primary:** Gemini 1.5 Flash (best quality/speed for free)
2. **Fallback:** Groq Llama 3.1 70B (when Gemini rate limited)
3. **Offline:** Ollama (for local dev, demos without internet)

---

## Database Schema

Same as production version - see `hld-production.md` for details.

**Tables:** `projects`, `jobs`, `artifacts`, `reviews`, `users`

---

## Free Tier Limitations & Workarounds

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **Render sleeps after 15min** | 30s cold start | Use cron job to ping every 14min |
| **Upstash 10K commands/day** | ~400 jobs/day max | Batch operations, use DB for persistence |
| **Supabase 500MB** | ~50K test cases | Archive old data, clean up regularly |
| **Gemini 15 RPM** | 900 requests/hour | Use Groq as fallback |

### Keep Render Awake (Free)

Add to GitHub Actions (runs every 14 minutes):
```yaml
name: Keep Alive
on:
  schedule:
    - cron: '*/14 * * * *'
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - run: curl -s https://your-app.onrender.com/health
```

---

## Implementation Plan (30 Days)

### Week 1 — Foundation (Free Stack Setup)

* [ ] Create Supabase project (Postgres + Storage)
* [ ] Create Upstash Redis instance
* [ ] Set up Render account (backend)
* [ ] Set up Vercel account (frontend)
* [ ] Get free API keys: Gemini, Groq
* [ ] Create GitHub OAuth App
* [ ] Repo scaffolding with Docker for local dev
* [ ] FastAPI skeleton with health endpoint
* [ ] GitHub Actions CI pipeline

### Week 2 — Core Features

* [ ] Implement GitHub OAuth login
* [ ] Requirement ingestion endpoint
* [ ] LLM integration (Gemini + Groq fallback)
* [ ] Test case generation with structured output
* [ ] Persist artifacts to Supabase

### Week 3 — GitHub Integration

* [ ] PyTest skeleton generator
* [ ] GitHub PR webhook handler
* [ ] Post PR review comments via GitHub API
* [ ] GitHub Issue creation for defects
* [ ] Basic React dashboard

### Week 4 — Polish & Demo

* [ ] Dashboard artifact viewer
* [ ] Approve/reject workflow
* [ ] GitHub Actions log parser
* [ ] End-to-end testing
* [ ] Deploy to Render + Vercel
* [ ] Demo with sample project

---

## Local Development Setup

```bash
# 1. Clone repo
git clone https://github.com/alihaidar2950/ai-sdlc-copilot.git
cd ai-sdlc-copilot

# 2. Start local services (Postgres, Redis)
docker-compose up -d

# 3. Set environment variables
cp .env.example .env
# Add your free API keys:
# - GEMINI_API_KEY (from https://aistudio.google.com/app/apikey)
# - GROQ_API_KEY (from https://console.groq.com/keys)
# - GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET

# 4. Run backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 5. Run frontend
cd frontend
npm install
npm run dev
```

---

## Environment Variables

```bash
# Database (Supabase free tier)
DATABASE_URL=postgresql://postgres:xxx@db.xxx.supabase.co:5432/postgres
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-anon-key

# Cache (Upstash free tier)
REDIS_URL=redis://default:xxx@xxx.upstash.io:6379

# LLM (all free)
GEMINI_API_KEY=your-free-gemini-key
GROQ_API_KEY=your-free-groq-key

# GitHub OAuth (free)
GITHUB_CLIENT_ID=your-oauth-app-id
GITHUB_CLIENT_SECRET=your-oauth-app-secret

# Optional: Local Ollama
OLLAMA_HOST=http://localhost:11434
```

---

## Acceptance Criteria (MVP)

* [ ] Generate test case JSON from markdown requirement (>90% success rate)
* [ ] Generate valid PyTest skeleton from test case
* [ ] Post PR review comment via GitHub API
* [ ] Create GitHub Issue from CI log failure
* [ ] Dashboard shows jobs and artifacts
* [ ] **Total infrastructure cost: $0/month**

---

## When to Upgrade to Production Stack

Consider upgrading when:

| Trigger | Action |
|---------|--------|
| First paying client | Upgrade Render to $7/mo (no sleep) |
| >500MB data | Upgrade Supabase to $25/mo |
| >10K requests/day | Add OpenAI as premium LLM option |
| Need Jira/Confluence | See `hld-production.md` |

---

## Links to Free Services

| Service | Sign Up Link |
|---------|--------------|
| Supabase | https://supabase.com (GitHub login) |
| Upstash | https://upstash.com (GitHub login) |
| Render | https://render.com (GitHub login) |
| Vercel | https://vercel.com (GitHub login) |
| Google AI Studio | https://aistudio.google.com/app/apikey |
| Groq | https://console.groq.com/keys |
| Ollama | https://ollama.ai |
| Sentry | https://sentry.io (free tier) |
| UptimeRobot | https://uptimerobot.com (free tier) |

---

## Next Steps

1. **Sign up for free services** (use GitHub login for all)
2. **Get API keys** (Gemini, Groq)
3. **Create GitHub OAuth App**
4. **Start Week 1 tasks**

For production deployment with paid services, see **`hld-production.md`**.
