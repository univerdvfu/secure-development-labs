# Практикум по безопасной разработке для начинающих специалистов ИБ

Пять лабораторных работ по ГОСТ Р 56939-2024 и ГОСТ Р 71207-2024 с готовым уязвимым веб-приложением. Опыт разработки не требуется: каждая методичка начинается с теории простыми словами, а затем показывает практику по шагам с командами, кодом, ожидаемым результатом и типичными ошибками.

> Приложение намеренно уязвимо. Работайте только на локальной учебной копии. Не сканируйте чужие системы и не используйте настоящие секреты.

## Как проходить практикум

1. Прочитайте раздел «Что вы изучите» и «Теория простыми словами».
2. Выполните подготовку из раздела «Перед началом».
3. Двигайтесь по практическим шагам сверху вниз. Не пропускайте проверку ожидаемого результата.
4. Сохраняйте команды и отчёты в `reports`.
5. Сдайте материалы из раздела «Что сдать в отчёте» и ответьте на вопросы.

Рекомендуемый порядок:

| Работа | Тема | PDF | Редактируемая версия |
|---|---|---|---|
| ЛР1 | Безопасный SDLC, архитектура, активы и угрозы | [PDF](methodical/pdf/ЛР1_Безопасный_SDLC_и_ГОСТ.pdf) | [DOCX](methodical/ЛР1_Безопасный_SDLC_и_ГОСТ.docx) |
| ЛР2 | SAST и исправление SQL injection/XSS через Semgrep | [PDF](methodical/pdf/ЛР2_SAST_Semgrep.pdf) | [DOCX](methodical/ЛР2_SAST_Semgrep.docx) |
| ЛР3 | Gitleaks, история Git и pre-commit | [PDF](methodical/pdf/ЛР3_Gitleaks_и_pre-commit.pdf) | [DOCX](methodical/ЛР3_Gitleaks_и_pre-commit.docx) |
| ЛР4 | Trivy, зависимости, CVE и SBOM | [PDF](methodical/pdf/ЛР4_SCA_Trivy_и_SBOM.pdf) | [DOCX](methodical/ЛР4_SCA_Trivy_и_SBOM.docx) |
| ЛР5 | OWASP ZAP, контроль доступа и CI/CD | [PDF](methodical/pdf/ЛР5_DAST_OWASP_ZAP_и_CI_CD.pdf) | [DOCX](methodical/ЛР5_DAST_OWASP_ZAP_и_CI_CD.docx) |

Каждая работа рассчитана на 2 академических часа и оценивается максимум в 100 баллов.

## Структура репозитория

```text
secure-dev-labs/
├── README.md
├── methodical/             # Пять методичек в DOCX и PDF
└── vulnerable-app/
    ├── backend/            # Flask, маршруты, конфигурация и работа с БД
    ├── frontend/           # HTML-шаблоны, CSS и JavaScript
    ├── legacy-component/   # Устаревший манифест только для SCA
    ├── tests/              # Проверки исходных учебных сценариев
    ├── compose.yaml        # Web + PostgreSQL
    ├── Dockerfile
    ├── .semgrep.yml        # Учебные правила SAST
    └── .pre-commit-config.yaml
```

## Что понадобится

- Python 3.11 или новее;
- Git;
- браузер и терминал;
- Docker Desktop для ZAP и альтернативного запуска сканеров;
- редактор, который показывает текстовые файлы и номера строк.

Команды в методичках показаны для Git Bash. Для Windows PowerShell активация окружения: `.venv\Scripts\Activate.ps1`.

## Быстрый запуск приложения

Откройте терминал в `vulnerable-app` и выполните:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m backend.app
```

Для Linux/macOS активация обычно выглядит как `source .venv/bin/activate`.

Откройте `http://127.0.0.1:5000`.

Учебные записи:

- `student / student123`;
- `admin / admin123`.

Проверка API и тестов:

```bash
curl http://127.0.0.1:5000/health
pytest -q
```

Ожидаемый результат тестов: `4 passed`. Эти тесты подтверждают исходные уязвимости. В ЛР2 и ЛР5 вы замените их на проверки безопасного поведения.

## Запуск с PostgreSQL

```bash
docker compose up --build
```

- приложение: порт `5000`;
- PostgreSQL: порт `5432`;
- БД использует `tmpfs`, поэтому данные удаляются после `docker compose down`.

Открытый порт БД и простые пароли намеренно оставлены для анализа конфигурации.

## Проверка Dockerfile, Compose и контейнера

Из каталога `vulnerable-app` запустите:

```bash
./scripts/check_container.sh
```

Скрипт выполняет шесть проверок:

1. `docker compose config` и сохранение итоговой конфигурации;
2. Hadolint для Dockerfile;
3. Trivy config для Dockerfile и Compose;
4. сборку образа;
5. Trivy image для собранного образа;
6. запуск Compose, ожидание healthy и HTTP-проверки `/health`, `/login`, `/comments`.

Отчёты сохраняются в `vulnerable-app/reports`. Учебные находки Hadolint/Trivy не блокируют baseline: root в Dockerfile намеренно оставлен для ЛР4. Workflow `.github/workflows/container-checks.yml` повторяет проверки в GitHub Actions и публикует отчёты как artifacts.

## Образ в GitHub Container Registry

Образ: `ghcr.io/univerdvfu/secure-dev-lab-app:latest`.

```bash
docker pull ghcr.io/univerdvfu/secure-dev-lab-app:latest
docker run --rm -p 5000:5000 ghcr.io/univerdvfu/secure-dev-lab-app:latest
```

Если пакет имеет ограниченный доступ, сначала выполните `docker login ghcr.io`. Образ содержит намеренно уязвимое приложение только для локальных лабораторных. Не используйте его в production и не открывайте порт внешним пользователям.

## Команды сканеров через Docker

Выполняйте из `vulnerable-app`:

```bash
# Semgrep
docker run --rm -v "${PWD}:/src" semgrep/semgrep:1.94.0 semgrep scan --config /src/.semgrep.yml --metrics=off /src

# Gitleaks по текущим файлам
docker run --rm -v "${PWD}:/src" ghcr.io/gitleaks/gitleaks:v8.24.2 dir --redact -v /src

# Trivy по файловой системе
docker run --rm -v "${PWD}:/src" aquasec/trivy:latest fs --scanners vuln,secret /src
```

Ненулевой код выхода Semgrep/Gitleaks при находках для исходного проекта ожидается. Это результат проверки, а не обязательно ошибка установки.

## Что должны найти студенты

- SQL injection в `/login` и `/search`;
- отражённый и хранимый XSS;
- IDOR в `/profile?id=`;
- пароли в открытом виде;
- отсутствие security-заголовков и anti-CSRF;
- включённый debug-режим;
- фиктивный токен в `backend/config.py`;
- уязвимые версии в `legacy-component/requirements.txt`;
- запуск контейнера от root и открытый порт PostgreSQL.

Не все дефекты обнаруживаются всеми инструментами. Это специально используется в заданиях для демонстрации ограничений сканеров.

## Контрольные ориентиры для преподавателя

- Semgrep с `.semgrep.yml`: 6 находок.
- Gitleaks: `generic-api-key` в `backend/config.py`; до исправления `pre-commit run --all-files` возвращает код 1.
- Trivy: находки в legacy-манифесте, секрет и DS-0002 в Dockerfile. Количество CVE зависит от даты базы.
- ZAP Baseline: заголовки, anti-CSRF и потенциальный XSS.
- ZAP active: SQL Injection, отражённый и хранимый XSS.
- IDOR и открытые пароли предназначены для ручного анализа.

`legacy-component/requirements.txt` не нужно устанавливать: он служит только учебным объектом SCA.
