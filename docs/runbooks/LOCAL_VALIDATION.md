# Local Validation Runbook

This runbook explains how to validate the HAaaS repository locally before pushing changes.

## Purpose

The validation flow checks that the repository contains the current documentation, evidence and CI baseline for the HAaaS architecture proof-of-concept.

It does not deploy Home Assistant and does not prove production readiness.

## Prerequisites

- Git Bash, Linux shell or macOS terminal
- Repository cloned locally
- No secrets committed to the repository

## Commands

```bash
git pull
bash scripts/validate-repo.sh
cat docs/evidence/VALIDATION_REPORT.md
git status
```

## Expected result

The validation script should return either:

```text
PASSED: validation report generated: docs/evidence/VALIDATION_REPORT.md
```

or:

```text
PASSED_WITH_WARNINGS: validation report generated: docs/evidence/VALIDATION_REPORT.md
```

Warnings are acceptable for explicitly documented non-production or planned components. Failures should be fixed before merging.

## Generated files

The generated live report is:

```text
docs/evidence/VALIDATION_REPORT.md
```

This report is ignored by Git. A stable example report is kept at:

```text
docs/evidence/VALIDATION_REPORT_EXAMPLE.md
```

## Troubleshooting

If the validation fails, check:

- missing documentation files
- missing `.env.example`
- missing CI workflow
- accidental root `requirements.txt` used as a documentation placeholder
- strong README claims such as production readiness without implementation evidence
