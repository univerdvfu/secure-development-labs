# Практикум по безопасной разработке (DevSecOps)

Пять лабораторных работ с намеренно уязвимым веб-приложением. Студент на своём ноутбуке проходит путь от модели угроз до работающего конвейера безопасности в GitHub Actions: читает теорию, выполняет шаги методички, сверяется с ожидаемым результатом и оформляет отчёт.

Опыт разработки не требуется: все команды и фрагменты кода приведены в методичках.

> Приложение намеренно уязвимо. Работайте только с локальной копией на своём компьютере. Не сканируйте чужие системы и не используйте настоящие секреты.

## Лабораторные работы

| № | Тема | Инструменты | Время | Методичка | Для печати |
|---|---|---|---|---|---|
| 1 | Безопасный SDLC, модель угроз, требования | схема, STRIDE | 2 ч | [labs/lab1-secure-sdlc.md](labs/lab1-secure-sdlc.md) | [DOCX](methodical/ЛР1_Безопасный_SDLC_и_модель_угроз.docx) · [PDF](methodical/pdf/ЛР1_Безопасный_SDLC_и_модель_угроз.pdf) |
| 2 | Статический анализ, SQL-инъекции и XSS | Semgrep, pytest | 2 ч | [labs/lab2-sast-semgrep.md](labs/lab2-sast-semgrep.md) | [DOCX](methodical/ЛР2_SAST_Semgrep.docx) · [PDF](methodical/pdf/ЛР2_SAST_Semgrep.pdf) |
| 3 | Секреты в коде и истории Git | Gitleaks, pre-commit | 2 ч | [labs/lab3-secrets-gitleaks.md](labs/lab3-secrets-gitleaks.md) | [DOCX](methodical/ЛР3_Gitleaks_и_pre-commit.docx) · [PDF](methodical/pdf/ЛР3_Gitleaks_и_pre-commit.pdf) |
| 4 | Зависимости, SBOM, контейнер | Trivy, Docker | 2 ч | [labs/lab4-sca-trivy-containers.md](labs/lab4-sca-trivy-containers.md) | [DOCX](methodical/ЛР4_SCA_Trivy_SBOM_и_контейнер.docx) · [PDF](methodical/pdf/ЛР4_SCA_Trivy_SBOM_и_контейнер.pdf) |
| 5 | DAST и конвейер CI | OWASP ZAP, GitHub Actions | 4 ч | [labs/lab5-dast-github-actions.md](labs/lab5-dast-github-actions.md) | [DOCX](methodical/ЛР5_DAST_и_GitHub_Actions.docx) · [PDF](methodical/pdf/ЛР5_DAST_и_GitHub_Actions.pdf) |

Шаблон отчёта: [labs/report-template.md](labs/report-template.md) · [DOCX](methodical/Шаблон_отчёта.docx).

Каждая работа оценивается из 100 баллов; критерии приведены в конце методички.

Работы выполняются **строго по порядку**: каждая продолжает предыдущую в одном и том же репозитории студента.

```text
ЛР1  своя копия проекта + git init ─► модель угроз и требования
ЛР2  Semgrep: 6 находок ─► исправление SQLi/XSS ─► тесты ─► коммит
ЛР3  Gitleaks: секрет в коде и истории ─► pre-commit ─► коммит
ЛР4  Trivy: зависимости, SBOM, Dockerfile ─► исправления ─► коммит
ЛР5  ZAP + IDOR ─► публикация на GitHub ─► конвейер из 5 заданий ─► защита ветки
```

## Структура методички

1. Цель работы и ожидаемые результаты.
2. Теория простыми словами.
3. Ход работы по шагам: команда → ожидаемый результат → что делать при ошибке → что внести в отчёт.
4. Требования к отчёту.
5. Контрольные вопросы.
6. Критерии оценивания.
7. Источники.

## Что понадобится студенту

- Git;
- Python 3.11 или новее;
- Docker Desktop (Windows, macOS) или Docker Engine (Linux) — с ЛР3;
- редактор кода;
- учётная запись на github.com — для ЛР5.

Команды в методичках написаны для Bash. В Windows используется Git Bash; перед командами `docker run` в нём нужно выполнить `export MSYS_NO_PATHCONV=1` (об этом сказано в методичках).

## Быстрый запуск приложения

```bash
cd vulnerable-app
python -m venv .venv
source .venv/Scripts/activate     # Windows, Git Bash
# source .venv/bin/activate       # Linux и macOS
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m backend.app
```

Приложение: <http://127.0.0.1:5000>. Учётные записи: `student / student123`, `admin / admin123`.

```bash
pytest -q        # ожидается: 4 passed — тесты подтверждают исходные уязвимости
```

С PostgreSQL в контейнерах:

```bash
docker compose up -d --build --wait
```

## Структура репозитория

