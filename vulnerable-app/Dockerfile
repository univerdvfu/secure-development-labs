FROM python:3.11-slim
LABEL org.opencontainers.image.title="Secure Dev Labs vulnerable training app" \
      org.opencontainers.image.description="Intentionally vulnerable training application. Local labs only, not for production." \
      org.opencontainers.image.source="https://github.com/univerdvfu/secure-development-labs"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY frontend ./frontend
ENV PYTHONPATH=/app
EXPOSE 5000
HEALTHCHECK --interval=5s --timeout=3s --retries=20 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"]
CMD ["python", "-m", "backend.app"]
