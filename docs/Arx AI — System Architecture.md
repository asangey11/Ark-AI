# Arx AI — System Architecture

## 1. Architecture Overview

Arx AI is an AI-powered cyber risk intelligence platform designed to help Application Security Analysts and Security Engineers assess security risk in sandboxed web applications.

The system allows a user to select an approved sandbox target, start a vulnerability scan, collect raw security findings, enrich those findings using AI, calculate business risk scores, and display the results in a dynamic KRI dashboard.

Arx AI is designed as a modular web application with separate components for the frontend dashboard, backend API, database, scan orchestration, scanner execution, AI enrichment, risk scoring, reporting, and sandbox targets.

The architecture is intentionally designed to be safe and controlled. The platform only scans pre-approved sandbox environments and does not support scanning arbitrary public websites or real production systems.

## 2. Architecture Goals

The architecture of Arx AI is designed around the following goals:

### 2.1 Safety

Arx AI must operate only in a controlled sandbox environment. The system should prevent users from scanning arbitrary external targets and should only allow scans against preconfigured intentionally vulnerable applications.

### 2.2 Modularity

The system should be divided into clear components so that scanning, AI enrichment, risk scoring, dashboard display, and reporting can be developed and tested independently.

### 2.3 Maintainability

The codebase should be organized so that new sandbox targets, scan types, risk metrics, and dashboard features can be added without rewriting the entire system.

### 2.4 Responsiveness

Long-running tasks such as scans, AI enrichment, and report generation should run in the background so the user interface remains responsive.

### 2.5 Traceability

The system should preserve raw findings, AI-enriched findings, scan history, and risk scores so the user can understand how each risk metric was produced.

### 2.6 Professional Presentation

The platform should present technical vulnerability data in a way that is understandable to both technical users and semi-technical stakeholders through dashboards, summaries, and reports.

### 2.7 Future Scalability

The MVP should be simple enough to build, but the architecture should allow future improvements such as real-time scan progress, MITRE ATT&CK mapping, vendor risk scoring, authentication, CI/CD, cloud deployment, and monitoring.

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


## 4. Core System Components

Arx AI is designed as a modular system made up of several core components. Each component has a clear responsibility and communicates with other components through defined interfaces. This separation makes the system easier to build, test, maintain, and extend.

The main components of Arx AI are:

1. Frontend Dashboard
2. Backend API
3. PostgreSQL Database
4. Background Worker
5. Scanner Service
6. AI Enrichment Service
7. Risk Scoring and KRI Engine
8. Report Generator
9. Sandbox Targets
10. Redis Queue
11. Audit Logging Component

---

### 4.1 Frontend Dashboard

The frontend dashboard is the user-facing part of Arx AI. It allows the Application Security Analyst or Security Engineer to interact with the system, view cyber risk data, start scans, review findings, and generate reports.

#### Responsibilities

The frontend dashboard is responsible for:

1. Displaying the main cyber risk summary.
2. Showing approved sandbox targets.
3. Allowing the user to start a scan against an approved sandbox target.
4. Displaying scan history and scan status.
5. Displaying vulnerability findings in a searchable and filterable table.
6. Showing AI-enriched explanations and remediation guidance.
7. Displaying KRI charts and business risk metrics.
8. Allowing filtering by severity, target, vendor, date, vulnerability category, and risk score.
9. Displaying scan summary reports.
10. Providing a clean and professional user experience.

#### Main Pages

The frontend should include the following pages:

1. Dashboard page
2. Targets page
3. Scans page
4. Scan details page
5. Findings page
6. KRI dashboard page
7. Reports page
8. Settings or admin page as an optional stretch feature

#### Technology Choices

The frontend will use:

1. Next.js
2. TypeScript
3. Tailwind CSS
4. shadcn/ui
5. Recharts
6. TanStack Table
7. React Query or TanStack Query

#### Justification

Next.js and TypeScript are strong choices for building a modern web application. TypeScript improves reliability by catching many errors during development. Tailwind CSS and shadcn/ui make it easier to build a polished dashboard interface quickly. Recharts is useful for visualizing KRI metrics, and TanStack Table is useful for creating searchable, sortable, and filterable findings tables.

The frontend is intentionally separated from the scanning and AI logic. This keeps the user interface focused on presentation and interaction, while the backend handles business logic, scan control, AI enrichment, and data processing.

---

### 4.2 Backend API

The backend API is the central control layer of Arx AI. It receives requests from the frontend, validates them, communicates with the database, creates scan jobs, triggers background processing, and returns data needed by the dashboard.

#### Responsibilities

The backend API is responsible for:

1. Managing approved sandbox targets.
2. Creating scan jobs.
3. Returning scan history and scan details.
4. Returning raw and enriched vulnerability findings.
5. Triggering background scan tasks.
6. Triggering AI enrichment tasks.
7. Returning KRI dashboard metrics.
8. Returning report data.
9. Validating user input.
10. Enforcing sandbox-only scanning rules.
11. Preventing arbitrary public URL scanning.
12. Handling errors and returning clear API responses.

#### Example API Endpoints

The backend may include endpoints such as:

1. `GET /health`
2. `GET /targets`
3. `GET /targets/{target_id}`
4. `POST /scans`
5. `GET /scans`
6. `GET /scans/{scan_id}`
7. `GET /findings`
8. `GET /findings/{finding_id}`
9. `GET /kri/summary`
10. `GET /kri/trends`
11. `GET /reports/{scan_id}`
12. `POST /reports/{scan_id}/generate`

#### Technology Choices

The backend will use:

1. FastAPI
2. Python
3. Pydantic
4. SQLAlchemy
5. Alembic

#### Justification

FastAPI is a strong backend choice because it is fast, modern, Python-based, and works well with AI, security tooling, and data processing. Pydantic provides structured request and response validation, which is important because the system will handle scanner output and AI-generated data. SQLAlchemy provides database access, and Alembic supports database migrations as the schema evolves.

The backend acts as the main gatekeeper of the system. It ensures users can only scan approved sandbox targets and cannot use Arx AI against arbitrary external systems.

---

### 4.3 PostgreSQL Database

The PostgreSQL database stores the persistent data used by Arx AI. This includes sandbox targets, scan jobs, raw findings, enriched findings, risk scores, KRI metrics, report metadata, and audit logs.

#### Responsibilities

The database is responsible for storing:

1. Approved sandbox targets.
2. Scan jobs.
3. Scan status history.
4. Raw vulnerability findings.
5. AI-enriched findings.
6. Risk scores.
7. KRI data.
8. Vendor and asset information.
9. Report metadata.
10. Audit logs.

#### Main Data Entities

The database should eventually include tables such as:

1. `targets`
2. `vendors`
3. `assets`
4. `scan_jobs`
5. `raw_findings`
6. `enriched_findings`
7. `risk_scores`
8. `kri_snapshots`
9. `reports`
10. `audit_logs`
11. `users` as a stretch feature
12. `roles` as a stretch feature

#### Technology Choices

The database layer will use:

1. PostgreSQL
2. SQLAlchemy ORM
3. Alembic migrations

#### Justification

PostgreSQL is reliable, widely used in industry, and well suited for structured relational data. Arx AI has many connected entities: targets have scans, scans have findings, findings have AI enrichments, and findings contribute to KRI calculations. A relational database is appropriate because these relationships need to be preserved clearly.

PostgreSQL also makes it easier to query historical data for dashboards, reports, and trend analysis.

---

### 4.4 Background Worker

The background worker handles long-running tasks that should not block the main backend API. Scans, AI enrichment, risk scoring, and report generation may take time, so they should run asynchronously in the background.

#### Responsibilities

The background worker is responsible for:

1. Running scan jobs.
2. Updating scan job status.
3. Processing raw scanner output.
4. Triggering AI enrichment for findings.
5. Triggering risk score calculation.
6. Updating KRI metrics after scans complete.
7. Generating reports.
8. Handling failed jobs gracefully.
9. Logging job errors for debugging.

#### Example Job Flow

A typical background job flow is:

1. Backend API creates a scan job.
2. Backend places the scan job into a queue.
3. Background worker picks up the job.
4. Worker runs the scanner service against the approved sandbox target.
5. Worker stores raw findings.
6. Worker triggers AI enrichment.
7. Worker triggers risk scoring.
8. Worker marks the scan as completed or failed.

#### Technology Choices

The background processing layer will use:

1. Redis Queue, also known as RQ, for the MVP.
2. Redis as the queue backend.

Celery may be considered later as a stretch option if the project needs more advanced task orchestration.

#### Justification

Background workers are important because vulnerability scanning and AI enrichment can take time. Without a worker, the backend API request could hang while the scan runs. That would create a poor user experience and make the system less reliable.

For the MVP, RQ is a good choice because it is simpler than Celery and easier to set up. This keeps the project manageable while still demonstrating asynchronous job processing.

---

### 4.5 Redis Queue

Redis supports the background worker system by acting as a lightweight queue. It stores jobs that need to be processed asynchronously.

#### Responsibilities

Redis is responsible for:

1. Holding queued scan jobs.
2. Allowing workers to pick up jobs.
3. Supporting asynchronous task processing.
4. Helping separate API requests from long-running work.
5. Supporting future real-time scan progress features.

#### Technology Choice

The queue system will use:

1. Redis
2. RQ

#### Justification

Redis is commonly used for queues, caching, and lightweight background processing. In Arx AI, Redis helps keep the frontend and backend responsive by allowing scan jobs and AI enrichment tasks to run outside the main request-response cycle.

---

### 4.6 Scanner Service

The scanner service is responsible for safely scanning approved sandbox targets and producing raw vulnerability findings. This component should only operate against preconfigured lab environments.

#### Responsibilities

The scanner service is responsible for:

1. Running scans only against approved sandbox targets.
2. Collecting vulnerability findings from sandbox applications.
3. Normalizing scanner output into a consistent format.
4. Returning raw findings to the backend or worker.
5. Avoiding destructive scan behavior.
6. Preventing scans against arbitrary public URLs.
7. Supporting repeatable scans for demos and testing.

#### Scanner Approach

For the MVP, Arx AI should use safe scanning methods against intentionally vulnerable lab applications. The project may use:

1. OWASP ZAP baseline scan.
2. Python wrapper scripts.
3. Predefined scan configurations.
4. Docker network isolation.

The scanner should produce normalized findings with fields such as:

1. Vulnerability type
2. Affected endpoint
3. Evidence summary
4. Severity
5. Confidence
6. Target ID
7. Scan ID
8. Timestamp

#### Technology Choices

The scanner service will use:

1. OWASP ZAP baseline scan
2. Python wrapper scripts
3. Docker
4. Docker Compose

#### Justification

The goal of Arx AI is not to build a professional vulnerability scanner from scratch. The stronger engineering value comes from orchestrating scans safely, storing findings, enriching them with AI, calculating business risk, and visualizing KRIs.

Using a known scanner in a controlled lab environment allows the project to stay safe, realistic, and focused.

---

### 4.7 AI Enrichment Service

The AI enrichment service analyzes raw vulnerability findings and converts them into structured, understandable risk insights. This component is what makes Arx AI an AI-powered security risk platform rather than a basic scanner.

#### Responsibilities

The AI enrichment service is responsible for:

1. Reading raw vulnerability findings.
2. Classifying the vulnerability type.
3. Generating a plain-English explanation.
4. Suggesting remediation guidance.
5. Mapping findings to OWASP categories.
6. Estimating business impact.
7. Producing structured JSON output.
8. Validating AI output before storage.
9. Marking findings for manual review if enrichment fails.
10. Separating AI interpretation from raw scanner evidence.

#### Example AI-Enriched Output

An enriched finding may include:

1. Finding title
2. Vulnerability category
3. Plain-English explanation
4. OWASP category
5. Business impact
6. Remediation recommendation
7. Suggested priority
8. Confidence level
9. Manual review flag

#### Technology Choices

The AI enrichment service will use:

1. LangGraph
2. LangChain
3. OpenAI API or a local LLM
4. Pydantic validation
5. Optional vector database for RAG in a later version

#### Justification

The AI enrichment service demonstrates modern AI engineering. The AI is not used as a chatbot. Instead, it acts as a structured analyst component inside a larger system.

The use of Pydantic validation is important because AI output can be inconsistent. By forcing the output into a structured schema, Arx AI becomes more reliable and easier to integrate with the database and dashboard.

---

### 4.8 Risk Scoring and KRI Engine

The Risk Scoring and KRI Engine converts enriched vulnerability findings into business-level cyber risk metrics. This is the component that turns technical scanner output into decision-support information.

#### Responsibilities

The Risk Scoring and KRI Engine is responsible for:

1. Calculating a risk score for each finding.
2. Ranking findings by priority.
3. Calculating average risk score.
4. Counting critical and high-risk findings.
5. Identifying the highest-risk target.
6. Identifying the highest-risk vendor.
7. Calculating risk trends over time.
8. Calculating vulnerability distribution by category.
9. Preparing dashboard-ready KRI metrics.
10. Supporting filtering by date, severity, target, vendor, and category.

