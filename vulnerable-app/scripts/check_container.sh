#!/usr/bin/env bash
set -euo pipefail
export MSYS_NO_PATHCONV=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
IMAGE="${IMAGE:-secure-dev-labs-check:latest}"
mkdir -p reports

printf '\n[1/6] Docker Compose config\n'
docker compose config --quiet
docker compose config > reports/compose-rendered.yaml

printf '\n[2/6] Hadolint\n'
docker run --rm -v "${PWD}:/work:ro" -w /work hadolint/hadolint hadolint Dockerfile | tee reports/hadolint.txt

printf '\n[3/6] Trivy config\n'
docker run --rm -v "${PWD}:/src" -v secure-dev-labs-trivy-cache:/root/.cache/trivy aquasec/trivy:0.76.2 config --exit-code 0 --severity HIGH,CRITICAL --format table --output /src/reports/trivy-config.txt /src
cat reports/trivy-config.txt

printf '\n[4/6] Image build\n'
docker build -t "$IMAGE" .

printf '\n[5/6] Trivy image\n'
docker run --rm -v "${PWD}:/src" -v secure-dev-labs-trivy-cache:/root/.cache/trivy -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:0.76.2 image --exit-code 0 --severity HIGH,CRITICAL --format table --output "/src/reports/trivy-image.txt" "$IMAGE"

printf '\n[6/6] Compose health checks\n'
cleanup() {
  docker compose down -v >/dev/null 2>&1 || true
}
trap cleanup EXIT
docker compose up -d --build
for attempt in $(seq 1 45); do
  container_id="$(docker compose ps -q web)"
  status="$(docker inspect "$container_id" --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}')"
  if [ "$status" = "healthy" ]; then
    break
  fi
  if [ "$attempt" = "45" ]; then
    docker compose ps
    docker compose logs --tail 80
    exit 1
  fi
  sleep 2
done
curl --fail --silent --show-error --output reports/health.json http://127.0.0.1:5000/health
python -m json.tool reports/health.json
curl --fail --silent --show-error --output reports/login.html http://127.0.0.1:5000/login
curl --fail --silent --show-error --output reports/comments.html http://127.0.0.1:5000/comments
printf '\nAll container checks completed.\n'
cleanup
trap - EXIT
