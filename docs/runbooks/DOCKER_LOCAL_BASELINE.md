# Docker Local Baseline Runbook

This runbook describes the local Home Assistant baseline for the HAaaS architecture proof-of-concept.

## Purpose

The Docker Compose baseline gives the repository a runnable local starting point. It is intended for architecture validation, documentation and local experimentation.

It is not a production deployment model.

## Services

| Service | Purpose |
| --- | --- |
| `homeassistant` | Local Home Assistant Core instance |

The service is bound to localhost only:

```text
127.0.0.1:8123:8123
```

This reduces accidental exposure outside the local machine during development.

## Start

```bash
docker compose up -d
```

Open:

```text
http://localhost:8123
```

## Check status

```bash
docker compose ps
docker compose logs --tail=100 homeassistant
```

## Stop

```bash
docker compose down
```

## Reset local configuration

The local Home Assistant configuration is stored under:

```text
config/
```

To reset the local instance, stop the stack and remove the local config directory manually.

```bash
docker compose down
rm -rf config
```

Use reset carefully. Local configuration and test data will be removed.

## Security notes

- Do not commit real Home Assistant configuration containing tokens, URLs, user data or device identifiers.
- Keep local runtime data out of Git.
- Use `.env.example` for public-safe placeholders only.
- Treat any future remote access model, tunnel or cloud hosting separately from this local baseline.

## Validation

Run repository validation after changes:

```bash
bash scripts/validate-repo.sh
cat docs/evidence/VALIDATION_REPORT.md
```