#### Example Risk Factors

The risk score may consider:

1. Technical severity
2. Exploitability
3. Asset criticality
4. Vendor exposure
5. Confidence level
6. Business impact

#### Example Risk Formula

A simple MVP risk formula may be:

```text
Risk Score = Severity Weight × Exploitability × Asset Criticality × Vendor Exposure × Confidence
```

The final score can then be normalized to a 0–100 scale.

#### Technology Choices

The KRI engine will use:

1. Python service layer
2. PostgreSQL queries
3. Optional Pandas for analytics
4. FastAPI endpoints for dashboard data

#### Justification

This component is one of the most important parts of Arx AI. A normal scanner only tells the user what was found. The KRI engine helps answer what matters most, what should be fixed first, and how risk is changing over time.

This makes the project more enterprise-focused and more valuable than a simple vulnerability scanning tool.

---

### 4.9 Report Generator

The report generator creates summaries of scans, findings, AI explanations, risk scores, and recommended remediation steps.

#### Responsibilities

The report generator is responsible for:

1. Creating scan summary reports.
2. Creating executive summaries.
3. Listing the highest-priority findings.
4. Including AI-generated explanations.
5. Including remediation guidance.
6. Including risk scores and KRI metrics.
7. Supporting HTML reports for the MVP.
8. Supporting PDF export as a stretch feature.

#### Report Types

Arx AI may support:

1. Scan Summary Report
2. Executive Risk Report
3. Vendor Risk Report as a stretch feature
4. Monthly KRI Report as a stretch feature

#### Technology Choices

The MVP report generator can use:

1. HTML report templates
2. Backend-generated report data
3. Frontend report preview page

The stretch version may use:

1. WeasyPrint
2. ReportLab
3. Playwright PDF export

#### Justification

Reports make Arx AI feel like a professional enterprise tool. They allow the user to communicate findings to both technical and non-technical stakeholders. For the MVP, a report preview page is enough. PDF export should be added only after the main workflow is working.

---

### 4.10 Sandbox Targets

Sandbox targets are intentionally vulnerable applications used for safe scanning and testing. These targets are controlled environments and are not real production systems.

#### Responsibilities

Sandbox targets are responsible for:

1. Providing safe vulnerable applications for testing.
2. Running inside Docker containers.
3. Producing realistic scan findings.
4. Supporting repeatable scans.
5. Remaining isolated from real networks and public systems.
6. Allowing the project to demonstrate scanning safely and ethically.

#### Example Sandbox Targets

Arx AI may use:

1. OWASP Juice Shop
2. DVWA
3. A custom intentionally vulnerable mini application

#### Technology Choices

Sandbox targets will use:

1. Docker
2. Docker Compose
3. Internal Docker networking

#### Justification

Sandbox targets are essential because Arx AI is a cybersecurity-related project. The system must demonstrate scanning and risk analysis without creating harm or scanning unauthorized systems.

Using sandbox targets keeps the project ethical, repeatable, and suitable for academic demonstration.

---

### 4.11 Audit Logging Component

The audit logging component records important actions that occur in the system. This improves traceability and helps show responsible security design.

#### Responsibilities

The audit logging component is responsible for recording:

1. Scan creation events.
2. Scan completion events.
3. Scan failure events.
4. AI enrichment events.
5. Report generation events.
6. Important system errors.
7. User actions as a stretch feature.

#### Example Audit Log Fields

An audit log entry may include:

1. Event ID
2. Event type
3. Timestamp
4. Related scan ID
5. Related target ID
6. User ID as a stretch feature
7. Message or description
8. Status

#### Technology Choices

The audit logging component will use:

1. PostgreSQL
2. Backend service layer
3. Structured application logs

#### Justification

Audit logs are important in security-related systems because they help explain what happened and when. They also support debugging, traceability, and professional system design.

Even in the MVP, basic audit logging helps show that Arx AI was designed with security and accountability in mind.

---

### 4.12 Component Interaction Summary

The core components work together as follows:

1. The user interacts with the Frontend Dashboard.
2. The Frontend Dashboard sends API requests to the Backend API.
3. The Backend API validates requests and stores data in PostgreSQL.
4. When a scan is started, the Backend API creates a scan job.
5. The scan job is placed into Redis Queue.
6. The Background Worker picks up the scan job.
7. The Scanner Service scans the approved sandbox target.
8. Raw findings are stored in PostgreSQL.
9. The AI Enrichment Service analyzes the raw findings.
10. Enriched findings are stored in PostgreSQL.
11. The Risk Scoring and KRI Engine calculates risk scores and dashboard metrics.
12. The Frontend Dashboard displays updated risk data.
13. The Report Generator creates a scan or risk summary report.
14. The Audit Logging Component records important system actions.

This modular architecture allows Arx AI to start as a manageable MVP while still supporting future improvements such as real-time scan updates, MITRE ATT&CK mapping, vendor risk scoring, authentication, cloud deployment, and monitoring.


## 5. Main Data Flow

The main data flow describes how information moves through Arx AI from the moment a user starts a scan until the KRI dashboard and report are updated. This flow is important because it explains how the frontend, backend, database, scanner, AI enrichment service, risk engine, and reporting component work together.

The main workflow follows this path:

```text
User → Frontend Dashboard → Backend API → Redis Queue → Background Worker → Scanner Service → Sandbox Target → Raw Findings → AI Enrichment → Risk Scoring → KRI Dashboard → Report
```

---

### 5.1 Main Scan-to-KRI Flow

The primary data flow begins when the user starts a scan from the Arx AI frontend.

```text
1. User selects an approved sandbox target.
2. User clicks “Start Scan.”
3. Frontend sends a scan request to the Backend API.
4. Backend validates that the target is approved.
5. Backend creates a scan job in PostgreSQL.
6. Backend places the scan job into Redis Queue.
7. Background Worker picks up the scan job.
8. Scanner Service runs a safe scan against the sandbox target.
9. Scanner Service returns raw findings.
10. Raw findings are stored in PostgreSQL.
11. AI Enrichment Service analyzes each raw finding.
12. Enriched findings are stored in PostgreSQL.
13. Risk Scoring and KRI Engine calculates business risk scores.
14. Dashboard metrics are updated.
15. User views prioritized findings and KRI visualizations.
16. User generates a scan summary report.
```

This flow ensures that long-running work is handled asynchronously and that the frontend remains responsive while scans and AI processing are running.

---

### 5.2 Detailed Step-by-Step Data Flow

#### Step 1: User Opens the Dashboard

The user begins on the Arx AI dashboard. The dashboard requests the latest cyber risk summary from the Backend API.

```text
Frontend → GET /kri/summary → Backend API → PostgreSQL
```

The backend retrieves the current KRI metrics, such as:

```text
Total scans
Total findings
Critical findings
Average risk score
Highest-risk target
Highest-risk vendor
Most common vulnerability category
Recent risk trends
```

The dashboard displays this information using cards, charts, and tables.

---

#### Step 2: User Views Approved Sandbox Targets

The user navigates to the Targets page. The frontend requests a list of approved sandbox targets.

```text
Frontend → GET /targets → Backend API → PostgreSQL
```

The backend returns only preconfigured sandbox targets, such as:

```text
OWASP Juice Shop
DVWA
Custom vulnerable lab application
```

Each target includes metadata such as:

```text
Target ID
Target name
Internal URL
Application type
Vendor label
Environment label
Online/offline status
Created date
```

The frontend displays the targets in a table or card layout.

---

#### Step 3: User Starts a Scan

The user selects a sandbox target and clicks “Start Scan.”

```text
Frontend → POST /scans → Backend API
```

The request includes the selected target ID and scan type.

Example request body:

```json
{
  "target_id": "target_001",
  "scan_type": "baseline"
}
```

The backend does not accept arbitrary external URLs. It only accepts a target ID that already exists in the approved targets table.

---

#### Step 4: Backend Validates the Scan Request

Before creating the scan, the backend validates the request.

The backend checks:

```text
Does the target ID exist?
Is the target approved?
Is the target a sandbox target?
Is the target currently enabled?
Is the scan type allowed?
```

If validation fails, the backend rejects the request and returns an error.

If validation succeeds, the backend creates a scan job.

---

#### Step 5: Backend Creates a Scan Job

The backend creates a new record in the `scan_jobs` table.

The scan job includes:

```text
Scan ID
Target ID
Scan type
Status
Created timestamp
Started timestamp
Completed timestamp
Failure reason
Created-by user, as a stretch feature
```

The initial scan status is:

```text
queued
```

Example scan job:

```json
{
  "scan_id": "scan_123",
  "target_id": "target_001",
  "scan_type": "baseline",
  "status": "queued",
  "created_at": "2026-07-09T10:30:00"
}
```

The backend also creates an audit log entry showing that a scan was created.

---

#### Step 6: Backend Sends the Job to Redis Queue

After the scan job is created, the backend places the job into Redis Queue.

```text
Backend API → Redis Queue
```

The queued job contains enough information for the Background Worker to process it:

```text
Scan ID
Target ID
Scan type
Target internal URL
Allowed scan configuration
```

The backend then returns a response to the frontend.

Example response:

```json
{
  "scan_id": "scan_123",
  "status": "queued",
  "message": "Scan job created successfully."
}
```

This means the user does not need to wait for the scan to finish before the interface responds.

---

#### Step 7: Frontend Displays Scan Status

After receiving the scan creation response, the frontend displays the scan as queued.

The user can see scan progress through the Scans page or Scan Details page.

For the MVP, the frontend can check scan status using polling:

```text
Frontend → GET /scans/{scan_id}
```

Possible scan statuses include:

```text
queued
running
enriching
scoring
completed
failed
```

For a stretch feature, this can be upgraded to real-time updates using WebSockets or Server-Sent Events.

---

#### Step 8: Background Worker Picks Up the Scan Job

The Background Worker continuously watches Redis Queue for new jobs.

When the worker receives the scan job, it updates the scan status in PostgreSQL.

```text
Background Worker → PostgreSQL
```

The scan status changes from:

```text
queued → running
```

The worker also creates an audit log entry showing that scan execution started.

---

#### Step 9: Scanner Service Runs Against Sandbox Target

The Background Worker calls the Scanner Service.

```text
Background Worker → Scanner Service → Approved Sandbox Target
```

The Scanner Service runs only against the approved internal sandbox target.

The Scanner Service may use:

```text
OWASP ZAP baseline scan
Python wrapper scripts
Predefined safe scan profiles
Docker network isolation
```

The scanner is not allowed to scan arbitrary public URLs.

The target may be:

```text
OWASP Juice Shop
DVWA
Custom vulnerable lab application
```

The Scanner Service produces raw scanner output.

---

#### Step 10: Scanner Output Is Normalized

Scanner tools may return data in different formats. Arx AI should normalize scanner output into a consistent internal structure.

A normalized raw finding should include:

```text
Scan ID
Target ID
Finding title
Vulnerability type
Affected endpoint
Evidence summary
Technical severity
Confidence level
Scanner source
Timestamp
Raw reference
```

Example normalized raw finding:

```json
{
  "scan_id": "scan_123",
  "target_id": "target_001",
  "title": "Missing Anti-clickjacking Header",
  "vulnerability_type": "Security Misconfiguration",
  "affected_endpoint": "/login",
  "evidence_summary": "The response did not include a frame protection header.",
  "technical_severity": "Medium",
  "confidence": "High",
  "scanner_source": "OWASP ZAP Baseline",
  "timestamp": "2026-07-09T10:35:00"
}
```

This normalized format makes later AI enrichment, risk scoring, filtering, and reporting easier.

---

#### Step 11: Raw Findings Are Stored

After normalization, the Background Worker stores raw findings in PostgreSQL.

```text
Background Worker → PostgreSQL
```

The raw findings are stored before AI enrichment begins.

This is important because raw scanner evidence should be preserved even if AI enrichment fails.

The scan job status may change from:

```text
running → enriching
```

---

#### Step 12: AI Enrichment Begins

The AI Enrichment Service receives each raw finding and produces structured analysis.

```text
Raw Finding → AI Enrichment Service
```

The AI enrichment process should generate:

```text
Plain-English explanation
OWASP category
Business impact
Remediation recommendation
Suggested priority
AI confidence
Manual review flag
```

The AI output must be structured and validated before it is saved.

---

#### Step 13: AI Output Is Validated

AI output can be inconsistent, so Arx AI validates the output using a schema before storing it.

For example, the expected AI output may require:

```text
finding_id
explanation
owasp_category
business_impact
remediation
suggested_priority
ai_confidence
manual_review_required
```

If the AI output is valid, it is stored as an enriched finding.

If the AI output is invalid or enrichment fails, the raw finding is preserved and the finding is marked as requiring manual review.

