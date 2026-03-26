# /stx-deploy:go — Deploy from zero to live in one command

Arguments: $ARGUMENTS

## Purpose

Single command that orchestrates the full deployment pipeline. Detects the
current state and executes only the missing phases. A new user with nothing
gets a full setup; a user with existing infrastructure gets a direct deploy.

## Argument parsing

Parse `$ARGUMENTS` as: `[PROJECT_PATH] [OPTIONS]`

- `PROJECT_PATH` — Path to the StreamTeX project (default: current directory)
- `--subdomain NAME` — Override the subdomain (default: project directory name)

### Examples

```
/stx-deploy:go                          # deploy current project
/stx-deploy:go ./projects/my-course     # deploy specific project
/stx-deploy:go --subdomain my-course    # custom subdomain
```

## Required readings BEFORE execution

1. `.claude/developer/agents/deploy-operator.md` — deployment protocol
2. `.stx-deploy.env` — credentials (may not exist yet)
3. `.stx-deploy.json` — infrastructure state (may not exist yet)

## Workflow

### Step 1: Adopt the Deploy Operator role

Read and adopt `.claude/developer/agents/deploy-operator.md`.

### Step 2: Detect current state

Read `.stx-deploy.env` and `.stx-deploy.json`. Determine which phases are needed:

| Check | Phase needed if missing |
|-------|----------------------|
| `.stx-deploy.env` exists? | setup |
| `HETZNER_API_TOKEN` set? | setup |
| Server in `.stx-deploy.json`? | provision |
| `phases_completed.provision` set? | provision |
| `phases_completed.secure` set? | secure |
| `COOLIFY_API_TOKEN` set? | install-coolify |
| Domain configured? | configure-domain |
| Project already deployed? | deploy (otherwise: update) |

### Step 3: Execute missing phases

For each missing phase, execute it in order. Use the exact same logic as the
individual `/stx-deploy:*` commands but with these simplifications:

1. **Confirmation gates only for costly operations**:
   - Server creation (~8.49 EUR/month) → ask confirmation
   - Domain DNS changes → ask confirmation
   - All other steps → proceed automatically

2. **Progress display**:
   ```
   StreamTeX Deploy — Full Pipeline
   ================================

   Phase 1/6 — Setup .................. ✓ (already done)
   Phase 2/6 — Provision .............. ✓ (already done)
   Phase 3/6 — Secure ................ ✓ (already done)
   Phase 4/6 — Install Coolify ....... ✓ (already done)
   Phase 5/6 — Configure Domain ...... ✓ (already done)
   Phase 6/6 — Deploy Project ........ ⏳
     → Preflight checks .............. ✓
     → Creating Coolify app .......... ✓
     → Triggering build .............. ✓
     → Waiting for healthy ........... ✓ (2m15s)

   ✓ Your document is live at: https://my-course.mysite.org
   ```

3. **Skip already-completed phases**: Read `.stx-deploy.json` `phases_completed`
   timestamps. If a phase was already done, show "already done" and skip.

### Step 4: Phase execution details

**If setup needed** → Execute `/stx-deploy:setup` workflow (Steps 3-8).

**If provision needed** → Execute `/stx-deploy:provision` workflow.
Ask: "This will create a Hetzner server (cax21, ~8.49 EUR/month). Continue? [y/N]"

**If secure needed** → Execute `/stx-deploy:secure` workflow.
No confirmation needed (no cost).

**If install-coolify needed** → Execute `/stx-deploy:install-coolify` workflow.
Requires user interaction for browser onboarding + API token paste.

**If configure-domain needed** → Execute `/stx-deploy:configure-domain` workflow.
If Cloudflare token available, DNS is automatic. Otherwise guide manual setup.

**If deploy needed** → Execute `/stx-deploy:deploy` workflow for the project.
Auto-detect project name from directory. Use Coolify API for all operations.

**If already deployed** → Execute `/stx-deploy:update --project NAME` workflow.
Trigger a rebuild to update to latest code.

### Step 5: Post-deploy verification

After deployment:

1. Wait for `running:healthy` status (max 5 minutes)
2. HTTP GET the URL and verify it responds with 200
3. Check the page content contains StreamTeX markers

```bash
# Health check
curl -s -o /dev/null -w "%{http_code}" "https://$SUBDOMAIN.$DOMAIN/_stcore/health"

# Page check
curl -s "https://$SUBDOMAIN.$DOMAIN" | grep -q "streamtex"
```

### Step 6: Display final result

```
============================================================
  StreamTeX Deployment Complete
============================================================

  URL:      https://my-course.mysite.org
  Server:   138.199.x.x (cax21, Falkenstein)
  Coolify:  https://coolify.mysite.org
  Status:   running:healthy

  Management:
    /stx-deploy:update    — rebuild after code changes
    /stx-deploy:status    — check all services
    stx deploy status     — same via CLI (no Claude needed)
============================================================
```

### Step 7: Update state file

Update `.stx-deploy.json` with the new application entry.
