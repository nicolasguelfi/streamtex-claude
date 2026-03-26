# /stx-deploy:setup — Setup local deployment environment

Arguments: $ARGUMENTS

## Purpose

Prepare the local machine for Hetzner/Coolify deployment by installing
required CLI tools, generating SSH keys, and storing API credentials
in `.stx-deploy.env`.

This is the FIRST command a new user runs before any other `/stx-deploy:*` command.
After setup, all subsequent commands read credentials automatically from `.stx-deploy.env`.

## Argument parsing

Parse `$ARGUMENTS` as: `[OPTIONS]`

**Options**:
- `--check` — Only verify current setup, don't install anything
- `--help` — Show this help

### Examples

```
/stx-deploy:setup                  # full interactive setup
/stx-deploy:setup --check          # verify only
```

## Required readings BEFORE execution

1. `.claude/developer/agents/deploy-operator.md` — deployment protocol

## Workflow

### Step 1: Adopt the Deploy Operator role

Read and adopt `.claude/developer/agents/deploy-operator.md`.

### Step 2: Check existing state

Check if `.stx-deploy.env` already exists in the workspace root (parent of current project).

If it exists and `--check` is NOT set:
```
Existing .stx-deploy.env found. Verifying...
```
Verify each tool and credential, report status, offer to fix missing items.

### Step 3: Hetzner CLI (hcloud)

Check:
```bash
which hcloud && hcloud version
```

If NOT found:
```
hcloud CLI not found. Installing...
```

Install based on platform:
- macOS: `brew install hcloud`
- Linux: `curl -sL https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-$(uname -m).tar.gz | tar xz && sudo mv hcloud /usr/local/bin/`

After install, verify:
```bash
hcloud version
```

### Step 4: Hetzner API token

Check if `HETZNER_API_TOKEN` is in `.stx-deploy.env` or environment.

If NOT found, guide the user:
```
You need a Hetzner API token.

1. Go to: https://console.hetzner.cloud
2. Create an account (if you don't have one)
3. Create a project (e.g. "streamtex")
4. Go to: Security → API Tokens → Generate API Token
5. Select "Read & Write" permissions
6. Copy the token
```

Ask the user to paste the token. Do NOT echo it back.

Configure hcloud CLI context:
```bash
hcloud context create streamtex --token $TOKEN
```

Verify:
```bash
hcloud server list
```

### Step 5: SSH key

Check for existing SSH key:
```bash
ls -la ~/.ssh/hetzner_streamtex*
```

If NOT found:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/hetzner_streamtex -N "" -C "streamtex-deploy"
```

Register in Hetzner:
```bash
hcloud ssh-key create --name streamtex-deploy --public-key-from-file ~/.ssh/hetzner_streamtex.pub
```

Save the returned SSH key ID.

### Step 6: Domain name

Ask the user:
```
Do you have a domain name for your deployment?

Options:
1. I have a domain (e.g. mysite.org)
2. I'll use the server IP directly (no custom domain)
3. I need to buy a domain

If option 3:
  Recommended registrars:
  - Cloudflare Registrar ($10/year for .org, built-in CDN)
  - Namecheap (~$9/year)
  - OVH (~$10/year)
```

If the user has a domain, ask for it and the registrar name.

### Step 7: Cloudflare API token (optional)

If the user's domain uses Cloudflare (or they want to set it up):
```
Cloudflare API token enables automatic DNS record management.

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Create Token → Edit zone DNS (template)
3. Zone Resources: Include → Specific zone → your-domain.org
4. Copy the token
```

Ask to paste. This is optional — without it, DNS records must be created manually.

### Step 8: Save .stx-deploy.env

Write all collected credentials to `.stx-deploy.env` in the workspace root:

```env
# StreamTeX Deployment Credentials
# Created by: /stx-deploy:setup on YYYY-MM-DD
# WARNING: This file contains secrets. Never commit to git.

# Hetzner
HETZNER_API_TOKEN=xxxx
HETZNER_SSH_KEY_PATH=~/.ssh/hetzner_streamtex
HETZNER_SSH_KEY_ID=12345

# Domain
DOMAIN=mysite.org
DOMAIN_REGISTRAR=cloudflare

# Cloudflare (optional)
CLOUDFLARE_API_TOKEN=xxxx

# Coolify (filled after install-coolify)
COOLIFY_URL=
COOLIFY_API_TOKEN=
```

Verify `.stx-deploy.env` is in `.gitignore`. If not, add it.

### Step 9: Display summary

```
✓ Local Deployment Setup Complete

  hcloud CLI:     v1.48.0 ✓
  SSH key:        ~/.ssh/hetzner_streamtex ✓  (Hetzner ID: 12345)
  Hetzner token:  ****...xxxx ✓
  Domain:         mysite.org (cloudflare)
  Cloudflare:     ✓ (auto DNS enabled)

  Credentials saved to: .stx-deploy.env

Next step: /stx-deploy:provision
  This will create a Hetzner server (~4.5€/month for cax21).
```
