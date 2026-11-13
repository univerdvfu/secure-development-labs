#!/usr/bin/env bash
# Пересборка DOCX-версий методичек из labs/*.md. Требуется pandoc.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p methodical

build() {
  pandoc "labs/$1" --from gfm --to docx --resource-path labs \
    --reference-doc tools/reference.docx --output "methodical/$2.docx"
  echo "methodical/$2.docx"
}

build lab1-secure-sdlc.md            "ЛР1_Введение_и_модель_угроз"
build lab2-sast-semgrep.md           "ЛР2_SAST_Semgrep"
build lab3-secrets-gitleaks.md       "ЛР3_Секреты_и_зависимости"
build lab4-sca-trivy-containers.md   "ЛР4_Контейнер_и_DAST"
build lab5-dast-github-actions.md    "ЛР5_GitHub_Actions"
build report-template.md             "Шаблон_отчёта"