This prevents AI failure from corrupting the system.

---

#### Step 14: Enriched Findings Are Stored

Validated AI-enriched findings are stored in PostgreSQL.

```text
AI Enrichment Service → PostgreSQL
```

An enriched finding may include:

```text
Raw finding ID
AI explanation
OWASP category
Business impact
Remediation guidance
Suggested priority
AI confidence
Manual review flag
Created timestamp
```

This creates a clear separation between original scanner evidence and AI-generated interpretation.

---

#### Step 15: Risk Scoring Is Calculated

After enrichment, the Risk Scoring and KRI Engine calculates a business risk score for each finding.

```text
Enriched Finding → Risk Scoring Engine
```

The risk score may consider:

```text
Technical severity
Exploitability
Asset criticality
Vendor exposure
Confidence level
Business impact
```

A simple MVP formula may be:

```text
Risk Score = Severity Weight × Exploitability × Asset Criticality × Vendor Exposure × Confidence
```

The score can then be normalized to a 0–100 scale.

Example risk score:

```json
{
  "finding_id": "finding_456",
  "risk_score": 82,
  "risk_level": "High",
  "priority_rank": 1
}
```

---

#### Step 16: KRI Metrics Are Updated

Once risk scores are calculated, the KRI Engine updates or recalculates dashboard metrics.

KRI metrics may include:

```text
Total scans
Total findings
Critical findings
Average risk score
Highest-risk target
Highest-risk vendor
Top vulnerability category
Risk trend over time
Findings by severity
Findings by OWASP category
Open high-risk findings
```

For the MVP, these metrics can be calculated directly from PostgreSQL when the dashboard requests them.

For a future version, Arx AI may store periodic KRI snapshots.

The scan job status changes from:

```text
scoring → completed
```

If any part fails, the status changes to:

```text
failed
```

with a stored failure reason.

---

#### Step 17: Dashboard Displays Updated Results

The frontend requests updated KRI data and findings.

```text
Frontend → GET /kri/summary
Frontend → GET /findings
Frontend → GET /scans/{scan_id}
```

The dashboard displays:

```text
Updated risk summary
Prioritized findings
Severity distribution
Risk trend charts
Target risk breakdown
Vendor risk breakdown
Latest scan status
```

The user can filter and sort the results by:

```text
Severity
Risk score
Target
Vendor
Date
OWASP category
Scan ID
```

---

#### Step 18: User Reviews Findings

The user can open a specific finding to see both raw and enriched information.

A finding detail view should show:

```text
Raw scanner evidence
Technical severity
Affected endpoint
AI explanation
OWASP mapping
Business impact
Risk score
Remediation recommendation
Manual review status
```

This is important because the user should be able to understand how the system moved from raw scanner output to business risk.

---

#### Step 19: User Generates a Report

The user can generate a report from a completed scan.

```text
Frontend → POST /reports/{scan_id}/generate → Backend API
```

The report generator pulls information from:

```text
Scan job
Target
Raw findings
Enriched findings
Risk scores
KRI metrics
```

The generated report includes:

```text
Executive summary
Scan details
Top findings
Risk scores
AI explanations
Remediation guidance
KRI summary
Ethical lab disclaimer
```

For the MVP, the report can be an HTML report page.

For a stretch feature, the report can be exported as a PDF.

---

### 5.3 Data Flow Diagram

The main data flow can be represented as follows:

```text
┌──────────────┐
│     User     │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  Frontend Dashboard  │
│  Next.js/TypeScript  │
└──────┬───────────────┘
       │ API Request
       ▼
┌──────────────────────┐
│     Backend API      │
│      FastAPI         │
└──────┬───────────────┘
       │ Validate target
       ▼
┌──────────────────────┐
│    PostgreSQL DB     │
│ Store scan job       │
└──────┬───────────────┘
       │ Queue job
       ▼
┌──────────────────────┐
│     Redis Queue      │
└──────┬───────────────┘
       │ Worker consumes job
       ▼
┌──────────────────────┐
│  Background Worker   │
└──────┬───────────────┘
       │ Run scan
       ▼
┌──────────────────────┐
│   Scanner Service    │
└──────┬───────────────┘
       │ Safe scan only
       ▼
┌──────────────────────┐
│  Sandbox Target App  │
└──────┬───────────────┘
       │ Raw scanner output
       ▼
┌──────────────────────┐
│   Raw Findings       │
│ Stored in database   │
└──────┬───────────────┘
       │ AI analysis
       ▼
┌──────────────────────┐
│ AI Enrichment Service│
└──────┬───────────────┘
       │ Validated output
       ▼
┌──────────────────────┐
│ Enriched Findings    │
│ Stored in database   │
└──────┬───────────────┘
       │ Calculate risk
       ▼
┌──────────────────────┐
│ Risk Scoring Engine  │
└──────┬───────────────┘
       │ Dashboard metrics
       ▼
┌──────────────────────┐
│    KRI Dashboard     │
└──────┬───────────────┘
       │ Generate report
       ▼
┌──────────────────────┐
│   Report Generator   │
└──────────────────────┘
```

---

### 5.4 Data States

During the main flow, scan and finding data move through different states.

#### Scan Job States

A scan job may have the following states:

```text
queued
running
enriching
scoring
completed
failed
```

Meaning:

```text
queued: The scan has been created and is waiting for a worker.
running: The scanner is actively scanning the sandbox target.
enriching: Raw findings are being analyzed by the AI enrichment service.
scoring: Risk scores and KRI metrics are being calculated.
completed: The scan workflow has finished successfully.
failed: The scan workflow failed and requires review.
```

#### Finding States

A finding may have the following states:

```text
raw
enriched
scored
manual_review_required
```

Meaning:

```text
raw: The finding has been collected from scanner output.
enriched: The finding has been analyzed by the AI enrichment service.
scored: The finding has a calculated business risk score.
manual_review_required: AI enrichment failed or produced invalid output.
```

---

### 5.5 Data Storage Points

Arx AI stores data at several important points in the workflow.

```text
1. When a scan is created:
   Store scan job metadata.

2. When a scan starts:
   Update scan status and start time.

3. When raw findings are collected:
   Store raw findings before AI enrichment.

4. When AI enrichment succeeds:
   Store enriched findings.

5. When AI enrichment fails:
   Store failure status and preserve raw findings.

6. When risk scoring completes:
   Store risk scores.

7. When the dashboard loads:
   Query stored findings and KRI metrics.

8. When a report is generated:
   Store report metadata.
```

This ensures that the system is traceable and reliable.

---

### 5.6 Error Handling Flow

Arx AI should handle failures safely.

#### Scan Failure

If the scanner fails:

```text
1. Background Worker catches the error.
2. Scan status is updated to failed.
3. Failure reason is stored.
4. Audit log entry is created.
5. Frontend displays a clear error message.
```

The system should not crash.

#### AI Enrichment Failure

If AI enrichment fails:

```text
1. Raw finding remains stored.
2. Enrichment status is marked as failed.
3. Finding is marked as manual_review_required.
4. Error is logged.
5. Risk scoring can either skip the finding or use fallback rule-based scoring.
```

The original scanner evidence should never be lost.

#### Report Generation Failure

If report generation fails:

```text
1. Report status is marked as failed.
2. Failure reason is stored.
3. User sees an understandable error message.
4. Scan and finding data remain unchanged.
```

---

### 5.7 MVP Data Flow vs Stretch Data Flow

For the MVP, the data flow can be simple:

```text
Frontend request
→ Backend API
→ Redis Queue
→ Background Worker
→ Scanner
→ Database
→ AI Enrichment
→ Risk Scoring
→ Dashboard
→ Basic HTML report
```

For stretch features, the data flow may be extended with:

```text
WebSockets or Server-Sent Events for real-time scan progress
PDF generation for executive reports
MITRE ATT&CK mapping during AI enrichment
Vendor risk scoring in the KRI engine
Authentication and role-based access control
Cloud deployment and CI/CD
Monitoring with Prometheus and Grafana
```

The MVP architecture should be designed so these stretch features can be added without changing the entire system.

---

### 5.8 Why This Data Flow Was Chosen

This data flow was chosen because it supports safety, reliability, and professional system design.

The frontend does not run scans directly. Instead, the frontend sends requests to the backend, and the backend controls what targets can be scanned. This helps enforce sandbox-only scanning rules.

Long-running tasks are placed into Redis Queue and handled by a Background Worker. This keeps the user interface responsive and prevents API requests from hanging.

Raw findings are stored before AI enrichment. This preserves the original scanner evidence and prevents AI errors from destroying important data.

AI enrichment is separated from scanning so the system can clearly distinguish between scanner evidence and AI-generated interpretation.

Risk scoring is separated from AI enrichment so the scoring formula can be documented, tested, and adjusted independently.

The KRI dashboard reads from stored data instead of relying on temporary scan output. This allows Arx AI to support scan history, trend analysis, filtering, reporting, and future vendor risk scoring.

Overall, this data flow turns Arx AI from a simple scanner into a modular cyber risk intelligence platform.


## 6. Technology Stack

The technology stack for Arx AI is selected to support a modern, modular, AI-powered cyber risk intelligence platform. The stack is designed to balance professional engineering practices with realistic capstone project scope.

The main goals behind the technology choices are:

1. Build a polished web dashboard.
2. Support safe vulnerability scanning in a sandbox.
3. Process long-running scan and AI tasks asynchronously.
4. Store structured scan, finding, risk, and report data.
5. Use AI in a structured and controlled way.
6. Support future improvements such as PDF reports, MITRE ATT&CK mapping, real-time scan progress, CI/CD, cloud deployment, and monitoring.

---

### 6.1 Technology Stack Summary

| Component            | Technology                              | Purpose                                                                      |
| -------------------- | --------------------------------------- | ---------------------------------------------------------------------------- |
| Frontend             | Next.js                                 | Web application framework                                                    |
| Frontend Language    | TypeScript                              | Type-safe frontend development                                               |
| Styling              | Tailwind CSS                            | Fast and consistent UI styling                                               |
| UI Components        | shadcn/ui                               | Professional dashboard components                                            |
| Charts               | Recharts                                | KRI visualizations and trend charts                                          |
| Tables               | TanStack Table                          | Searchable and filterable findings tables                                    |
| API State Management | TanStack Query                          | Fetching and caching backend data                                            |
| Backend API          | FastAPI                                 | Main backend API layer                                                       |
| Backend Language     | Python                                  | AI, security tooling, and backend logic                                      |
| Data Validation      | Pydantic                                | Request, response, and AI output validation                                  |
| ORM                  | SQLAlchemy                              | Database models and queries                                                  |
| Migrations           | Alembic                                 | Database schema migrations                                                   |
| Database             | PostgreSQL                              | Persistent relational data storage                                           |
| Background Jobs      | RQ                                      | Simple asynchronous job processing                                           |
| Queue Backend        | Redis                                   | Queue storage for background tasks                                           |
| Scanner              | OWASP ZAP Baseline Scan                 | Safe vulnerability scanning against sandbox targets                          |
| Scanner Control      | Python wrapper scripts                  | Run and normalize scanner output                                             |
| AI Workflow          | LangGraph                               | Structured AI enrichment workflow                                            |
| AI Utilities         | LangChain                               | LLM integrations and prompt utilities                                        |
| AI Model             | OpenAI API or local LLM                 | Generate explanations, classifications, and remediation                      |
| Containerization     | Docker                                  | Run app components in isolated containers                                    |
| Local Orchestration  | Docker Compose                          | Run frontend, backend, database, Redis, scanner, and sandbox targets locally |
| Reports              | HTML templates for MVP                  | Basic report generation                                                      |
| PDF Reports          | WeasyPrint or Playwright PDF export     | Stretch feature for executive report export                                  |
| Version Control      | Git and GitHub                          | Source control and portfolio visibility                                      |
| CI/CD                | GitHub Actions                          | Automated checks and deployment pipeline                                     |
| Deployment           | Vercel, Render, Fly.io, Railway, or AWS | Stretch feature for cloud deployment                                         |
| Monitoring           | Prometheus and Grafana                  | Stretch feature for observability                                            |

---

### 6.2 Frontend Stack

The frontend of Arx AI will be built using:

1. Next.js
2. TypeScript
3. Tailwind CSS
4. shadcn/ui
5. Recharts
6. TanStack Table
7. TanStack Query

---

#### 6.2.1 Next.js

Next.js will be used as the main frontend framework.

Arx AI needs a professional dashboard with multiple pages, including:

1. Dashboard page
2. Targets page
3. Scans page
4. Scan details page
5. Findings page
6. KRI dashboard page
7. Reports page

Next.js is a strong choice because it supports modern React development, routing, reusable components, and production-ready frontend structure.

For Arx AI, Next.js will mainly be used to build the user interface and communicate with the FastAPI backend.

---

#### 6.2.2 TypeScript

