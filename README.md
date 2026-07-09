# Arx AI

**Arx AI** is an AI-powered cyber risk intelligence platform designed to help Application Security Analysts and Security Engineers convert vulnerability scan findings from sandboxed applications into prioritized business risk insights, dynamic Key Risk Indicators, and professional security reports.

The project focuses on the intersection of **application security**, **AI enrichment**, **risk scoring**, **data visualization**, and **enterprise-style cyber risk reporting**.

> Arx AI is designed for educational, defensive, and authorized security testing only. It does not support scanning public websites or real systems.

---

## Project Overview

Traditional vulnerability scanners can generate many technical findings, but those findings are often difficult to prioritize, explain, and communicate to non-technical stakeholders.

Arx AI aims to solve this problem by taking raw vulnerability findings from approved sandbox targets and converting them into:

* AI-generated plain-English explanations
* OWASP category mappings
* Business impact summaries
* Remediation recommendations
* Calculated risk scores
* KRI dashboard metrics
* Scan summary reports

The goal is not just to detect vulnerabilities, but to help answer:

> Which security issues matter most, why do they matter, and what should be fixed first?

---

## Primary User

The primary user of Arx AI is an:

**Application Security Analyst / Security Engineer**

This user is responsible for reviewing vulnerability findings, prioritizing risk, communicating security concerns, and helping teams understand what needs to be fixed.

---

## Core Workflow

The main Arx AI workflow is:

```text
Approved Sandbox Target
        ↓
Scan Job Created
        ↓
Scanner Runs in Background
        ↓
Raw Findings Stored
        ↓
AI Enrichment
        ↓
Risk Scoring
        ↓
KRI Dashboard
        ↓
Report Generation
```

A user should be able to:

1. Open the Arx AI dashboard.
2. View the current cyber risk summary.
3. Select an approved sandbox target.
4. Start a scan.
5. View scan status and scan history.
6. Review raw vulnerability findings.
7. View AI-enriched explanations and remediation guidance.
8. Review calculated risk scores.
9. Analyze KRI dashboard metrics.
10. Generate a scan summary report.

---

## MVP Features

The MVP version of Arx AI will include:

* Frontend dashboard
* Backend API
* PostgreSQL database
* Approved sandbox target management
* Scan job creation
* Background scan execution
* Raw finding storage
* AI enrichment of findings
* Business risk scoring
* KRI dashboard
* Findings table with filtering and sorting
* Basic scan summary report
* Audit logging for important system events

---

## Planned Stretch Features

After the MVP is complete, the following features may be added:

* PDF executive report generation
* Vendor risk scoring
* MITRE ATT&CK mapping
* Real-time scan progress updates
* Authentication and role-based access control
* CI/CD pipeline
* Cloud deployment
* Monitoring and observability with Prometheus and Grafana
* Vector database and RAG-based security knowledge retrieval
* Additional scanner integrations
* Developer remediation workflow

---

## Technology Stack

### Frontend

* Next.js
* TypeScript
* Tailwind CSS
* shadcn/ui
* Recharts
* TanStack Table
* TanStack Query

### Backend

* FastAPI
* Python
* Pydantic
* SQLAlchemy
* Alembic

### Database

* PostgreSQL

### Background Processing

* Redis
* RQ

### Security Scanning

* OWASP ZAP Baseline Scan
* Python scanner wrapper scripts
* Dockerized sandbox targets

### AI Layer

* LangGraph
* LangChain
* OpenAI API or local LLM
* Pydantic validation for structured AI output

### DevOps

* Docker
* Docker Compose
* GitHub Actions as a stretch feature

---

## High-Level Architecture

```text
                         ┌──────────────────────┐
                         │   Frontend Dashboard  │
                         │ Next.js + TypeScript  │
                         └───────────┬──────────┘
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │     Backend API       │
                         │       FastAPI         │
                         └───────────┬──────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                      ▼
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │ PostgreSQL DB    │   │ Background Worker│   │ Report Generator │
   │ Stores system    │   │ Runs async jobs  │   │ Creates reports  │
   │ data             │   │                  │   │                  │
   └──────────────────┘   └─────────┬────────┘   └──────────────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     ▼              ▼              ▼
           ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
           │ Scanner Service│ │ AI Enrichment│ │ KRI Engine     │
           │ Safe scanning  │ │ AI analysis  │ │ Risk scoring   │
           └───────┬────────┘ └──────────────┘ └────────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │ Approved Sandbox Targets │
        │ Juice Shop / DVWA / Lab  │
        └──────────────────────────┘
```

---

## Database Model

The MVP database model includes:

* `targets`
* `scan_jobs`
* `raw_findings`
* `enriched_findings`
* `risk_scores`
* `reports`
* `audit_logs`

Main relationship flow:

```text
targets
   ↓
scan_jobs
   ↓
raw_findings
   ↓
enriched_findings
   ↓
risk_scores

scan_jobs
   ↓
reports

scan_jobs / targets
   ↓
audit_logs
```

---

## Risk Scoring Concept

Arx AI calculates a business risk score for each finding using a documented scoring formula.

A simple MVP formula may be:

```text
Risk Score = Severity Weight × Exploitability × Asset Criticality × Vendor Exposure × Confidence
```

The score is then normalized to a 0–100 scale and displayed as a business risk level.

Example levels:

* Low
* Medium
* High
* Critical

The goal is to make vulnerability prioritization explainable and consistent.

---

## Ethical Boundaries

Arx AI is built with strict ethical and safety boundaries.

The platform will:

* Only scan approved sandbox targets
* Only run against intentionally vulnerable lab applications
* Preserve raw scanner evidence
* Validate AI-generated output before storage
* Separate scanner evidence from AI interpretation
* Focus on remediation and defensive risk analysis

The platform will not:

* Scan public websites
* Attack real systems
* Perform destructive actions
* Store real company data or credentials
* Support unrestricted offensive automation
* Provide step-by-step exploitation guidance for real systems

---

## Example Approved Sandbox Targets

Arx AI may use controlled lab targets such as:

* OWASP Juice Shop
* DVWA
* Custom intentionally vulnerable demo application

These targets should run locally or inside a private Docker network.

---

## Project Status

Current status:

```text
Planning and architecture design in progress
```

Completed planning artifacts:

* Requirements document
* Functional requirements
* Non-functional requirements
* MVP scope
* Stretch feature scope
* System architecture
* Database model / ERD

Next development steps:

1. Set up backend project structure.
2. Create SQLAlchemy models.
3. Configure PostgreSQL and Alembic.
4. Build target and scan job APIs.
5. Add background worker and Redis queue.
6. Integrate sandbox scanner.
7. Add AI enrichment.
8. Build KRI dashboard.

---

## Local Development

Local setup instructions will be added as the implementation progresses.

Planned local environment:

```text
Frontend: Next.js
Backend: FastAPI
Database: PostgreSQL
Queue: Redis
Worker: RQ
Sandbox Targets: Docker Compose
```

Expected future command:

```bash
docker compose up --build
```

---

## Repository Structure

Planned structure:

```text
arx-ai/
  backend/
    app/
      models/
      schemas/
      api/
      services/
      workers/
      db/
    tests/

  frontend/
    app/
    components/
    lib/

  docs/
    requirements.md
    architecture.md
    database-model.md

  docker-compose.yml
  README.md
```

---

## Disclaimer

Arx AI is an educational cyber risk intelligence platform designed for authorized testing against sandboxed, intentionally vulnerable applications.

It must not be used to scan, attack, or assess systems without explicit permission.

The project focuses on defensive security analysis, risk prioritization, remediation guidance, and cyber risk communication.
