# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC--GROUP-2
Group Members :<br>
- Tanmay Ghodke<br>
- Ritika Tiwari<br>
- Shashwat Singh<br>
- Kanak Mehta<br>
- Kamireddi Lakshmi Keerthi Sri<br>

Project :
A secure internal AI chatbot system that processes natural language queries and retrieves department-specific company information using Retrieval-Augmented Generation (RAG). <br>
The system enforces strict Role-Based Access Control (RBAC) to ensure secure departmental data access.

---

## 🚀 Project Overview

This project builds a complete enterprise-style AI system that:

- Authenticates users securely <br>
- Assigns role-based permissions <br>
- Retrieves relevant company documents using semantic search <br>
- Generates context-aware responses using a locally hosted LLM via **Ollama** <br>
- Prevents unauthorized cross-department data access <br>

---

## 🏗️ System Architecture

User → Streamlit UI → FastAPI Backend → RBAC Middleware → Vector Database → RAG Pipeline → Ollama LLM → Response with Sources <br>

---

## 🛠️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Vector Database | Chroma (Free Tier) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| LLM | **Ollama (Local LLM Execution)** |
| Database | SQLite |
| Authentication | JWT (PyJWT) |
| Version Control | GitHub |

---

# 📚 Milestones Breakdown

---

# ✅ Milestone 1: Data Preparation & Vector Database (Weeks 1–2)

### Module 1: Environment Setup & Data Exploration

- Set up Python virtual environment <br>
- Install dependencies (FastAPI, Streamlit, LangChain, sentence-transformers, pandas) <br>
- Clone GitHub RAG document repository <br>
- Explore markdown and CSV documents <br>
- Create role-to-document mapping <br>

**Deliverables:** <br>
- Configured Python environment <br>
- Initialized folder structure <br>
- Role-document mapping documentation <br>
- Data exploration summary report <br>

---

### Module 2: Document Preprocessing & Metadata Tagging

- Parse markdown and CSV documents <br>
- Clean and normalize text <br>
- Chunk documents into 300–512 token segments <br>
- Assign role-based metadata (source, department, allowed roles) <br>
- Create metadata mapping file <br>

**Deliverables:** <br>
- Preprocessing module <br>
- Cleaned document chunks <br>
- Metadata mapping documentation <br>
- Validation & QA report <br>

---

# ✅ Milestone 2: Backend Auth & Search (Weeks 3–4)

---

## Module 3: Vector Database & Embedding Generation

- Load embedding model: `sentence-transformers/all-MiniLM-L6-v2` <br>
- Generate embeddings for all document chunks <br>
- Initialize Chroma vector database <br>
- Index embeddings with metadata <br>
- Implement semantic search <br>

**Deliverables:** <br>
- Embedding generation module <br>
- Populated vector database with indexed documents <br>
- Semantic search functionality & query interface <br>
- Search quality & performance benchmarking report <br>

---

## Module 4: Role-Based Search & Query Processing

- Implement RBAC filtering logic <br>
- Define role hierarchy: <br>
  C-Level > Department Staff > General Employee <br>
- Normalize incoming queries <br>
- Filter retrieved chunks by role permissions <br>
- Validate role-based access (Finance cannot access HR, etc.) <br>

**Deliverables:** <br>
- RBAC filtering module <br>
- Query processing & normalization utilities <br>
- Role hierarchy definition <br>
- Role-based access validation test suite & results <br>

---

# ✅ Milestone 3: RAG Pipeline & LLM (Weeks 5–6)

---

## Module 5: Authentication & RBAC Middleware

- Build FastAPI backend <br>
- Implement JWT authentication <br>
- Create login endpoints <br>
- Store users in SQLite database <br>
- Enforce RBAC middleware <br>
- Implement access logging <br>

**Deliverables:** <br>
- FastAPI backend <br>
- JWT authentication system <br>
- RBAC middleware <br>
- User database <br>
- Authentication & authorization test cases <br>

---

## Module 6: RAG Pipeline & LLM Integration

- Integrate **Ollama** for local LLM execution <br>
- Design system prompts and templates <br>
- Build complete RAG pipeline: <br>
  1. Authenticate user <br>
  2. Filter by role <br>
  3. Retrieve relevant chunks <br>
  4. Augment prompt <br>
  5. Generate response using Ollama <br>
- Add source attribution <br>
- Implement confidence scoring <br>

**Deliverables:** <br>
- Ollama LLM integration module <br>
- Complete RAG pipeline <br>
- Prompt templates <br>
- Source citation system <br>
- RAG functionality test cases <br>

---

# ✅ Milestone 4: Frontend & Deployment (Weeks 7–8)

---

## Module 7: Streamlit Frontend

- Build login interface <br>
- Build chat interface <br>
- Display user role and department <br>
- Show source citations <br>
- Connect frontend with backend API <br>

**Deliverables:** <br>
- Streamlit application <br>
- Login system <br>
- Chat UI <br>
- API integration <br>
- User guide documentation <br>

---

## Module 8: Integration, Testing & Deployment

- End-to-end workflow testing <br>
- Role-based access validation <br>
- Performance optimization <br>
- Error handling tests <br>
- System documentation <br>
- GitHub deployment preparation <br>

**Deliverables:** <br>
- Integration test suite <br>
- System architecture documentation <br>
- API specification <br>
- Deployment guide <br>
- Performance & security testing report <br>
- Demo video <br>
- Production-ready GitHub repository <br>

---

# 🔐 Role Hierarchy

- **C-Level:** Full system access <br>
- **Department Staff:** Access to department-specific documents <br>
- **General Employees:** Access to general company documents only <br>

---

# 🧠 Why Ollama?

We used **Ollama** to:

- Run LLM locally <br>
- Avoid paid API dependency <br>
- Maintain internal data privacy <br>
- Enable offline inference <br>
- Ensure enterprise-level security <br>

---

# 🎯 Final Outcome

A fully secure, role-aware internal AI chatbot that:

✔ Prevents unauthorized data access <br>
✔ Retrieves relevant company knowledge <br>
✔ Generates grounded responses with sources <br>
✔ Uses only free & open-source technologies <br>
✔ Is fully documented and deployment-ready <br>

---