TypeScript will be used instead of plain JavaScript.

TypeScript helps catch errors earlier by adding type safety to frontend code. This is useful because Arx AI will pass structured data between the frontend and backend, including scan jobs, findings, risk scores, targets, and reports.

Example frontend types may include:

```ts
type ScanJob = {
  id: string;
  targetId: string;
  status: "queued" | "running" | "enriching" | "scoring" | "completed" | "failed";
  scanType: string;
  createdAt: string;
  completedAt?: string;
};

type Finding = {
  id: string;
  title: string;
  severity: "low" | "medium" | "high" | "critical";
  riskScore: number;
  targetName: string;
  owaspCategory?: string;
};
```

Using TypeScript makes the frontend more reliable and easier to maintain.

---

#### 6.2.3 Tailwind CSS

Tailwind CSS will be used for styling.

Arx AI needs a clean, polished dashboard interface. Tailwind makes it easier to build consistent spacing, colors, layouts, cards, tables, and responsive pages without writing large custom CSS files.

Tailwind will be used for:

1. Dashboard layout
2. Navigation sidebar
3. Cards
4. Tables
5. Filters
6. Status badges
7. Report pages

---

#### 6.2.4 shadcn/ui

shadcn/ui will be used for reusable UI components.

Arx AI will need many dashboard-style components, including:

1. Buttons
2. Cards
3. Tables
4. Dialogs
5. Dropdowns
6. Tabs
7. Badges
8. Forms
9. Toast notifications

Using shadcn/ui helps the project look more professional without building every UI component from scratch.

This is important because the dashboard presentation will strongly affect how impressive the final project feels during a demo.

---

#### 6.2.5 Recharts

Recharts will be used for data visualization.

The KRI dashboard will need charts such as:

1. Findings by severity
2. Risk trend over time
3. Findings by OWASP category
4. Risk by target
5. Risk by vendor
6. Critical findings by month

Recharts is suitable because it works well with React and is straightforward to use for dashboard visualizations.

---

#### 6.2.6 TanStack Table

TanStack Table will be used for displaying findings, scans, targets, and reports in interactive tables.

Arx AI will need tables that support:

1. Searching
2. Sorting
3. Filtering
4. Pagination
5. Column visibility
6. Row selection

This is especially important for the findings table because the user must be able to quickly identify high-priority vulnerabilities.

---

#### 6.2.7 TanStack Query

TanStack Query will be used to manage API data fetching from the FastAPI backend.

It will help with:

1. Fetching dashboard metrics
2. Fetching scan history
3. Fetching findings
4. Fetching target lists
5. Refetching scan status
6. Handling loading states
7. Handling errors
8. Caching API responses

For the MVP, TanStack Query can also support simple polling for scan status updates.

For example, the frontend may poll:

```text
GET /scans/{scan_id}
```

until the scan status becomes:

```text
completed
```

or:

```text
failed
```

---

### 6.3 Backend Stack

The backend of Arx AI will be built using:

1. FastAPI
2. Python
3. Pydantic
4. SQLAlchemy
5. Alembic

---

#### 6.3.1 FastAPI

FastAPI will be used as the main backend framework.

The backend API is responsible for:

1. Managing sandbox targets
2. Creating scan jobs
3. Returning scan history
4. Returning findings
5. Triggering background jobs
6. Returning KRI metrics
7. Returning report data
8. Enforcing sandbox-only scanning rules

FastAPI is a good choice because it is Python-based, modern, fast, and provides automatic API documentation. It also works well with Pydantic, which is useful for validating structured data.

Example backend endpoints may include:

```text
GET /health
GET /targets
POST /scans
GET /scans
GET /scans/{scan_id}
GET /findings
GET /kri/summary
GET /kri/trends
POST /reports/{scan_id}/generate
```

---

#### 6.3.2 Python

Python will be used for backend logic, scanning orchestration, AI enrichment, and risk scoring.

Python is suitable for Arx AI because it has strong support for:

1. Backend APIs
2. AI and LLM tooling
3. Security tooling
4. Data processing
5. Automation scripts
6. Background workers

Using Python across the backend, scanner wrapper, AI enrichment, and KRI engine keeps the project consistent and easier to maintain.

---

#### 6.3.3 Pydantic

Pydantic will be used for data validation.

It will validate:

1. API request bodies
2. API response structures
3. Scanner-normalized findings
4. AI-generated enrichment output
5. Risk scoring input and output

This is especially important for AI enrichment because LLM output can be inconsistent. Pydantic ensures that AI responses match the expected schema before they are stored in the database.

Example AI enrichment schema:

```python
class EnrichedFindingOutput(BaseModel):
    explanation: str
    owasp_category: str
    business_impact: str
    remediation: str
    suggested_priority: str
    ai_confidence: float
    manual_review_required: bool
```

---

#### 6.3.4 SQLAlchemy

SQLAlchemy will be used as the Object Relational Mapper.

It will help the backend interact with PostgreSQL using Python models.

Arx AI will likely have models such as:

1. Target
2. Vendor
3. Asset
4. ScanJob
5. RawFinding
6. EnrichedFinding
7. RiskScore
8. Report
9. AuditLog

SQLAlchemy is useful because Arx AI has many related database entities. For example:

```text
A target has many scans.
A scan has many raw findings.
A raw finding has one enriched finding.
An enriched finding has one risk score.
A scan can have one or more reports.
```

---

#### 6.3.5 Alembic

Alembic will be used for database migrations.

As the database schema changes, Alembic will track those changes in migration files. This is useful because the project will evolve over time.

For example, early in the MVP you may start with:

```text
targets
scan_jobs
raw_findings
```

Later, you may add:

```text
enriched_findings
risk_scores
reports
audit_logs
vendors
assets
```

Alembic allows these changes to be made in a controlled and repeatable way.

---

### 6.4 Database Stack

The main database will be:

1. PostgreSQL

---

#### 6.4.1 PostgreSQL

PostgreSQL will store all persistent Arx AI data.

This includes:

1. Approved sandbox targets
2. Vendors
3. Assets
4. Scan jobs
5. Raw findings
6. Enriched findings
7. Risk scores
8. KRI data
9. Report metadata
10. Audit logs

PostgreSQL is appropriate because Arx AI has structured relational data.

For example:

```text
targets → scan_jobs → raw_findings → enriched_findings → risk_scores
```

The relationships between these records matter, so a relational database is a strong fit.

PostgreSQL also supports powerful queries for dashboards, filtering, sorting, and trend analysis.

---

### 6.5 Background Processing Stack

Background processing will use:

1. Redis
2. RQ

---

#### 6.5.1 Redis

Redis will be used as the queue backend.

When a user starts a scan, the backend should not run the scan directly inside the API request. Instead, the backend creates a scan job and sends it to Redis Queue.

Redis helps store queued jobs until a worker is ready to process them.

---

#### 6.5.2 RQ

RQ, also known as Redis Queue, will be used for background jobs in the MVP.

RQ will handle jobs such as:

1. Running scans
2. Processing scanner output
3. Triggering AI enrichment
4. Calculating risk scores
5. Generating reports

RQ is recommended for the MVP because it is simpler than Celery and easier to understand.

A possible future upgrade is Celery, but RQ is enough for the first version of Arx AI.

---

### 6.6 Scanner Stack

The scanner layer will use:

1. OWASP ZAP Baseline Scan
2. Python wrapper scripts
3. Docker
4. Docker Compose

---

#### 6.6.1 OWASP ZAP Baseline Scan

OWASP ZAP Baseline Scan will be used as the main scanner for the MVP.

It is suitable because it can scan web applications in a controlled way and produce findings that can be normalized and stored.

The scanner will only run against approved sandbox targets such as:

1. OWASP Juice Shop
2. DVWA
3. A custom intentionally vulnerable lab application

The scanner will not be used against real public websites.

---

#### 6.6.2 Python Wrapper Scripts

Python wrapper scripts will control scanner execution and normalize scanner output.

The wrapper will be responsible for:

1. Receiving scan job information
2. Running the approved scanner configuration
3. Collecting scanner output
4. Converting scanner output into Arx AI’s internal finding format
5. Returning normalized findings to the background worker

The normalized output should include fields such as:

```text
title
vulnerability_type
affected_endpoint
evidence_summary
technical_severity
confidence
scanner_source
timestamp
```

This step is important because scanner tools can produce output in different formats. Arx AI should store findings in a consistent structure.

---

#### 6.6.3 Docker and Docker Compose

Docker will be used to containerize Arx AI components and sandbox targets.

Docker Compose will be used for local development and demo setup.

The local environment may include containers for:

1. Frontend
2. Backend API
3. PostgreSQL
4. Redis
5. Background worker
6. OWASP Juice Shop
7. DVWA
8. Scanner service

Docker Compose makes the project easier to run and demonstrate because the full environment can be started with one command.

---

### 6.7 AI Stack

The AI layer will use:

1. LangGraph
2. LangChain
3. OpenAI API or a local LLM
4. Pydantic validation
5. Optional vector database as a stretch feature

---

#### 6.7.1 LangGraph

LangGraph will be used to create the AI enrichment workflow.

The enrichment workflow may include steps such as:

```text
Raw finding
→ classify vulnerability
→ map to OWASP category
→ estimate business impact
→ generate remediation guidance
→ return structured output
```

LangGraph is useful because it allows the AI process to be structured as a workflow rather than a single unorganized prompt.

This makes Arx AI look more like a real AI engineering project.

---

#### 6.7.2 LangChain

LangChain will be used for LLM integration and prompt utilities.

It can help with:

1. Calling the AI model
2. Managing prompt templates
3. Structuring AI inputs
4. Handling model responses
5. Supporting future RAG features

LangChain should not be the entire project. It should be used as a tool inside the AI enrichment service.

---

#### 6.7.3 OpenAI API or Local LLM

The MVP can use an OpenAI API model for AI enrichment.

The AI model will generate:

1. Plain-English explanations
2. OWASP category suggestions
3. Business impact summaries
4. Remediation recommendations
5. Suggested priority
6. Confidence estimate

A local LLM can be considered later if the project needs to avoid API costs or demonstrate privacy-focused deployment.

For the MVP, using an API model is simpler and more reliable.

---

#### 6.7.4 Pydantic Validation for AI Output

AI output must be validated before storage.

This is necessary because LLMs can produce inconsistent or incomplete output.

Pydantic will enforce a structure such as:

```json
{
  "explanation": "string",
  "owasp_category": "string",
  "business_impact": "string",
  "remediation": "string",
  "suggested_priority": "string",
  "ai_confidence": 0.85,
  "manual_review_required": false
}
```

If the AI output does not match the schema, Arx AI should mark the finding as requiring manual review.

---

#### 6.7.5 Vector Database as Stretch Feature

A vector database may be added later for Retrieval-Augmented Generation.

Possible options:

1. ChromaDB
2. Qdrant

This would allow the AI enrichment service to retrieve reference material from:

1. OWASP documentation
2. Internal remediation guidance
3. Security policy notes
4. Previous findings

This should be considered a stretch feature, not part of the first MVP.

---

### 6.8 Risk Scoring and Analytics Stack

The risk scoring and KRI engine will use:

1. Python service layer
2. PostgreSQL queries
3. Optional Pandas

---

#### 6.8.1 Python Service Layer

The risk scoring logic will be implemented in the backend as a Python service module.

This module will calculate:

1. Per-finding risk score
2. Risk level
3. Priority rank
4. Average risk score
5. Critical finding count
6. Highest-risk target
7. Highest-risk vendor
8. Findings by severity
9. Findings by category
10. Risk trends over time

The risk scoring logic should be separate from both scanning and AI enrichment.

This makes the scoring formula easier to test, explain, and adjust.

---

#### 6.8.2 PostgreSQL Queries

PostgreSQL queries will be used to calculate dashboard metrics and retrieve filtered results.

Examples:

1. Count findings by severity
2. Calculate average risk score
3. Group findings by target
4. Group findings by vendor
5. Group findings by month
6. Retrieve top high-risk findings

For the MVP, dashboard metrics can be calculated directly from database queries.

For a future version, Arx AI may store periodic KRI snapshots.

---

#### 6.8.3 Pandas as Optional Tool

Pandas may be used later for more advanced analytics or report generation.

However, Pandas is not required for the first version.

The MVP should rely mainly on database queries and Python service functions.

---

### 6.9 Reporting Stack

The reporting layer will use:

1. HTML report templates for MVP
2. PDF generation as stretch feature

---

#### 6.9.1 HTML Report Templates

For the MVP, reports should be generated as HTML pages inside the Arx AI frontend.

A report page should include:

1. Executive summary
2. Scan details
3. Top findings
4. Risk scores
5. AI explanations
6. Remediation recommendations
7. KRI summary
8. Ethical lab disclaimer

This is enough for the first working version.

---

#### 6.9.2 PDF Export as Stretch Feature

