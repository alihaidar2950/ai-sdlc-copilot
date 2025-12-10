# AI SDLC Co-Pilot

🤖 **Automate your software development lifecycle with AI** — Generate test cases, review PRs, and create defect tickets automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 What is AI SDLC Co-Pilot?

AI SDLC Co-Pilot is a productivity platform that uses LLMs to automate tedious SDLC tasks:

| Feature | Description |
|---------|-------------|
| **Test Case Generation** | Input requirements → Get structured test cases + PyTest skeletons |
| **PR Review** | AI-powered code review with actionable suggestions |
| **Defect Creation** | Parse CI logs → Auto-create GitHub Issues with repro steps |
| **Documentation** | Generate test matrices and technical docs |

### Who is this for?

- 🧑‍💻 **Solo developers** building portfolio projects
- 🏢 **QA teams** looking to accelerate test design
- 🚀 **Startups** without dedicated QA resources
- 💼 **Freelancers** offering automation services on Upwork

---

## ✨ Features

### MVP (Current Focus)
- [x] Requirement ingestion (Markdown, GitHub Issues)
- [x] Test case generation with structured JSON output
- [x] PyTest skeleton generation
- [x] PR review comments via GitHub API
- [x] CI log parsing → GitHub Issue creation
- [x] Web dashboard for artifact review

### Coming Soon
- [ ] Jira/Confluence integration
- [ ] RAG context for historical issues
- [ ] Confidence scoring for suggestions
- [ ] Multi-tenant SaaS

---

## 🏗️ Architecture

```mermaid
flowchart LR
    U["User"] --> FE["React Frontend"]
    FE --> API["FastAPI Backend"]
    API --> LLM["Gemini / Groq / OpenAI"]
    API --> DB["PostgreSQL"]
    API --> GH["GitHub API"]
```

See the [High-Level Design docs](./docs/) for detailed architecture:
- **[hld.md](./docs/hld.md)** — Overview and index
- **[hld-mvp-free.md](./docs/hld-mvp-free.md)** — Zero-cost MVP stack ($0/month)
- **[hld-production.md](./docs/hld-production.md)** — Production scale architecture

---

## 💰 Cost

### MVP Stack: **$0/month**

| Component | Free Service |
|-----------|--------------|
| Frontend | Vercel Free |
| Backend | Render Free |
| Database | Supabase Free (500MB) |
| Cache | Upstash Free |
| LLM | Google Gemini + Groq (free APIs) |
| Auth | GitHub OAuth |

See [hld-mvp-free.md](./docs/hld-mvp-free.md) for complete setup guide.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for local development)
- Free API keys from [Google AI Studio](https://aistudio.google.com/app/apikey) and [Groq](https://console.groq.com/keys)

### Local Development

```bash
# Clone the repo
git clone https://github.com/alihaidar2950/ai-sdlc-copilot.git
cd ai-sdlc-copilot

# Start local services (Postgres, Redis)
docker-compose up -d

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Install backend dependencies
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Install frontend dependencies (new terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

```bash
# LLM APIs (free)
GEMINI_API_KEY=your-key-from-aistudio.google.com
GROQ_API_KEY=your-key-from-console.groq.com

# GitHub OAuth
GITHUB_CLIENT_ID=your-oauth-app-id
GITHUB_CLIENT_SECRET=your-oauth-app-secret

# Database (local Docker or Supabase)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sdlc_copilot

# Redis (local Docker or Upstash)
REDIS_URL=redis://localhost:6379
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [docs/hld.md](./docs/hld.md) | HLD index and comparison |
| [docs/hld-mvp-free.md](./docs/hld-mvp-free.md) | Free tier MVP architecture |
| [docs/hld-production.md](./docs/hld-production.md) | Production scale architecture |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — Modern Python web framework
- **Pydantic** — Data validation
- **Celery/RQ** — Task queue for async processing
- **PostgreSQL** — Primary database
- **Redis** — Caching and job queue

### Frontend
- **React** — UI library
- **Vite** — Build tool
- **Tailwind CSS** — Styling
- **React Query** — Data fetching

### LLM Providers
- **Google Gemini** — Primary (free tier)
- **Groq** — Fallback (free tier)
- **Ollama** — Local/offline option
- **OpenAI** — Production option

---

## 🗺️ Roadmap

### Phase 1: MVP (Weeks 1-4) ← **Current**
- Core test case generation
- GitHub integration
- Basic dashboard

### Phase 2: Enhanced Features (Weeks 5-8)
- RAG context integration
- Confidence scoring
- Analytics dashboard

### Phase 3: Enterprise (Months 3-6)
- Jira/Confluence connectors
- SSO (Okta/Azure AD)
- Multi-tenant billing

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines (coming soon).

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing Python framework
- [Google AI Studio](https://aistudio.google.com/) for free Gemini API access
- [Groq](https://groq.com/) for free Llama API access
- [Supabase](https://supabase.com/) for the free database tier

---

## 📬 Contact

**Ali Haidar** - [@alihaidar2950](https://github.com/alihaidar2950)

Project Link: [https://github.com/alihaidar2950/ai-sdlc-copilot](https://github.com/alihaidar2950/ai-sdlc-copilot)
