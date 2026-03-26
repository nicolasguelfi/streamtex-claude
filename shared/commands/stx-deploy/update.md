# /stx-deploy:update — Update deployed projects

Arguments: $ARGUMENTS

## Argument parsing

Parse `$ARGUMENTS` as: `[OPTIONS]`

**Options**:
- `--project NAME` — Update a specific project
- `--all` — Update all deployed projects
- `--quick` — Quick restart (reuse existing Docker image, no rebuild)
- `--force` — Force rebuild even if no changes detected

By default (without `--quick`), update triggers a **full rebuild** from git + PyPI.
Use `--quick` only for env var or config changes that don't require a new Docker image.

### Examples

```
/stx-deploy:update --project cours-python          # full rebuild (default)
/stx-deploy:update --all                            # rebuild all
/stx-deploy:update --project cours-python --quick   # restart only (same image)
/stx-deploy:update --all --force                    # force rebuild all
```

## Required readings BEFORE execution

1. `.claude/developer/agents/deploy-operator.md` — deployment protocol

## Workflow

### Step 1: Adopt the Deploy Operator role

Read and adopt `.claude/developer/agents/deploy-operator.md`.

### Step 2: Load state

Read `.stx-deploy.json` to get the list of deployed projects.

If no projects deployed:
```
No projects deployed yet. Deploy with: /stx-deploy:deploy [path]
```

### Step 3: Select projects to update

If `--project NAME`: find the matching project in `.stx-deploy.json`.
If `--all`: select all projects.
If neither: ask the user which project(s) to update.

### Step 4: Trigger redeploy

For each selected project, trigger a redeploy via Coolify.

Read credentials from `.stx-deploy.env` (COOLIFY_URL, COOLIFY_API_TOKEN).
If `.stx-deploy.env` does not exist, read from `.stx-deploy.json` infrastructure section.

**CRITICAL**: Use `/start` for full rebuild (default) and `/restart` for quick restart only.
- `/start` = pull latest git, rebuild Docker image, install latest PyPI packages
- `/restart` = reuse existing container image (NO code update, NO PyPI update)

**Option A — Via Coolify API** (if API token available):

For **full rebuild** (default):
```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/$APP_UUID/start" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json"
```

For **quick restart** (`--quick` flag):
```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/$APP_UUID/restart" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json"
```

**Option B — Via Coolify UI** (guide the user):
```
In Coolify dashboard:
1. Projects → $PROJECT_NAME → Deploy (for rebuild)
   or Projects → $PROJECT_NAME → Restart (for quick restart)
```

**Option C — Via git push** (if auto-deploy is enabled):
```
The project has auto-deploy enabled.
Push a change to trigger a rebuild:
  cd $PROJECT_PATH
  git commit --allow-empty -m "Trigger rebuild"
  git push origin main
```

### Step 5: Monitor deployment

For each project being updated:
1. Wait for build to start
2. Monitor health check endpoint
3. Report when the new version is live

```bash
# Poll health check
curl -s "https://$SUBDOMAIN/_stcore/health"
```

### Step 6: Display result

```
Update Complete:
  #  Project          Status    Duration
  1  cours-python     updated   45s
  2  cours-docker     updated   38s

All health checks passing.
```