PDF generation can be added after the MVP.

Possible PDF tools include:

1. WeasyPrint
2. ReportLab
3. Playwright PDF export

PDF export is useful because it makes the project feel more professional and enterprise-ready.

However, PDF export should not be built before the scan-to-dashboard workflow works.

---

### 6.10 DevOps and Deployment Stack

The DevOps and deployment stack will use:

1. Git
2. GitHub
3. GitHub Actions
4. Docker
5. Docker Compose
6. Cloud deployment platform as stretch feature

---

#### 6.10.1 Git and GitHub

Git will be used for version control.

GitHub will be used to host the repository and present the project as a portfolio piece.

The repository should include:

1. README
2. Setup instructions
3. Architecture documentation
4. Requirements document
5. Ethical-use disclaimer
6. Screenshots
7. Demo video link as a stretch feature

---

#### 6.10.2 GitHub Actions

GitHub Actions will be used for CI/CD as a stretch feature.

The pipeline may include:

1. Backend tests
2. Frontend linting
3. Type checking
4. Build verification
5. Docker image build
6. Deployment steps

This shows professional development workflow and makes the project more impressive to recruiters.

---

#### 6.10.3 Deployment Options

For the MVP, local Docker Compose deployment is enough.

For a stretch feature, cloud deployment can be added.

Possible deployment options:

1. Vercel for frontend
2. Render for backend
3. Fly.io for backend
4. Railway for full-stack deployment
5. Supabase or Neon for PostgreSQL
6. AWS as an advanced option

For a capstone, the recommended approach is:

```text
Frontend: Vercel
Backend: Render or Fly.io
Database: Supabase or Neon
Local sandbox targets: Docker Compose
```

The sandbox scanning environment may remain local because exposing vulnerable lab targets publicly would create unnecessary risk.

---

### 6.11 Monitoring and Observability Stack

Monitoring and observability are stretch features.

Possible tools include:

1. Prometheus
2. Grafana
3. Structured application logs
4. OpenTelemetry as an advanced stretch feature

---

#### 6.11.1 Prometheus

Prometheus can be used to collect system metrics.

Possible metrics include:

1. Number of scans started
2. Number of completed scans
3. Number of failed scans
4. Average scan duration
5. AI enrichment failures
6. Report generation failures

---

#### 6.11.2 Grafana

Grafana can be used to visualize monitoring data.

This is different from the Arx AI KRI dashboard.

The Arx AI dashboard is for security risk metrics.

Grafana is for system health and observability.

---

#### 6.11.3 Structured Logs

Structured logs should be used to help debug system behavior.

Logs may include:

1. Scan job started
2. Scan job completed
3. Scan job failed
4. AI enrichment started
5. AI enrichment failed
6. Report generated
7. Backend error

Logs should avoid exposing sensitive information.

---

### 6.12 Authentication and Authorization Stack

Authentication and authorization are stretch features.

Possible options include:

1. Auth.js / NextAuth for frontend authentication
2. FastAPI JWT authentication
3. Role-based access control
4. User and Role tables in PostgreSQL

For the MVP, authentication can be skipped if the project is running locally and used only for demonstration.

For the stretch version, Arx AI can include roles such as:

1. Security Analyst
2. Security Manager
3. Developer
4. Admin

Example permission differences:

```text
Security Analyst: start scans and review findings
Security Manager: view KRI dashboard and reports
Developer: view remediation guidance
Admin: manage approved sandbox targets
```

Authentication should only be added after the core MVP workflow is complete.

---

### 6.13 MVP Technology Stack

The MVP should use only the technologies needed to build the full core workflow.

The MVP stack is:

| Area               | MVP Technology                               |
| ------------------ | -------------------------------------------- |
| Frontend           | Next.js, TypeScript, Tailwind CSS, shadcn/ui |
| Charts             | Recharts                                     |
| Tables             | TanStack Table                               |
| Backend            | FastAPI, Python, Pydantic                    |
| Database           | PostgreSQL                                   |
| ORM and Migrations | SQLAlchemy, Alembic                          |
| Queue              | Redis, RQ                                    |
| Scanner            | OWASP ZAP Baseline Scan                      |
| AI                 | LangGraph, LangChain, OpenAI API             |
| Containers         | Docker, Docker Compose                       |
| Reports            | HTML report page                             |
| Version Control    | Git, GitHub                                  |

The MVP should not start with Kubernetes, Terraform, advanced monitoring, complex authentication, or multi-cloud deployment.

---

### 6.14 Stretch Technology Stack

The stretch stack includes technologies that can be added after the MVP works.

| Feature                 | Stretch Technology                                      |
| ----------------------- | ------------------------------------------------------- |
| PDF reports             | WeasyPrint, ReportLab, or Playwright PDF export         |
| Real-time scan progress | WebSockets or Server-Sent Events                        |
| MITRE ATT&CK mapping    | AI enrichment plus reference mapping table              |
| Vendor risk scoring     | PostgreSQL vendor and asset tables                      |
| Authentication          | JWT, Auth.js, or FastAPI auth                           |
| CI/CD                   | GitHub Actions                                          |
| Cloud deployment        | Vercel, Render, Fly.io, Railway, Supabase, Neon, or AWS |
| Monitoring              | Prometheus and Grafana                                  |
| Advanced AI/RAG         | ChromaDB or Qdrant                                      |
| Advanced orchestration  | Celery instead of RQ                                    |
| Infrastructure as Code  | Terraform                                               |
| Container orchestration | Kubernetes                                              |

These technologies should only be added if time allows.

---

### 6.15 Technology Choice Philosophy

The technology stack is intentionally divided into MVP technologies and stretch technologies.

The MVP stack is chosen to make sure Arx AI can be built successfully within a final-year project timeline. It focuses on the full end-to-end workflow:

```text
Target selection
→ scan job creation
→ background scan execution
→ raw finding storage
→ AI enrichment
→ risk scoring
→ KRI dashboard
→ basic report
```

The stretch stack is chosen to make the project more professional and industry-relevant after the MVP is complete.

This approach avoids overengineering early while still allowing the project to grow into a MAANG-level portfolio project.


## 7. Design Decisions and Justifications

This section explains the major design decisions made for Arx AI and why those decisions were chosen. The goal is to show that the architecture was not chosen randomly, but was designed around safety, maintainability, reliability, and professional software engineering practices.

---

### 7.1 Modular Architecture

Arx AI is designed using a modular architecture where each major responsibility is separated into its own component.

The main modules include:

1. Frontend Dashboard
2. Backend API
3. PostgreSQL Database
4. Background Worker
5. Scanner Service
6. AI Enrichment Service
7. Risk Scoring and KRI Engine
8. Report Generator
9. Sandbox Targets
10. Audit Logging Component

#### Justification

A modular architecture makes the system easier to understand, build, test, and extend. Each component has a clear responsibility.

For example, the Scanner Service is responsible only for collecting raw vulnerability findings, while the AI Enrichment Service is responsible for explaining and classifying those findings. The Risk Scoring Engine then converts enriched findings into business-level risk metrics.

This separation prevents the project from becoming one large, hard-to-maintain script.

A modular design also supports future growth. Features such as MITRE ATT&CK mapping, PDF reports, vendor risk scoring, authentication, cloud deployment, and monitoring can be added later without rewriting the entire system.

---

### 7.2 Frontend and Backend Separation

Arx AI separates the frontend dashboard from the backend API.

The frontend is responsible for:

1. Displaying data
2. Handling user interaction
3. Showing dashboard metrics
4. Rendering charts and tables
5. Displaying scan and report pages

The backend is responsible for:

1. Validating requests
2. Managing targets
3. Creating scan jobs
4. Triggering background work
5. Querying the database
6. Returning KRI data
7. Enforcing scanning restrictions

#### Justification

Separating the frontend and backend creates a cleaner and more professional architecture. The frontend should not directly control scans, access the database, or run security tools. Those responsibilities belong in the backend.

This separation improves security because the backend acts as a gatekeeper. For example, when the user starts a scan, the backend verifies that the selected target is an approved sandbox target before creating a scan job.

This also improves maintainability because frontend UI changes can be made without changing scanner logic, and backend logic can be improved without redesigning the user interface.

---

### 7.3 FastAPI for the Backend

FastAPI was selected as the backend framework for Arx AI.

#### Justification

FastAPI is a strong choice because Arx AI depends heavily on Python-based components, including scanner orchestration, AI enrichment, risk scoring, and data processing.

FastAPI also provides:

1. Strong integration with Pydantic
2. Automatic API documentation
3. Clear request and response models
4. Good performance
5. A modern development experience
6. Easy integration with background job systems

Since Arx AI uses structured data such as scan jobs, findings, enriched findings, and risk scores, FastAPI and Pydantic are a good match.

---

### 7.4 Next.js and TypeScript for the Frontend

Next.js and TypeScript were selected for the frontend dashboard.

#### Justification

Arx AI needs a polished and professional user interface. The dashboard must display targets, scan jobs, findings, KRI metrics, charts, filters, and reports.

Next.js is suitable because it supports modern React development, routing, reusable components, and production-style frontend organization.

TypeScript improves reliability because the frontend will handle structured data from the backend. For example, scan jobs have specific statuses, findings have severity levels, and risk scores are numeric values. TypeScript helps catch mistakes before runtime.

This makes the frontend easier to maintain as the project grows.

---

### 7.5 PostgreSQL for Persistent Storage

PostgreSQL was selected as the main database.

#### Justification

Arx AI contains structured relational data. For example:

1. A target can have many scans.
2. A scan can have many raw findings.
3. A raw finding can have one enriched finding.
4. An enriched finding can have one risk score.
5. A scan can generate one or more reports.
6. Audit logs can be connected to scans, reports, and users.

Because these relationships are important, a relational database is a strong fit.

PostgreSQL also supports filtering, sorting, aggregation, and historical queries, which are important for the KRI dashboard.

For example, the dashboard may need to calculate:

1. Findings by severity
2. Average risk score
3. Risk trends by month
4. Highest-risk target
5. Highest-risk vendor
6. Most common vulnerability category

PostgreSQL is reliable, widely used in industry, and appropriate for this type of application.

---

### 7.6 Asynchronous Background Jobs

Arx AI uses a background worker system for long-running tasks.

Long-running tasks include:

1. Running vulnerability scans
2. Processing scanner output
3. Running AI enrichment
4. Calculating risk scores
5. Generating reports

#### Justification

These tasks may take several seconds or longer. If they were executed directly inside an API request, the frontend could freeze or the request could time out.

By using Redis Queue and a background worker, Arx AI can create a scan job quickly and let the worker process it asynchronously.

This improves:

1. Responsiveness
2. Reliability
3. User experience
4. System organization
5. Future scalability

The user can start a scan, receive a scan ID, and continue using the dashboard while the scan runs in the background.

---

### 7.7 Redis Queue and RQ for the MVP

Redis Queue, also known as RQ, was selected for MVP background processing.

#### Justification

RQ is simpler than more advanced task systems such as Celery. Since Arx AI is a final-year project, the first priority is to build a complete and understandable system.

RQ provides enough functionality for the MVP:

1. Queue scan jobs
2. Run background workers
3. Track job execution
4. Separate long-running tasks from API requests

Celery may be considered later if the project needs more advanced task scheduling, retries, or distributed workers. For the MVP, RQ keeps the system manageable while still demonstrating asynchronous processing.

---

### 7.8 Sandbox-Only Scanning

Arx AI is designed to scan only approved sandbox targets.

The system does not allow users to enter arbitrary public URLs.

#### Justification

This is one of the most important design decisions in the project.

Arx AI is a cybersecurity-related platform, so it must be designed responsibly. Allowing arbitrary URL scanning would create ethical, legal, and safety risks.

By limiting scans to preconfigured sandbox targets, Arx AI stays focused on:

1. Education
2. Defensive security
3. Risk analysis
4. Controlled testing
5. Safe demonstration

The approved target model also makes the project easier to demo because the same targets can be scanned repeatedly in a predictable environment.

This design decision shows responsible cybersecurity engineering.

---

### 7.9 Using Existing Scanning Tools Instead of Building a Scanner From Scratch

Arx AI uses safe scanner orchestration instead of trying to build a full vulnerability scanner from scratch.

For the MVP, the scanner layer may use:

1. OWASP ZAP baseline scan
2. Python wrapper scripts
3. Predefined scan profiles
4. Docker network isolation

#### Justification

Building a professional vulnerability scanner from scratch is outside the realistic scope of a final-year project.

The strongest value of Arx AI is not simply detecting vulnerabilities. The stronger value is the full pipeline:

```text
Safe scan execution
→ raw finding collection
→ AI enrichment
→ business risk scoring
→ KRI visualization
→ report generation
```

Using an existing scanner allows the project to focus on orchestration, data processing, AI analysis, risk scoring, and dashboard design.