```text
secure-development-labs/
├── README.md
├── labs/                   # методички в Markdown — основной источник
│   ├── lab1-secure-sdlc.md
│   ├── lab2-sast-semgrep.md
│   ├── lab3-secrets-gitleaks.md
│   ├── lab4-sca-trivy-containers.md
│   ├── lab5-dast-github-actions.md
│   └── report-template.md
├── methodical/             # те же методички в DOCX и PDF
├── tools/build_guides.sh   # пересборка DOCX из Markdown
└── vulnerable-app/         # учебное приложение — его копирует студент
    ├── backend/            # Flask: маршруты, конфигурация, работа с БД
    ├── frontend/           # HTML-шаблоны, CSS, JavaScript
    ├── legacy-component/   # устаревший манифест — объект для SCA, не устанавливать
    ├── tests/              # тесты исходных учебных сценариев
    ├── compose.yaml        # web + PostgreSQL
    ├── Dockerfile
    ├── .semgrep.yml        # учебные правила SAST
    └── .pre-commit-config.yaml
```

Методички правятся в `labs/*.md`. После правки DOCX пересобирается командой `bash tools/build_guides.sh` (нужен pandoc); PDF получают из DOCX через «Сохранить как» в Word или LibreOffice.

## Заложенные уязвимости

| Дефект | Где | Чем обнаруживается | В какой работе устраняется |
|---|---|---|---|
| SQL-инъекция | `/login`, `/search` | Semgrep, вручную | ЛР2 |
| Отражённый и хранимый XSS | `search.html`, `comments.html` | Semgrep, вручную | ЛР2 |
| Отладочный режим Flask | `backend/app.py` | Semgrep | ЛР2 |
| Токен в коде и в истории Git | `backend/config.py` | Gitleaks, Semgrep | ЛР3 |
| Уязвимые версии библиотек | `legacy-component/`, `requirements.txt` | Trivy | ЛР4 |
| Контейнер работает от root | `Dockerfile` | Trivy config (DS-0002) | ЛР4 |
| Открытый порт PostgreSQL | `compose.yaml` | только вручную | ЛР4 |
| IDOR: чужой профиль без входа | `/profile?id=` | только вручную | ЛР5 |
| Нет заголовков безопасности | все ответы | OWASP ZAP | ЛР5 |
| Нет защиты от CSRF | формы | OWASP ZAP | остаточный риск |
| Пароли в открытом виде | таблица `users` | только вручную | остаточный риск, доп. задание |
| Ключ сессии по умолчанию | `backend/config.py` | только вручную | остаточный риск |

Часть дефектов намеренно не находит ни один сканер — на этом построены задания об ограничениях инструментов.

## Контрольные результаты для преподавателя

Получены при полном прохождении всех шагов на Ubuntu 24.04 (Python 3.12, Docker 29) в ноябре 2026 года. Версии инструментов закреплены: Semgrep 1.185.0, Gitleaks 8.24.2, Trivy 0.76.2; ZAP — образ `stable`.

| Работа | Проверка | Исходное состояние | После выполнения |
|---|---|---|---|
| ЛР1 | `pytest -q` | 4 passed | — |
| ЛР2 | Semgrep | 6 находок | 1 (токен, уходит в ЛР3) |
| ЛР2 | `pytest -q` | после правок кода: 2 failed, 2 passed | 7 passed |
| ЛР3 | `gitleaks dir` | 1 (`generic-api-key`, `config.py:3`) | 0 |
| ЛР3 | `gitleaks git` | 1 | 1 до `.gitleaksignore`, затем 0 |
| ЛР3 | Semgrep | 1 | 0 |
| ЛР4 | `trivy fs` | 44 в `legacy-component`, 1 в `requirements.txt` | 0 HIGH/CRITICAL, код 0 |
| ЛР4 | `trivy config` | DS-0002 (HIGH) | 0 |
| ЛР4 | SBOM CycloneDX | 9 компонентов | 4 |
| ЛР4 | `id` в контейнере | `uid=0(root)` | `uid=1000(labuser)` |
| ЛР4 | `trivy image` | 49 HIGH в Debian (исправление есть у 2) | не устраняется, разбор |
| ЛР5 | ZAP baseline | 10 WARN | 6 WARN |
| ЛР5 | `/profile?id=1` без входа | 200 | 401 |
| ЛР5 | `pytest -q` | 7 passed | 11 passed |
| ЛР5 | конвейер | — | 5 заданий; PR с `\|safe` — красные `tests` и `sast`, `dast` пропущен |

Число CVE в отчётах Trivy со временем растёт — это ожидаемо и обсуждается в ЛР4. Если после выхода новой CVE шаг с порогом `--exit-code 1` перестанет проходить, обновите версию библиотеки в методичке ЛР4 (сейчас `Flask==3.1.3`).

Признаки самостоятельной работы: у каждого студента свои идентификаторы коммитов, свой отпечаток в `.gitleaksignore`, своя ссылка на репозиторий и свои запуски на вкладке Actions.

## Автоматическая проверка самого практикума

Workflow `.github/workflows/container-checks.yml` проверяет учебное приложение в исходном, уязвимом виде (сборка образа, Compose, Trivy) и публикует образ `ghcr.io/univerdvfu/secure-dev-lab-app`. Это служебный конвейер репозитория курса. Студенты копируют себе только каталог `vulnerable-app`, поэтому он к ним не попадает: свой конвейер они пишут в ЛР5 с нуля.
