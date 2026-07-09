## **Arx AI — Requirements Document** 

## **1. Main User Workflow** 

Arx AI is designed for an Application Security Analyst or Security Engineer who needs to assess application security risk and communicate the results clearly. 

The main workflow begins when the user opens the Arx AI dashboard and views the current cyber risk summary. From there, the user navigates to the approved sandbox targets page, selects a sandboxed vulnerable application, and starts a vulnerability scan. 

Once the scan is started, Arx AI creates a scan job and runs the scan in the background. The system collects raw vulnerability findings, stores them in the database, and then passes them through an AI enrichment process. The AI enrichment process classifies each finding, explains the risk in plain language, suggests remediation steps, and maps the finding to relevant security categories such as OWASP. 

After enrichment, Arx AI calculates a business risk score for each finding and updates the KRI dashboard. The user can then review the highest-risk findings, filter results by severity, target, vendor, date, or risk score, and generate a summary report for technical or executive review. 

In summary, the main workflow is: 

1. User opens the Arx AI dashboard. 

2. User views the current cyber risk summary. 

3. User navigates to the approved sandbox targets page. 

4. User selects a sandboxed vulnerable application. 

5. User starts a vulnerability scan. 

6. Arx AI creates a scan job. 

7. The scanner runs in the background. 

8. Raw vulnerability findings are collected and stored. 

9. AI enrichment classifies and explains the findings. 

10. Arx AI calculates business risk scores. 

11. The KRI dashboard is updated. 

12. User reviews prioritized findings. 

13. User generates a scan or risk summary report. 

## **2. Functional Requirements** 

## **2.1 Dashboard Requirements** 

FR1: The system shall display a cyber risk summary when the user opens the dashboard. 

FR2: The dashboard shall show key metrics including total scans, total findings, critical findings, average risk score, and highest-risk target. 

FR3: The dashboard shall display cyber risk trends over time. 

1 

FR4: The dashboard shall display the distribution of findings by severity. 

FR5: The dashboard shall display the distribution of findings by vulnerability category. 

FR6: The dashboard shall allow the user to filter results by severity, date, target, vendor, and risk score. 

FR7: The dashboard shall highlight the highest-priority risks that require attention. 

## **2.2 Target Management Requirements** 

FR8: The system shall display a list of approved sandbox targets. 

FR9: Each target shall include a name, URL, environment label, vendor label, application type, and current status. 

FR10: The system shall show whether each sandbox target is online or offline. 

FR11: The system shall only allow scans against preconfigured sandbox targets. 

FR12: The system shall prevent users from scanning arbitrary public URLs. 

FR13: The system shall clearly identify that all targets are sandboxed and intentionally vulnerable for educational and testing purposes. 

## **2.3 Scan Management Requirements** 

FR14: The user shall be able to start a vulnerability scan against an approved sandbox target. 

FR15: The system shall create a scan job whenever a scan is started. 

FR16: Each scan job shall include a unique ID, selected target, scan type, status, start time, completion time, and created-by information. 

FR17: The system shall track scan status using states such as queued, running, completed, and failed. 

FR18: The scanner shall run in the background so the user interface remains responsive. 

FR19: The user shall be able to view scan history. 

FR20: The user shall be able to view the details of an individual scan. 

FR21: The system shall store scan results after the scan is completed. 

FR22: If a scan fails, the system shall store the failure status and display an understandable error message. 

2 

## **2.4 Finding Storage Requirements** 

FR23: The system shall store raw vulnerability findings generated from each scan. 

FR24: Each finding shall be linked to a scan job and sandbox target. 

FR25: Each finding shall include vulnerability type, affected endpoint, evidence summary, severity, confidence level, and timestamp. 

FR26: The user shall be able to view all findings in a searchable and filterable table. 

FR27: The user shall be able to sort findings by severity, risk score, date, vulnerability type, target, and vendor. 

FR28: The system shall preserve scan findings for historical risk analysis. 

## **2.5 AI Enrichment Requirements** 

FR29: The system shall use an AI enrichment process to analyze raw vulnerability findings. 

FR30: The AI enrichment process shall generate a plain-English explanation for each finding. 

FR31: The AI enrichment process shall suggest remediation guidance for each finding. 

FR32: The AI enrichment process shall map findings to relevant OWASP categories. 

FR33: The AI enrichment process shall estimate the business impact of each finding. 

FR34: The AI enrichment output shall be structured and validated before being stored. 

FR35: If AI enrichment fails, the system shall keep the raw finding and mark it as requiring manual review. 

FR36: The system shall allow the user to distinguish between raw scanner output and AI-enriched analysis. 

## **2.6 Risk Scoring and KRI Requirements** 

FR37: The system shall calculate a business risk score for each vulnerability finding. 

FR38: The risk score shall consider severity, exploitability, asset criticality, confidence, and vendor exposure. 

FR39: The system shall rank findings from highest risk to lowest risk. 

FR40: The system shall calculate Key Risk Indicators, including critical findings, average risk score, highest-risk target, highest-risk vendor, and most common vulnerability category. 

3 

FR41: The system shall display KRI trends by month and year. 

FR42: The system shall allow the user to compare risk across targets, vendors, and time periods. 

