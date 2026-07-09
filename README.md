# 🌐 NetworkOps — Network Operations Learning Platform

> **Master network operations, protocols, troubleshooting, and infrastructure — with structured learning paths and quizzes.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![Tests](https://img.shields.io/badge/Tests-29%20passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What is this?

NetworkOps is a local-first learning platform for network operations and engineering. It covers routing, switching, protocols, troubleshooting, security, and infrastructure management — all running on your machine with no cloud dependencies.

**For each topic, you get:**
- Concept explanation with real-world context
- Configuration examples
- Troubleshooting steps
- Best practices
- Related protocols and standards

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📚 Topic Explorer | 148 topics across 6 network domains |
| 🌐 Domain Browser | Routing, Switching, Security, Protocols, Infrastructure, Troubleshooting |
| 🧠 Quiz Engine | 401 quiz questions with adaptive testing |
| 📊 Progress Tracking | Track your learning journey |
| 🔍 Search & Filter | Find topics by domain, keyword, or difficulty |
| 📖 Structured Phases | Progressive learning path |
| 🎨 Hyperstudio Theme | Monochrome terminal + amber accents |

---

## 📊 Platform Stats

| Metric | Count |
|--------|-------|
| Topics | 148 |
| Domains | 6 |
| Quiz Questions | 401 |
| Automated Tests | 29 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Installation

```bash
# Clone the repository
git clone https://github.com/Yash-Patil-1/NetworkOps.git
cd NetworkOps

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Running the Application

```bash
# Terminal 1 — Backend
cd backend
./venv/bin/python -m uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm run dev
```

Open **http://localhost:5173**

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS v4 |
| Backend | FastAPI, Python 3.10+ |
| Database | SQLite (progress tracking) |
| Knowledge Base | JSON (topics, domains, questions) |
| Design | Hyperstudio — monochrome terminal + amber (#E7C59A) + green (#00AC5C) |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Platform info |
| GET | `/health` | Health check |
| GET | `/api/topics` | List all topics (with search/filter) |
| GET | `/api/topics/{id}` | Get topic details |
| GET | `/api/domains` | List network domains |
| GET | `/api/domains/phases` | Learning phases |
| GET | `/api/quiz/next` | Get next quiz question |
| POST | `/api/quiz/submit` | Submit quiz answer |
| GET | `/api/quiz/stats` | Quiz statistics |
| POST | `/api/progress/mark` | Mark topic as learned |
| GET | `/api/progress` | Get learning progress |

---

## 📁 Project Structure

```
NetworkOps/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── data/
│   │   ├── topics/             # Topic JSON files (148 topics)
│   │   ├── questions/          # Quiz questions (401)
│   │   ├── domains.json        # Network domains (6)
│   │   └── phases.json         # Learning phases
│   ├── models/                 # Database models
│   ├── routers/                # API route handlers
│   ├── services/               # Business logic
│   └── tests/                  # Test suite (29 tests)
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page views
│   │   └── styles/             # Tailwind styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── database/               # SQLite database
├── docs/                       # Design documents
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🧪 Testing

```bash
cd backend
./venv/bin/python -m pytest tests/ -v
```

**29 tests passing** — API endpoints, topic search, quiz engine, domain listing, progress tracking, streak/XP system, and guided lessons.

---

## 📸 Screenshots

| Dashboard | Learn | Topics |
|:---:|:---:|:---:|
| ![Dashboard](screenshots/01-dashboard.png) | ![Learn](screenshots/02-learn.png) | ![Topics](screenshots/03-topics.png) |

| Quiz | Lesson View | Topic Detail |
|:---:|:---:|:---:|
| ![Quiz](screenshots/04-quiz.png) | ![Lesson](screenshots/05-lesson-osi.png) | ![Topic Detail](screenshots/06-topic-osi.png) |

---

## 🌐 Domains Covered

| Domain | Focus Area |
|--------|-----------|
| Routing | OSPF, BGP, EIGRP, static routes, route redistribution |
| Switching | VLANs, STP, EtherChannel, trunking |
| Security | ACLs, firewalls, VPNs, port security, AAA |
| Protocols | TCP/IP, DNS, DHCP, HTTP, SNMP, NTP |
| Infrastructure | Server management, virtualization, storage, monitoring |
| Troubleshooting | Diagnostic tools, methodology, common issues |

---

## 🎨 Design

Hyperstudio design language:
- Dark monochrome terminal aesthetic
- Amber accent (#E7C59A) for highlights
- Green accent (#00AC5C) for success states
- Minimal, professional, distraction-free

---

## 🔒 Important

This is an **educational platform**. It does NOT:
- Configure real network devices
- Access live network infrastructure
- Use external AI APIs
- Require cloud or VMs

It teaches network operations concepts, explains protocols, and builds understanding. Everything runs locally.

---

## 👤 Author

**Yash Patil** — B.Tech IT | CEH  
🌐 [yashpatil.online](https://www.yashpatil.online/) · 🐙 [GitHub](https://github.com/Yash-Patil-1) · 💼 [LinkedIn](https://www.linkedin.com/in/yash-patil-997357330/)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
