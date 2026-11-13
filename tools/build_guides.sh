#!/usr/bin/env bash
# Пересборка DOCX-версий методичек из labs/*.md. Требуется pandoc.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p methodical

build() {
  pandoc "labs/$1" --from gfm --to docx --reference-doc tools/reference.docx --output "methodical/$2.docx"
  echo "methodical/$2.docx"
}

build lab1-secure-sdlc.md            "ЛР1_Знакомство_с_целью"
build lab2-sast-semgrep.md           "ЛР2_SAST_Semgrep"
build lab3-secrets-gitleaks.md       "ЛР3_Gitleaks_и_pre-commit"
build lab4-sca-trivy-containers.md   "ЛР4_SCA_Trivy_SBOM_и_контейнер"
build lab5-dast-github-actions.md    "ЛР5_DAST_и_GitHub_Actions"
build report-template.md             "Шаблон_отчёта"
