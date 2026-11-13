"""Настройки учебного приложения. Секреты приходят из переменных окружения."""
import os

DEMO_GITHUB_TOKEN = os.getenv("DEMO_GITHUB_TOKEN", "")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")
DATABASE_PATH = "data/students.db"
