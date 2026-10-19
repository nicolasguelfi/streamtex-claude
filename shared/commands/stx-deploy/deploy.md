# /stx-deploy:deploy — Deploy a StreamTeX project to Hetzner

Arguments: $ARGUMENTS

This command drives the `stx deploy` CLI. It never writes a Dockerfile,
an entrypoint or `.stx-deploy.json` by hand: the CLI generates and owns them.

## Argument parsing

Parse `$ARGUMENTS` as: `[PATH] [OPTIONS]`, the options of `stx deploy hetzner`:

- **PATH**: Path to the StreamTeX project (default: current directory)
- `--subdomain NAME` — Subdomain of the service (asked when omitted; default proposal: the project directory name)
- `--uuid UUID` — An existing Coolify application (skips creation)
- `--serve-mode MODE` — `dual` (default: Nginx serves the HTML export on `/html/` and proxies Streamlit on `/`), `static-only` (Nginx, HTML export only), `streamlit-only` (no Nginx)
- `--yes` — Skip the confirmation prompts
- `--help` — Show this guide

Anything else (memory, CPU, environment variables) is set in the Coolify UI or
with `stx deploy update` / `stx deploy scale`; `stx deploy hetzner` has no
option for it.

### Examples

```
/stx-deploy:deploy
/stx-deploy:deploy ./projects/cours-python --subdomain cours-python
/stx-deploy:deploy . --serve-mode static-only
```

## Required readings BEFORE execution

1. `.claude/developer/skills/hetzner-infrastructure.md` — Streamlit config requirements
2. `.claude/developer/agents/deploy-operator.md` — deployment protocol

## Workflow

### Step 1: Adopt the Deploy Operator role

Read and adopt `.claude/developer/agents/deploy-operator.md`.

### Step 2: Check credentials and infrastructure

`.stx-deploy.env` must exist (workspace root or parent directory) with
`COOLIFY_URL` and `COOLIFY_API_TOKEN`. If it is missing:

```
Deployment credentials not found.
Run /stx-deploy:setup (or `stx deploy setup`) first,
or /stx-deploy:go to set up everything.
```

### Step 3: Preflight

```bash
stx deploy preflight PATH
```

It checks `book.py`, `pyproject.toml`, `.stx-version`, the `Dockerfile`,
static serving in `.streamlit/config.toml` and the `static/` folder, local
packs, a clean git tree, that secret files (`.env`, `.stx-deploy.env`,
`.stx-passwords.toml`) are git-ignored and kept out of the image by
`.dockerignore`, then runs the tests and the linter. Stop on any failure and
report it.

### Step 4: Deployment files

Coolify builds from the repository, so `Dockerfile`, `entrypoint.sh`,
`nginx.conf` and `.dockerignore` must be committed. If they are missing,
`stx deploy docker PATH --build-only` writes them (and builds the image
locally, which also proves it builds). `stx deploy diff PATH` shows how
existing files differ from the current templates.

### Step 5: Push

```bash
git status
git log --oneline -1
git remote -v
```

Coolify deploys what is on GitHub. If there are uncommitted changes or
unpushed commits, tell the user and stop until they push.

### Step 6: Deploy

```bash
stx deploy hetzner PATH [--subdomain NAME] [--serve-mode MODE] [--uuid UUID]
```

The command finds or creates the Coolify application (it guides the creation
in the Coolify UI when the API cannot), sets `STX_SERVE_MODE`, the exposed
port and the domain, rebuilds, waits for the health check, smoke-tests the
site and records the service in `.stx-deploy.json`.

### Step 7: Protect (optional)

To put the site behind the login screen:

```bash
stx deploy lock SERVICE        # passwords from .stx-passwords.toml (git-ignored)
stx deploy auth-status SERVICE # labels and dates, never a secret
```

### Step 8: Report

```
Project deployed:
  URL:     https://<subdomain>.<domain>
  Health:  OK (from stx deploy hetzner)

Check status:  stx deploy status
Rebuild:       stx deploy update SERVICE
```

If `.stx-deploy.json` shows no CDN, add:
```
Tip: no CDN or bot protection yet. Run /stx-deploy:configure-domain to set up Cloudflare (free).
```
