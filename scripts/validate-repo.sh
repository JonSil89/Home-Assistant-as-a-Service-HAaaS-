#!/bin/bash
set -euo pipefail

REPORT_FILE="docs/evidence/VALIDATION_REPORT.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

mkdir -p docs/evidence

report_line() {
  echo "${1:-}" >> "$REPORT_FILE"
}

record_result() {
  local status="$1"
  local component="$2"
  local details="$3"

  report_line "| $status | $component | $details |"
}

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  record_result "PASS" "$1" "$2"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  record_result "WARN" "$1" "$2"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  record_result "FAIL" "$1" "$2"
}

check_file() {
  if [ -f "$1" ]; then
    pass "$2" "$1 found"
  else
    fail "$2" "$1 missing"
  fi
}

check_dir() {
  if [ -d "$1" ]; then
    pass "$2" "$1 found"
  else
    fail "$2" "$1 missing"
  fi
}

{
  echo "# HAaaS Repository Validation Report"
  echo
  echo "| Field | Value |"
  echo "| --- | --- |"
  echo "| Generated | $TIMESTAMP |"
  echo "| Scope | Documentation and repository hygiene validation |"
  echo "| Production readiness claim | No |"
  echo
  echo "## Results"
  echo
  echo "| Status | Component | Details |"
  echo "| --- | --- | --- |"
} > "$REPORT_FILE"

check_file "README.MD" "Root README"
check_file ".env.example" "Environment template"
check_file ".gitignore" "Git ignore rules"
check_file ".github/workflows/status.yml" "CI workflow"
check_file "docs/README.md" "Docs overview"
check_file "docs/deployment_azure.md" "Azure deployment concept"
check_file "docs/database_schema.md" "Data model documentation"
check_file "docs/development_guide.md" "Development guide"
check_file "docs/dlcm_lifecycle.md" "Lifecycle model"
check_file "docs/roadmap_llm.md" "LLM roadmap"
check_file "docs/roadmap_pinecone.md" "RAG roadmap"
check_file "docs/requirements.md" "Requirements documentation"
check_file "docs/evidence/VALIDATION_REPORT_EXAMPLE.md" "Validation evidence example"
check_file "docs/runbooks/LOCAL_VALIDATION.md" "Local validation runbook"

check_dir "docs" "Documentation directory"
check_dir "docs/evidence" "Evidence directory"
check_dir "docs/runbooks" "Runbook directory"
check_dir "scripts" "Script directory"

if [ -f "requirements.txt" ]; then
  warn "Python dependency hygiene" "requirements.txt exists; use only for pip dependencies"
else
  pass "Python dependency hygiene" "No root requirements.txt placeholder present"
fi

if grep -qi "production-ready\|GDPR-ready\|Scale-Up" README.MD; then
  warn "README claims" "README may contain strong readiness wording; review manually"
else
  pass "README claims" "No obvious production-readiness overclaim found"
fi

report_line
report_line "## Summary"
report_line
report_line "| Metric | Count |"
report_line "| --- | ---: |"
report_line "| PASS | $PASS_COUNT |"
report_line "| WARN | $WARN_COUNT |"
report_line "| FAIL | $FAIL_COUNT |"

if [ "$FAIL_COUNT" -gt 0 ]; then
  report_line
  report_line "**FINAL STATUS:** FAILED"
  echo "FAILED: validation report generated with failed checks: $REPORT_FILE"
  exit 1
fi

if [ "$WARN_COUNT" -gt 0 ]; then
  report_line
  report_line "**FINAL STATUS:** PASSED_WITH_WARNINGS"
  echo "PASSED_WITH_WARNINGS: validation report generated: $REPORT_FILE"
  exit 0
fi

report_line
report_line "**FINAL STATUS:** PASSED"
echo "PASSED: validation report generated: $REPORT_FILE"
