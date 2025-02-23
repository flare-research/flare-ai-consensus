# Stage 1: Build Backend
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS backend-builder
ADD . /flare-ai-consensus
WORKDIR /flare-ai-consensus
RUN uv sync --frozen

# Stage 2: Final Image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY --from=backend-builder /flare-ai-consensus/.venv ./.venv
COPY --from=backend-builder /flare-ai-consensus/src ./src
COPY --from=backend-builder /flare-ai-consensus/pyproject.toml .
COPY --from=backend-builder /flare-ai-consensus/README.md .

# Allow workload operator to override environment variables
LABEL "tee.launch_policy.allow_env_override"="OPEN_ROUTER_API_KEY"
LABEL "tee.launch_policy.log_redirect"="always"

EXPOSE 80

CMD ["uv", "run", "start-backend"]