This also makes the project more realistic because many enterprise platforms integrate and normalize findings from existing tools instead of reinventing every scanner internally.

---

### 7.10 Normalizing Scanner Output

Arx AI normalizes raw scanner output into a consistent internal format before storing it.

A normalized finding includes fields such as:

1. Scan ID
2. Target ID
3. Finding title
4. Vulnerability type
5. Affected endpoint
6. Evidence summary
7. Technical severity
8. Confidence level
9. Scanner source
10. Timestamp

#### Justification

Different scanners may produce output in different formats. If Arx AI stores raw scanner output without normalization, it becomes harder to enrich, score, filter, and report findings.

Normalization creates a stable internal format that the rest of the system can depend on.

This makes it easier to:

1. Store findings consistently
2. Run AI enrichment
3. Calculate risk scores
4. Filter findings in the UI
5. Generate reports
6. Add additional scanners later

Normalization is an important data engineering decision.

---

### 7.11 Storing Raw Findings Before AI Enrichment

Arx AI stores raw scanner findings before sending them to the AI Enrichment Service.

#### Justification

Raw scanner evidence should be preserved before AI interpretation is added.

This is important because AI-generated content may be incomplete, incorrect, or fail validation. If the system only stored AI-enriched output, then a failed AI process could result in lost evidence.

By storing raw findings first, Arx AI maintains traceability.

The system can always show:

1. What the scanner originally found
2. What the AI later interpreted
3. How the risk score was calculated
4. Whether manual review is required

This design improves reliability, transparency, and trust.

---

### 7.12 Separating Raw Findings From AI-Enriched Findings

Arx AI stores raw findings and AI-enriched findings separately.

#### Justification

Scanner output and AI-generated interpretation are not the same thing.

Raw findings are original evidence from the scanner. AI-enriched findings are explanations, classifications, remediation suggestions, and business impact summaries generated by the AI layer.

Separating them helps users understand what is evidence and what is interpretation.

This is especially important because AI output should not be treated as unquestionable truth. The system should make it clear when information came from the scanner and when it came from the AI enrichment process.

This improves transparency and supports responsible AI use.

---

### 7.13 Structured AI Output

Arx AI requires the AI Enrichment Service to return structured output instead of free-form text only.

The AI output should include fields such as:

1. Explanation
2. OWASP category
3. Business impact
4. Remediation guidance
5. Suggested priority
6. AI confidence
7. Manual review flag

#### Justification

Structured AI output is easier to validate, store, display, filter, and use in risk scoring.

Without structured output, the AI would behave more like a chatbot. That would make the system harder to integrate into the dashboard and reports.

By requiring structured JSON output, Arx AI uses AI as a controlled component inside a larger software system.

This is a stronger engineering design than simply displaying AI-generated paragraphs.

---

### 7.14 Validating AI Output With Pydantic

Arx AI validates AI-generated output using Pydantic schemas before storing it.

#### Justification

AI models can produce incomplete, inconsistent, or incorrectly formatted output.

Validation is necessary to protect the reliability of the system.

If AI output is valid, the enriched finding is stored.

If AI output is invalid, the finding is marked as requiring manual review.

This prevents unreliable AI responses from corrupting the database or dashboard.

This design decision shows responsible AI engineering.

---

### 7.15 Separating AI Enrichment From Risk Scoring

AI enrichment and risk scoring are separate components.

The AI Enrichment Service explains and classifies findings.

The Risk Scoring and KRI Engine calculates numeric business risk scores.

#### Justification

Risk scoring should be explainable and consistent. If the AI directly produced final risk scores without a documented scoring formula, the system would be harder to justify.

By separating AI enrichment from risk scoring, Arx AI can use AI for interpretation while still using a documented formula for prioritization.

This makes the risk calculation:

1. More transparent
2. Easier to test
3. Easier to adjust
4. Easier to explain in a presentation
5. Less dependent on unpredictable AI output

This is an important design decision for a serious cybersecurity platform.

---

### 7.16 Risk Scoring Formula

Arx AI uses a documented risk scoring formula to calculate business risk.

A simple MVP formula may be:

```text
Risk Score = Severity Weight × Exploitability × Asset Criticality × Vendor Exposure × Confidence
```

The score can then be normalized to a 0–100 scale.

#### Justification

A risk score helps the user prioritize findings.

A scanner may produce many findings, but not all findings are equally important. The risk scoring formula helps answer:

1. Which finding should be fixed first?
2. Which target creates the most risk?
3. Which vendor has the highest exposure?
4. Is the overall risk increasing or decreasing?

The formula is intentionally documented so that the user can understand how the system calculates priority.

This supports transparency and makes the dashboard more meaningful.

---

### 7.17 KRI Dashboard Instead of Only a Findings List

Arx AI includes a KRI dashboard instead of only displaying raw vulnerability findings.

#### Justification

A findings list is useful, but it does not fully solve the main pain point of the project.

The main problem is that security teams often receive many technical findings and struggle to prioritize and communicate them.

The KRI dashboard helps convert technical data into business-level insight.

Examples of KRIs include:

1. Total findings
2. Critical findings
3. Average risk score
4. Highest-risk target
5. Highest-risk vendor
6. Risk trend over time
7. Findings by severity
8. Findings by OWASP category

This makes Arx AI more valuable than a basic scanner.

---

### 7.18 HTML Reports for MVP, PDF Reports as Stretch

For the MVP, Arx AI will generate report pages in HTML. PDF export is treated as a stretch feature.

#### Justification

The most important part of the report is the content, not the file format.

An HTML report page can still show:

1. Executive summary
2. Scan details
3. Top findings
4. AI explanations
5. Risk scores
6. Remediation guidance
7. KRI summary
8. Ethical lab disclaimer

PDF generation can be added later once the core workflow is working.

This prevents the project from spending too much time on formatting before the main scan-to-dashboard pipeline is complete.

---

### 7.19 Docker Compose for Local Development and Demo

Arx AI uses Docker and Docker Compose for local development and demonstration.

Docker Compose can run:

1. Frontend
2. Backend API
3. PostgreSQL
4. Redis
5. Background Worker
6. Scanner Service
7. Sandbox Targets

#### Justification

Docker Compose makes the project easier to set up and demo.

Instead of manually installing every dependency, the full system can be started with a consistent environment.

This is especially useful because Arx AI depends on multiple services.

Docker also helps isolate sandbox targets from real systems, which supports the ethical and safety goals of the project.

---

### 7.20 Local Sandbox Targets Instead of Public Deployment of Vulnerable Apps

The sandbox targets should run locally or in a controlled private environment.

#### Justification

Intentionally vulnerable applications should not be publicly exposed without strong controls.

Keeping sandbox targets local reduces risk and keeps the project safe.

The frontend and backend may be deployed later as stretch features, but the vulnerable scanning environment should remain controlled.

This decision supports responsible cybersecurity practice.

---

### 7.21 Polling for MVP, Real-Time Updates as Stretch

For the MVP, the frontend can poll the backend for scan status.

Example:

```text
GET /scans/{scan_id}
```

The frontend can check periodically until the scan status becomes:

```text
completed
```

or:

```text
failed
```

Real-time updates using WebSockets or Server-Sent Events can be added later.

#### Justification

Polling is simpler to implement and good enough for the MVP.

Real-time updates are more impressive, but they add extra complexity. Treating real-time progress as a stretch feature keeps the MVP manageable.

This follows a practical engineering approach: build the simplest working version first, then improve it.

---

### 7.22 MVP-First Development Strategy

Arx AI is designed to be built MVP-first.

The MVP focuses on the complete end-to-end workflow:

```text
Target selection
→ scan job creation
→ background scan execution
→ raw finding storage
→ AI enrichment
→ risk scoring
→ KRI dashboard
→ basic report
```

#### Justification

The project has many possible advanced features, but trying to build everything at once would increase the risk of not finishing.

The MVP-first strategy ensures that the core idea is proven early.

Once the MVP works, stretch features can be added safely.

This approach also matches professional software development practices, where a working vertical slice is built before expanding the system.

---

### 7.23 Avoiding Early Overengineering

Arx AI intentionally avoids starting with complex technologies such as Kubernetes, Terraform, advanced monitoring, multi-cloud deployment, or complex authentication.

#### Justification

These technologies are valuable, but they should not be implemented before the core product works.

The first priority is to prove that Arx AI can complete the main workflow.

Advanced infrastructure should only be added after the scan-to-dashboard workflow is stable.

This prevents the project from becoming impressive on paper but unfinished in practice.

---

### 7.24 Future-Ready Architecture

Although the MVP is kept manageable, the architecture is designed to support future extensions.

Possible future extensions include:

1. PDF executive report generation
2. Vendor risk scoring
3. MITRE ATT&CK mapping
4. Real-time scan progress
5. Authentication and role-based access control
6. CI/CD and cloud deployment
7. Monitoring and observability
8. Vector database for RAG
9. Additional sandbox targets
10. Additional scanner integrations

#### Justification

A good architecture should support future growth without requiring a full rewrite.

By separating the system into modules, Arx AI can start simple and later evolve into a more advanced platform.

This makes the project both realistic for a capstone and strong enough for a professional portfolio.

---

### 7.25 Summary of Key Design Decisions

The main design decisions for Arx AI are:

1. Use a modular architecture.
2. Separate frontend from backend.
3. Use FastAPI for the backend.
4. Use Next.js and TypeScript for the frontend.
5. Use PostgreSQL for persistent relational data.
6. Use Redis Queue and a background worker for long-running tasks.
7. Restrict scanning to approved sandbox targets.
8. Use existing safe scanner tooling instead of building a scanner from scratch.
9. Normalize scanner output into a consistent internal format.
10. Store raw findings before AI enrichment.
11. Separate raw scanner evidence from AI-generated interpretation.
12. Validate AI output before storage.
13. Separate AI enrichment from risk scoring.
14. Use a documented risk scoring formula.
15. Build a KRI dashboard instead of only a findings list.
16. Use HTML reports for MVP and PDF reports as a stretch feature.
17. Use Docker Compose for local development and demo.
18. Keep vulnerable targets local or controlled.
19. Use polling for MVP and real-time updates as a stretch feature.
20. Follow an MVP-first development strategy.
21. Avoid early overengineering.
22. Design the system to support future extensions.

These decisions support the main goal of Arx AI: to safely convert sandbox vulnerability findings into AI-enriched, prioritized cyber risk intelligence that can be reviewed through a professional KRI dashboard.


## 8. Security and Ethical Boundaries

Arx AI is a cybersecurity-related platform, so security and ethical boundaries are a core part of the system design. The project is intended for educational, defensive, and authorized testing only. It must be designed in a way that prevents misuse and clearly communicates its limitations.

The purpose of Arx AI is not to attack real systems. The purpose is to demonstrate how vulnerability findings from controlled sandbox environments can be collected, enriched with AI, scored for business risk, and displayed through a professional KRI dashboard.

---

### 8.1 Ethical Purpose

Arx AI is designed for:

1. Educational cybersecurity learning.
2. Defensive application security analysis.
3. Safe testing against intentionally vulnerable lab applications.
4. Demonstrating vulnerability prioritization and cyber risk communication.
5. Helping users understand how raw technical findings can become business-level risk insights.

Arx AI is not designed for:

1. Unauthorized scanning.
2. Real-world exploitation.
3. Attacking public websites.
4. Stealing data.
5. Bypassing security controls.
6. Damaging systems.
7. Hiding malicious activity.
8. Automating offensive actions against unknown targets.

This boundary is important because the project involves security scanning and AI analysis. The system must be framed and implemented responsibly.

---

### 8.2 Approved Sandbox Targets Only

Arx AI shall only scan approved sandbox targets that are preconfigured inside the system.

Approved targets may include:

1. OWASP Juice Shop.
2. DVWA.
3. A custom intentionally vulnerable lab application.
4. Other local test applications created specifically for the project.

The system shall not allow users to enter arbitrary public URLs.

The target selection workflow should use target IDs from the database rather than user-submitted URLs. This ensures that the backend controls which environments can be scanned.

Example safe flow:

```text id="mizv2o"
User selects target ID
→ Backend checks target exists
→ Backend checks target is approved
→ Backend retrieves internal sandbox URL
→ Scan job is created
```

Unsafe flow that should not be allowed:

```text id="k29zbb"
User enters any public URL
→ System scans external target
```

This restriction is one of the most important safety controls in Arx AI.

---

### 8.3 No Public Website Scanning

Arx AI shall not scan public websites or systems on the internet.

The project should not include a feature where the user can type:

```text id="o7lcaz"
https://example.com
```

and scan that target.

This is out of scope because public website scanning can create legal and ethical issues if performed without explicit authorization.

Instead, all target URLs should be stored and managed internally by the project.

For example, the database may store approved internal targets such as:

```text id="rkqag9"
http://juice-shop:3000
http://dvwa:80
http://custom-vulnerable-api:8000
```

