# Backup and Restore Runbook

This runbook describes a simple local backup and restore model for the HAaaS Docker Compose baseline.

## Purpose

The goal is to document how local Home Assistant configuration can be backed up and restored during development and architecture validation.

This is not a production backup model. Production environments require tested storage, retention, encryption, access control and restore procedures.

## Scope

| Item | Included |
| --- | --- |
| Local `config/` directory backup | Yes |
| Home Assistant local database backup | If present under `config/` |
| Cloud backup | No |
| Encrypted offsite backup | No |
| Production restore SLA | No |

## Backup

Stop the local stack before backup:

```bash
docker compose down
```

Create a backup directory:

```bash
mkdir -p backups
```

Create a timestamped archive:

```bash
tar -czf backups/homeassistant-config-$(date +%Y%m%d-%H%M%S).tar.gz config
```

Start the stack again:

```bash
docker compose up -d
```

## Restore

Stop the local stack:

```bash
docker compose down
```

Move the current config aside:

```bash
mv config config.restore-previous-$(date +%Y%m%d-%H%M%S)
```

Restore from a selected backup archive:

```bash
tar -xzf backups/homeassistant-config-YYYYMMDD-HHMMSS.tar.gz
```

Start the stack:

```bash
docker compose up -d
```

Check logs:

```bash
docker compose logs --tail=100 homeassistant
```

## Validation after restore

Open:

```text
http://localhost:8123
```

Then confirm:

- Home Assistant starts successfully.
- Expected local configuration is visible.
- No sensitive local runtime files were committed to Git.
- `git status` does not show generated runtime data.

## Evidence

After backup or restore testing, run repository validation:

```bash
bash scripts/validate-repo.sh
cat docs/evidence/VALIDATION_REPORT.md
```

## Production notes

A production-grade backup model would require at least:

- defined recovery point objective and recovery time objective
- encrypted backup storage
- offsite or cloud copy
- access-control model for backup operators
- periodic restore tests
- documented retention policy
- incident and rollback procedure
