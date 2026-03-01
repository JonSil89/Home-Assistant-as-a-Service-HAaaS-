# Case Study: Disaster Recovery & Version Control

*Tämä dokumentaatio toimii työnäytteenä hallitusta kriisinhallinnasta ja Git-ympäristön palauttamisesta.*

# Incident & Recovery Log

This document records significant environment failures, automation anomalies, and their respective recovery actions. Maintenance of this log is part of our **Operational Quality** and **Compliance** (ISO 27001 / MDR) framework.

---

## [INC-20251227-01] AI Agent Environment Corruption

**Date:** 2025-12-27  
**Severity:** High (Local Development Blocked)  
**Status:** Resolved  
**Lead:** Jonne Silvennoinen

### 1. Description
An autonomous AI agent corrupted the local development environment during an automated refactoring task. The corruption resulted in the deletion of core project files, including architectural documentation (`WARP.md`) and configuration templates. Additionally, the agent introduced invalid Windows-specific file paths that conflicted with the POSIX-aligned CI/CD environment.

### 2. Root Cause Analysis (RCA)
* **Trigger:** Automated file system write-operation by an AI agent.
* **Failure:** Lack of path-validation logic in the agent's execution script, leading to directory-tree collapse and OS-specific path conflicts.

### 3. Recovery Actions (The Rollback)
Instead of manual restoration, a **State-Based Recovery** was performed:
1.  **Identification:** Used `git reflog` and `git log` to identify the last known healthy state (`87e317d`).
2.  **Rollback:** Performed a controlled git rollback to restore project integrity.
3.  **Sanitization:** Manually stripped invalid Windows-specific metadata and paths to prevent recurrence in the Linux-based CI/CD runner.
4.  **Validation:** Pushed a cleanup commit (`a755499`) to trigger the **GitHub Actions CI Pipeline**.
5.  **Audit Trail:** Documented the recovery in the commit history to maintain a transparent audit trail.

### 4. Verification
* [x] **File Integrity:** All `docs/` and `WARP.md` files restored.
* [x] **Pipeline Status:** GitHub Actions CI build passed (Green).
* [x] **Environment:** Local dev environment synced with remote main branch.

### 5. Preventative Measures
* Updated `.gitignore` to be more restrictive with agent-generated temp files.
* Implemented stricter **Quality Gates** for local agent execution.
* Enforced a "Commit-First" policy before triggering high-autonomy AI tasks.

---
*Log maintained by JonSil89 — Infrastructure & Compliance*

---
### Severity rationale: 
Local development halted --> production and customer environments unaffected.

### Classification: 
Automation-induced configuration drift.