These targets should run inside the local Docker network or another controlled lab environment.

---

### 8.4 No Destructive Actions

Arx AI shall not perform destructive actions against any target.

The scanner configuration should avoid behavior that could:

1. Delete data.
2. Modify application state in harmful ways.
3. Overload services.
4. Attempt persistence.
5. Attempt privilege escalation on real systems.
6. Exfiltrate data.
7. Bypass authentication in unauthorized environments.
8. Disrupt availability.

For the MVP, Arx AI should focus on safe baseline scanning, passive checks, controlled lab testing, and risk analysis.

The system should be built to demonstrate security engineering maturity, not aggressive exploitation.

---

### 8.5 Controlled Scanner Configuration

The Scanner Service shall use predefined scan configurations.

The user should not be able to freely customize dangerous scanner behavior.

The scanner configuration should be controlled by the backend and project developer.

Recommended scanner controls include:

1. Use safe scan profiles.
2. Limit scanning to sandbox URLs.
3. Avoid destructive scan modes.
4. Run scanner inside Docker.
5. Keep scanning inside an internal Docker network.
6. Log every scan job.
7. Store scan status and failure reasons.
8. Prevent unknown external target input.

This design keeps scanning predictable, safe, and suitable for academic demonstration.

---

### 8.6 AI Safety Boundaries

The AI Enrichment Service shall be used for defensive analysis and explanation only.

The AI should generate:

1. Plain-English vulnerability explanations.
2. OWASP category mapping.
3. Business impact summaries.
4. Remediation recommendations.
5. Prioritization support.
6. Executive summaries.

The AI should not generate:

1. Step-by-step exploitation instructions.
2. Instructions for attacking real systems.
3. Instructions for evading detection.
4. Instructions for stealing credentials or data.
5. Instructions for persistence or privilege escalation.
6. Instructions for bypassing security tools.
7. Payloads intended for use against real systems.

The AI layer should focus on helping the user understand and fix risk, not exploit systems.

---

### 8.7 Separation of Evidence and AI Interpretation

Arx AI shall clearly separate raw scanner evidence from AI-generated interpretation.

Raw scanner evidence includes:

1. Scanner source.
2. Finding title.
3. Affected endpoint.
4. Technical severity.
5. Evidence summary.
6. Confidence.
7. Timestamp.

AI-generated interpretation includes:

1. Plain-English explanation.
2. OWASP category.
3. Business impact.
4. Remediation guidance.
5. Suggested priority.
6. AI confidence.
7. Manual review flag.

This separation is important because AI output may be incomplete or incorrect. The user should be able to see what came directly from the scanner and what was generated by AI.

This supports transparency, reliability, and responsible AI use.

---

### 8.8 AI Output Validation

AI-generated output shall be validated before it is stored or displayed as structured risk intelligence.

The system should validate that AI output includes required fields such as:

1. Explanation.
2. OWASP category.
3. Business impact.
4. Remediation guidance.
5. Suggested priority.
6. AI confidence.
7. Manual review flag.

If AI output is missing required fields or does not match the expected schema, the system should:

1. Preserve the raw finding.
2. Mark the enrichment as failed.
3. Mark the finding as requiring manual review.
4. Log the failure.
5. Avoid using the invalid AI output for final risk scoring unless fallback rules are applied.

This prevents unreliable AI output from corrupting the dashboard, reports, or database.

---

### 8.9 No Real Sensitive Data

Arx AI shall not store real company data, real customer data, real passwords, real API keys, production logs, or private user information.

The project should use:

1. Fake vendors.
2. Fake assets.
3. Fake business units.
4. Sandbox scan data.
5. Demo risk scenarios.
6. Intentionally vulnerable lab applications.

If sample credentials are needed for a lab target, they should be clearly marked as demo-only and should never be reused outside the lab.

This keeps the project safe and avoids unnecessary privacy or data protection concerns.

---

### 8.10 Secrets Management

Arx AI shall not hardcode secrets into the source code.

Sensitive configuration values should be stored using environment variables.

Examples include:

1. Database URL.
2. Redis URL.
3. OpenAI API key or model provider key.
4. JWT secret as a stretch feature.
5. Deployment credentials as a stretch feature.

The repository should include a sample environment file such as:

```text id="hbr766"
.env.example
```

but not the real `.env` file.

The real `.env` file should be excluded using:

```text id="v0ou2w"
.gitignore
```

This shows professional security practice.

---

### 8.11 Audit Logging

Arx AI shall maintain audit logs for important system actions.

Audit logs should record events such as:

1. Scan created.
2. Scan started.
3. Scan completed.
4. Scan failed.
5. Raw findings stored.
6. AI enrichment completed.
7. AI enrichment failed.
8. Risk scoring completed.
9. Report generated.
10. Report generation failed.

Each audit log should include:

1. Event type.
2. Timestamp.
3. Related scan ID.
4. Related target ID.
5. Event status.
6. Description or message.
7. User ID as a stretch feature.

Audit logs improve traceability and help explain what happened during system execution.

---

### 8.12 Error Handling and Safe Failure

Arx AI should fail safely.

If a scan fails, the system should:

1. Mark the scan as failed.
2. Store the failure reason.
3. Create an audit log entry.
4. Display a clear error message.
5. Avoid crashing the whole application.

If AI enrichment fails, the system should:

1. Preserve the raw finding.
2. Mark the finding as requiring manual review.
3. Log the enrichment failure.
4. Avoid storing invalid AI output.

If report generation fails, the system should:

1. Preserve scan and finding data.
2. Mark the report generation attempt as failed.
3. Store the failure reason.
4. Display a clear message to the user.

Safe failure is important because security-related systems must preserve evidence and avoid data corruption.

---

### 8.13 Documentation Disclaimer

The project documentation shall include a clear ethical-use disclaimer.

The disclaimer should state that:

1. Arx AI is for educational and authorized defensive testing only.
2. Arx AI should only be used against sandboxed or explicitly authorized targets.
3. The project does not support scanning real public websites.
4. The project does not support destructive actions.
5. The vulnerability findings are generated in a controlled lab environment.
6. The platform is not a replacement for professional security tools or expert review.

Example disclaimer:

```text id="xj4pv2"
Arx AI is an educational cyber risk intelligence platform designed for authorized testing against sandboxed, intentionally vulnerable applications. It must not be used to scan, attack, or assess systems without explicit permission. The project focuses on defensive security analysis, risk prioritization, and remediation guidance.
```

This disclaimer should appear in:

1. README.
2. Architecture documentation.
3. Report footer.
4. Demo presentation.
5. Optional application settings or about page.

---

### 8.14 User-Facing Report Boundaries

Reports generated by Arx AI should focus on defensive and remediation-oriented content.

Reports should include:

1. Executive summary.
2. Risk score.
3. Severity.
4. Business impact.
5. OWASP mapping.
6. Affected sandbox target.
7. Remediation guidance.
8. Ethical lab disclaimer.

Reports should avoid:

1. Step-by-step exploitation instructions.
2. Payloads intended for real systems.
3. Guidance for bypassing security controls.
4. Instructions for hiding activity.
5. Language that encourages unauthorized testing.

This ensures that the reports communicate risk responsibly.

---

### 8.15 Network Isolation

Sandbox targets should run in a controlled local or containerized environment.

For local development, Docker Compose should create an internal network for:

1. Backend API.
2. Scanner Service.
3. Sandbox targets.
4. Database.
5. Redis.
6. Background worker.

The scanner should only be configured to reach approved sandbox targets.

Network isolation helps reduce the chance that scans accidentally reach external systems.

For a deployed version, extra care should be taken not to expose intentionally vulnerable applications publicly.

---

### 8.16 Role-Based Access as a Stretch Boundary

Authentication and role-based access control are stretch features, but the architecture should allow them later.

Possible roles include:

1. Security Analyst.
2. Security Manager.
3. Developer.
4. Admin.

Possible access controls include:

1. Security Analysts can start scans.
2. Security Managers can view dashboards and reports.
3. Developers can view remediation guidance.
4. Admins can manage approved sandbox targets.
5. Only authorized users can generate reports.

Although this may not be part of the MVP, documenting it shows that Arx AI is designed with enterprise security practices in mind.

---

### 8.17 Responsible Demonstration Rules

During presentations, demos, or portfolio reviews, Arx AI should be demonstrated only against sandbox targets.

A responsible demo should show:

1. The approved target list.
2. The scan being started against a lab target.
3. The scan job status.
4. Raw findings.
5. AI-enriched findings.
6. Risk scores.
7. KRI dashboard metrics.
8. A report with an ethical-use disclaimer.

The demo should not show scanning of a real website or any system that is not part of the controlled lab.

This keeps the project professional and avoids giving the wrong impression.

---

### 8.18 Security and Ethical Boundary Summary

The main security and ethical boundaries of Arx AI are:

1. Arx AI is for educational, defensive, and authorized testing only.
2. Arx AI only scans approved sandbox targets.
3. Arx AI does not scan public websites.
4. Arx AI does not attack real systems.
5. Arx AI does not perform destructive actions.
6. Arx AI does not store real sensitive data.
7. Arx AI does not hardcode secrets.
8. Arx AI separates raw evidence from AI interpretation.
9. Arx AI validates AI output before storing it.
10. Arx AI logs important system events.
11. Arx AI reports focus on risk, remediation, and defensive analysis.
12. Arx AI documentation clearly explains ethical-use limitations.

These boundaries ensure that Arx AI demonstrates responsible cybersecurity engineering while still showing advanced technical skills in AI, security, backend systems, data processing, and risk visualization.

## 9. Future Architecture Extensions

The MVP architecture of Arx AI is designed to be simple enough to build within a final-year project timeline while still supporting advanced future improvements. These future architecture extensions are not required for the first working version, but they can make the project more professional, scalable, and industry-relevant after the MVP is complete.

The most important principle is that these extensions should be added only after the core scan-to-dashboard workflow is working.

The MVP workflow is:

```text
Approved target selection
→ scan job creation
→ background scan execution
→ raw finding storage
→ AI enrichment
→ risk scoring
→ KRI dashboard
→ basic report
```

Once that workflow is stable, the following extensions can be added.

---

### 9.1 PDF Executive Report Generation

The MVP will support a basic HTML report page. A future extension is to generate downloadable PDF executive reports.

#### Purpose

PDF reports make Arx AI feel more like a professional enterprise security platform. They allow users to share cyber risk summaries with managers, executives, developers, or academic evaluators.

#### Future Capabilities

PDF reports may include:

1. Executive summary.
2. Scan details.
3. Top high-risk findings.
4. Severity distribution.
5. Risk score summary.
6. OWASP category breakdown.
7. Vendor risk summary.
8. Remediation recommendations.
9. Ethical-use disclaimer.
10. Charts and tables from the KRI dashboard.

#### Possible Technologies

PDF generation could use:

1. WeasyPrint.
2. ReportLab.
3. Playwright PDF export.

#### Architectural Impact

The Report Generator component would be extended to support PDF rendering. The backend would collect scan, finding, enrichment, risk, and KRI data, then pass it into a report template.

Possible endpoint:

```text
POST /reports/{scan_id}/generate-pdf
```

The generated PDF could be stored locally or in object storage as a future cloud extension.

---

### 9.2 Vendor Risk Scoring

The MVP may include basic vendor labels, but a future extension is to create a full vendor risk scoring system.

#### Purpose

Vendor risk scoring helps the user understand which third-party vendors or simulated business units contribute the most cyber risk.

This makes Arx AI more enterprise-focused because many organizations need to assess not only technical vulnerabilities, but also the business impact of vendors and external systems.

#### Future Capabilities

Vendor risk scoring may include:

1. Vendor profiles.
2. Vendor criticality.
3. Number of findings per vendor.
4. Critical findings per vendor.
5. Average risk score per vendor.
6. Risk trend by vendor.
7. Vendor exposure score.
8. Vendor comparison charts.
9. Vendor-specific reports.

#### Possible Database Additions

Additional tables may include:

```text
vendors
vendor_assets
vendor_risk_scores
vendor_kri_snapshots
```

#### Architectural Impact

The KRI Engine would be extended to calculate vendor-level metrics. The frontend dashboard would add vendor-specific charts, filters, and report sections.

Possible endpoint:

```text
GET /kri/vendors
```

---

### 9.3 MITRE ATT&CK Mapping

The MVP will focus on OWASP category mapping. A future extension is to map findings to MITRE ATT&CK tactics and techniques.

#### Purpose

MITRE ATT&CK mapping makes the project more security-professional and helps connect application vulnerabilities to broader adversary behavior.

#### Future Capabilities

MITRE ATT&CK mapping may include:

1. Mapping findings to ATT&CK technique IDs.
2. Displaying tactic and technique names.
3. Filtering findings by ATT&CK tactic.
4. Showing ATT&CK technique distribution.
5. Including ATT&CK references in reports.
6. Combining OWASP and MITRE mappings in the AI enrichment output.