FR43: The system shall update dashboard metrics when new scan results are processed. 

## **2.7 Reporting Requirements** 

FR44: The user shall be able to generate a scan summary report. 

FR45: The report shall include scan details, top findings, severity levels, risk scores, AI explanations, and remediation recommendations. 

FR46: The report shall include an executive summary written in non-technical language. 

FR47: The report shall identify the highest-priority findings that should be addressed first. 

FR48: The system shall support PDF report generation as a stretch feature. 

## **3. Non-Functional Requirements** 

## **3.1 Security Requirements** 

NFR1: The system shall only allow scans against approved sandbox targets. 

NFR2: The system shall not allow scanning of real public websites. 

NFR3: The system shall not perform destructive actions against any target. 

NFR4: The system shall store sensitive configuration values, such as API keys, using environment variables. 

NFR5: The system shall avoid storing real credentials, real company data, or sensitive personal information. 

NFR6: The system shall include clear ethical-use limitations in the documentation. 

NFR7: The system shall maintain audit logs for important actions such as scan creation and report generation. 

## **3.2 Reliability Requirements** 

NFR8: A failed scan shall not crash the entire system. 

NFR9: A failed AI enrichment process shall not delete or corrupt raw findings. 

4 

NFR10: The system shall preserve scan history and findings after processing. 

NFR11: The system shall handle missing or incomplete scanner output gracefully. 

NFR12: The system shall display clear error messages when something fails. 

## **3.3 Performance Requirements** 

NFR13: The dashboard shall load summary KRI data within a reasonable time for demo-sized datasets. 

NFR14: Scan jobs shall run asynchronously so that the user interface remains usable. 

NFR15: Filtering and sorting findings shall remain responsive for the expected project dataset size. 

NFR16: The system shall avoid blocking frontend interactions while scans or AI enrichment tasks are running. 

## **3.4 Usability Requirements** 

NFR17: The dashboard shall clearly separate technical vulnerability details from business risk metrics. 

NFR18: The user shall be able to identify the highest-priority risks without reading raw scanner output. 

NFR19: The user interface shall use clear labels, readable tables, and understandable risk indicators. 

NFR20: The system shall provide enough explanation for non-technical stakeholders to understand the business impact of findings. 

## **3.5 Maintainability Requirements** 

NFR21: The backend shall be organized into clear modules such as targets, scans, findings, AI enrichment, KRI calculations, and reporting. 

NFR22: The frontend shall be organized into reusable components. 

NFR23: The project shall include documentation for setup, architecture, usage, and ethical limitations. 

NFR24: The codebase shall follow consistent naming, formatting, and project structure. 

NFR25: The system shall be designed so that additional sandbox targets or scanners can be added later. 

## **4. MVP Requirements** 

The MVP version of Arx AI shall include the minimum set of features needed to prove the main idea. 

5 

The MVP shall allow a user to run a scan on a sandboxed vulnerable web application, collect vulnerability findings, enrich each finding using AI, assign a business risk score, and display the results in a KRI dashboard. 

The MVP includes: 

1. A working frontend dashboard. 

2. A FastAPI backend. 

3. A PostgreSQL database. 

4. Approved sandbox target management. 

5. Ability to start a scan against a sandbox target. 

6. Scan job creation and status tracking. 

7. Storage of raw vulnerability findings. 

8. AI enrichment of findings. 

9. Risk scoring for findings. 

10. KRI dashboard showing summary metrics. 

11. Findings table with filtering and sorting. 

12. Basic scan summary report. 

The MVP is considered successful if a user can complete the following flow: 

1. Open Arx AI. 

2. View the dashboard. 

3. Select an approved sandbox target. 4. Start a scan. 5. View stored findings. 

6. See AI-generated explanations and remediation guidance. 

7. View calculated risk scores. 

8. Review updated KRI metrics. 

9. Generate a basic report. 

## **5. Stretch Requirements** 

The stretch features are advanced features that will be implemented after the MVP is working. 

Stretch features include: 

1. PDF executive report generation. 

2. Vendor risk scoring. 

3. MITRE ATT&CK mapping. 

4. Real-time scan progress updates. 

5. CI/CD pipeline. 

6. Cloud deployment. 

7. Authentication and role-based access control. 

8. Monitoring with Prometheus and Grafana. 

9. More advanced dashboard filtering by month, year, vendor, target, and vulnerability category. 

10. Architecture and system design documentation suitable for a technical portfolio. 

These features are not required for the first working version, but they will make the final project more professional, impressive, and industry-relevant. 

6 

## **6. Out-of-Scope** 

The following items are outside the scope of Arx AI: 

1. The platform will not scan real public websites. 

2. The platform will not attack or exploit real systems. 

3. The platform will not perform destructive actions. 

4. The platform will not store real company data, real credentials, or private user data. 

5. The platform will not attempt to replace professional enterprise security tools. 

6. The platform will not provide unrestricted offensive security automation. 

7. The platform will not allow users to enter arbitrary external targets for scanning. 

8. The platform will not be used against systems without explicit authorization. 

All scanning activity will be limited to sandboxed, intentionally vulnerable applications created for educational and testing purposes. 

7 