#### Possible Database Additions

Additional fields or tables may include:

```text
mitre_tactic
mitre_technique_id
mitre_technique_name
finding_mitre_mappings
```

#### Architectural Impact

The AI Enrichment Service would be extended to include MITRE mapping. The KRI dashboard would add MITRE-based visualizations.

Possible enriched finding output:

```json
{
  "owasp_category": "A01: Broken Access Control",
  "mitre_tactic": "Initial Access",
  "mitre_technique_id": "T1190",
  "mitre_technique_name": "Exploit Public-Facing Application"
}
```

This feature should be implemented carefully as a defensive mapping and reporting feature, not as an exploitation guide.

---

### 9.4 Real-Time Scan Progress

The MVP can use polling to check scan status. A future extension is to add real-time scan progress updates.

#### Purpose

Real-time progress makes the application feel more interactive and professional. The user can see the scan move through different stages without manually refreshing the page.

#### Future Capabilities

Real-time updates may show:

1. Scan queued.
2. Scan running.
3. Scanner output received.
4. Findings stored.
5. AI enrichment started.
6. AI enrichment completed.
7. Risk scoring started.
8. KRI dashboard updated.
9. Scan completed or failed.

#### Possible Technologies

Real-time updates could use:

1. WebSockets.
2. Server-Sent Events.
3. Redis Pub/Sub.
4. FastAPI WebSocket support.

#### Architectural Impact

The Background Worker would publish status updates as the scan progresses. The backend would send these updates to the frontend in real time.

Possible flow:

```text
Background Worker
→ Redis Pub/Sub
→ Backend WebSocket endpoint
→ Frontend scan status component
```

This should be added after the MVP because polling is simpler and good enough for the first version.

---

### 9.5 Authentication and Role-Based Access Control

The MVP may run locally without authentication. A future extension is to add authentication and role-based access control.

#### Purpose

Authentication and authorization make Arx AI feel more like an enterprise platform. Different users may need different permissions.

#### Future Roles

Possible roles include:

1. Security Analyst.
2. Security Manager.
3. Developer.
4. Admin.

#### Example Permissions

```text
Security Analyst:
- Start scans
- View findings
- View KRI dashboard
- Generate reports

Security Manager:
- View dashboard
- View reports
- Review vendor risk

Developer:
- View assigned findings
- View remediation guidance

Admin:
- Manage approved targets
- Manage users
- Manage system settings
```

#### Possible Technologies

Authentication could use:

1. JWT authentication in FastAPI.
2. Auth.js / NextAuth for frontend authentication.
3. OAuth as an advanced option.
4. PostgreSQL users and roles tables.

#### Architectural Impact

The backend would add authentication middleware and permission checks. The database would include users, roles, and possibly user activity logs.

Possible database additions:

```text
users
roles
user_roles
permissions
```

This should be a stretch feature because authentication can add significant complexity.

---

### 9.6 CI/CD Pipeline

The MVP can be built locally, but a future extension is to add a CI/CD pipeline.

#### Purpose

CI/CD demonstrates professional software engineering workflow. It shows that the project is not just a local prototype, but a maintainable application with automated checks.

#### Future Capabilities

A CI/CD pipeline may include:

1. Backend linting.
2. Backend tests.
3. Frontend linting.
4. TypeScript type checking.
5. Frontend build verification.
6. Docker image build.
7. Database migration checks.
8. Deployment steps.

#### Possible Technology

The recommended tool is:

```text
GitHub Actions
```

#### Architectural Impact

The repository would include workflow files such as:

```text
.github/workflows/backend.yml
.github/workflows/frontend.yml
.github/workflows/docker.yml
```

This makes the project stronger for portfolio and recruiter review.

---

### 9.7 Cloud Deployment

The MVP can run locally with Docker Compose. A future extension is to deploy parts of Arx AI to the cloud.

#### Purpose

Cloud deployment demonstrates production awareness and makes the project easier to demo publicly.

#### Recommended Deployment Strategy

A safe deployment strategy would be:

```text
Frontend:
Vercel

Backend API:
Render, Fly.io, Railway, or AWS

Database:
Supabase, Neon, Railway PostgreSQL, or AWS RDS

Sandbox Targets:
Keep local or private only
```

#### Important Safety Note

Intentionally vulnerable sandbox targets should not be publicly exposed unless strong controls are in place. For this project, the safer approach is to deploy the frontend/backend if desired, but keep vulnerable targets local or private.

#### Architectural Impact

The application would need:

1. Environment variable management.
2. Production database connection.
3. CORS configuration.
4. Secure API keys.
5. Deployment documentation.
6. Possibly separate local and production modes.

Cloud deployment should be added only after the local MVP works reliably.

---

### 9.8 Monitoring and Observability

Monitoring and observability can be added after the MVP to track system health and job behavior.

#### Purpose

Monitoring shows professional engineering maturity. It helps developers understand whether scans, AI enrichment, reports, and backend APIs are working correctly.

#### Future Capabilities

Monitoring may track:

1. Number of scans started.
2. Number of scans completed.
3. Number of scans failed.
4. Average scan duration.
5. AI enrichment success rate.
6. AI enrichment failure rate.
7. Report generation failures.
8. API request latency.
9. Background worker errors.
10. Database health.

#### Possible Technologies

Monitoring may use:

1. Prometheus.
2. Grafana.
3. Structured logs.
4. OpenTelemetry as an advanced option.

#### Architectural Impact

The backend and worker would expose metrics. Grafana dashboards would visualize system health.

Important distinction:

```text
Arx AI KRI Dashboard:
Shows cybersecurity risk metrics.

Grafana Dashboard:
Shows system health and application performance metrics.
```

Both dashboards serve different purposes.

---

### 9.9 Vector Database and RAG

The MVP AI enrichment can use direct model calls with structured prompts. A future extension is to add Retrieval-Augmented Generation using a vector database.

#### Purpose

RAG would allow the AI Enrichment Service to use trusted reference material when generating explanations and remediation guidance.

#### Future Knowledge Sources

The AI could retrieve from:

1. OWASP references.
2. Internal remediation guidance.
3. Secure coding guidelines.
4. Previous findings.
5. Project-specific security notes.
6. MITRE ATT&CK reference summaries.

#### Possible Technologies

A vector database could use:

1. ChromaDB.
2. Qdrant.
3. pgvector as a PostgreSQL extension.

#### Architectural Impact

A new Knowledge Base component would be added.

Possible flow:

```text
Raw finding
→ retrieve relevant security references
→ AI enrichment with context
→ validated structured output
→ enriched finding stored
```

This would make the AI output more grounded and consistent.

This should be a stretch feature because RAG adds extra complexity and is not required for the first MVP.

---

### 9.10 Additional Scanner Integrations

The MVP should use one safe scanner, such as OWASP ZAP baseline scan. A future extension is to support multiple scanner integrations.

#### Purpose

Multiple scanner integrations make Arx AI more realistic because enterprise security platforms often combine findings from different tools.

#### Possible Scanner Sources

Future scanner sources may include:

1. OWASP ZAP.
2. Semgrep for static analysis.
3. npm audit for JavaScript dependencies.
4. pip-audit for Python dependencies.
5. Trivy for container scanning.
6. Custom scanner modules for lab-only checks.

#### Architectural Impact

The Scanner Service would become a scanner orchestration layer with multiple adapters.

Possible interface:

```text
ScannerAdapter
- run_scan(target)
- normalize_output(raw_output)
- return findings
```

Each scanner would normalize output into the same internal finding format.

This supports better maintainability and future extensibility.

---

### 9.11 Advanced KRI Snapshots

For the MVP, KRI metrics can be calculated directly from the database whenever the dashboard loads. A future extension is to store KRI snapshots.

#### Purpose

KRI snapshots allow Arx AI to preserve historical risk posture at specific points in time.

This makes trend analysis more accurate and realistic.

#### Future Capabilities

KRI snapshots may store:

1. Date.
2. Total findings.
3. Critical findings.
4. Average risk score.
5. Highest-risk target.
6. Highest-risk vendor.
7. Top OWASP category.
8. Risk trend summary.
9. Open high-risk finding count.

#### Possible Database Addition

```text
kri_snapshots
```

#### Architectural Impact

The KRI Engine would periodically calculate and store risk metrics. The frontend could then query historical snapshots for time-series charts.

Possible endpoint:

```text
GET /kri/snapshots
```

This would be especially useful for monthly or quarterly risk reporting.

---

### 9.12 Notification System

A future extension is to notify users when important scan or risk events occur.

#### Purpose

Notifications improve user awareness and make Arx AI feel more like a real security operations platform.

#### Future Notification Events

Notifications may be triggered when:

1. A scan completes.
2. A scan fails.
3. A critical finding is discovered.
4. AI enrichment fails.
5. Risk score exceeds a threshold.
6. A report is generated.

#### Possible Notification Channels

The project may support:

1. In-app notifications.
2. Email notifications.
3. Slack webhook integration as an advanced option.

#### Architectural Impact

A Notification Service would be added. The Background Worker or KRI Engine could trigger notifications based on events.

Possible flow:

```text
Critical finding detected
→ KRI Engine evaluates threshold
→ Notification Service creates alert
→ User sees notification
```

This should be added only after the dashboard and scan workflow are stable.

---

### 9.13 Developer Remediation Workflow

A future extension is to add developer-focused remediation tracking.

#### Purpose

The MVP identifies and explains findings. A remediation workflow would allow findings to be tracked through a fix lifecycle.

#### Future Capabilities

Finding statuses may include:

```text
open
in_review
accepted_risk
fixed
false_positive
```

The user may be able to:

1. Assign findings to developers.
2. Add remediation notes.
3. Change finding status.
4. Track time to resolution.
5. Re-scan to verify fixes.
6. View open vs fixed findings.

#### Possible Database Additions

```text
finding_status_history
finding_assignments
remediation_notes
```

#### Architectural Impact

The backend would add endpoints for updating finding status. The frontend would add remediation workflow views.

This extension would make Arx AI feel more like a complete vulnerability management system.

---

### 9.14 Kubernetes and Terraform

Kubernetes and Terraform are advanced infrastructure extensions.

#### Purpose

These technologies can demonstrate cloud-native and infrastructure-as-code skills, but they should not be part of the first MVP.

#### Possible Future Use

Kubernetes could be used to run:

1. Backend API.
2. Background workers.
3. Redis.
4. Scanner services.
5. Internal sandbox targets in a private cluster.

Terraform could be used to define cloud infrastructure such as:

1. Compute services.
2. Databases.
3. Networking.
4. Secrets.
5. Deployment resources.

#### Architectural Impact

This would move Arx AI closer to a cloud-native architecture.

However, it adds significant complexity. It should only be attempted after the MVP, CI/CD, and basic deployment are stable.

---

### 9.15 Future Extension Priority Order

The future extensions should not all be attempted at once. The recommended order is:

```text
1. PDF executive reports
2. Vendor risk scoring
3. MITRE ATT&CK mapping
4. Real-time scan progress
5. CI/CD pipeline
6. Cloud deployment
7. Authentication and role-based access control
8. Monitoring and observability
9. Vector database and RAG
10. Additional scanner integrations
11. KRI snapshots
12. Notification system
13. Developer remediation workflow
14. Kubernetes and Terraform
```

This order prioritizes features that improve the demo and portfolio value first, while leaving complex infrastructure work for later.

---

### 9.16 MVP vs Future Architecture Summary

The MVP architecture focuses on the essential end-to-end workflow:

```text
Frontend Dashboard
→ Backend API
→ Redis Queue
→ Background Worker
→ Scanner Service
→ Sandbox Target
→ Raw Findings
→ AI Enrichment
→ Risk Scoring
→ KRI Dashboard
→ Basic Report
```

The future architecture may expand into:

```text
Authentication
Role-based access control
Real-time updates
PDF reporting
Vendor risk scoring
MITRE ATT&CK mapping
RAG knowledge base
Multiple scanner adapters
Cloud deployment
CI/CD
Monitoring
Notifications
Remediation workflows
Infrastructure as Code
```

The architecture is designed this way so Arx AI can begin as a manageable final-year project and later grow into a portfolio-quality security intelligence platform.

---

### 9.17 Future Architecture Extension Summary

The main future architecture extensions for Arx AI are:

1. PDF executive report generation.
2. Vendor risk scoring.
3. MITRE ATT&CK mapping.
4. Real-time scan progress.
5. Authentication and role-based access control.
6. CI/CD pipeline.
7. Cloud deployment.
8. Monitoring and observability.
9. Vector database and RAG.
10. Additional scanner integrations.
11. Advanced KRI snapshots.
12. Notification system.
13. Developer remediation workflow.
14. Kubernetes and Terraform.

These extensions are valuable, but they should only be added after the MVP workflow is complete, stable, and demo-ready.
