# SSH Operations — Shared patterns for remote server management

This skill centralizes SSH connection patterns used by all `/stx-deploy:*` commands
that interact with the Hetzner server.

## Credential resolution

Always read credentials in this order:

1. `.stx-deploy.env` in workspace root (preferred)
2. `.stx-deploy.env` in parent directory
3. Environment variables (`COOLIFY_URL`, `COOLIFY_API_TOKEN`, `HETZNER_API_TOKEN`, `HETZNER_SSH_KEY_PATH`)
4. `.stx-deploy.json` → `infrastructure.server.ipv4` and `infrastructure.server.ssh_key_path`
5. Prompt the user as last resort

The canonical SSH key path is `~/.ssh/hetzner_streamtex` (stored as `HETZNER_SSH_KEY_PATH`
in `.stx-deploy.env`). The SSH key name in Hetzner is `streamtex-deploy`.

## Connection patterns

### Standard SSH command (as root, during setup phases)

```bash
ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=accept-new root@$SERVER_IP "command"
```

### Standard SSH command (as deploy user, after secure phase)

```bash
ssh -i $SSH_KEY_PATH deploy@$SERVER_IP "command"
```

### Multi-line SSH script

```bash
ssh -i $SSH_KEY_PATH deploy@$SERVER_IP << 'REMOTE'
command1
command2
command3
REMOTE
```

### Which user to use

| Phase | User | Reason |
|-------|------|--------|
| provision (just created) | `root` | Only root exists |
| secure (hardening) | `root` → creates `deploy` user | Switch to deploy at the end |
| install-coolify | `root` | Coolify installer needs root |
| configure-domain | `deploy` | Post-hardening, sudo available |
| All maintenance ops | `deploy` | Standard operations |

## Server IP resolution

Read IP from `.stx-deploy.json`:
```
infrastructure.server.ipv4
```

If the key is `ip` instead of `ipv4` (v1 state format), try both:
```python
ip = state["infrastructure"]["server"].get("ipv4") or state["infrastructure"]["server"].get("ip")
```

## Health check after SSH operations

After any operation that changes the server state:
```bash
# Verify server is reachable
ssh -i $SSH_KEY_PATH deploy@$SERVER_IP "echo OK && uptime"
```

## Coolify-specific SSH patterns

### Check Coolify status
```bash
ssh -i $SSH_KEY_PATH deploy@$SERVER_IP "sudo docker ps --format '{{.Names}}\t{{.Status}}'"
```

### View container logs
```bash
ssh -i $SSH_KEY_PATH deploy@$SERVER_IP "sudo docker logs --tail 20 CONTAINER_NAME 2>&1"
```

### Check resource usage
```bash
ssh -i $SSH_KEY_PATH deploy@$SERVER_IP "free -h && echo '---' && df -h / && echo '---' && sudo docker stats --no-stream"
```

## Constants

These values are shared with the Python CLI (`streamtex.cli.coolify`):

| Constant | Value | Python constant name | Description |
|----------|-------|---------------------|-------------|
| SSH key path | `~/.ssh/hetzner_streamtex` | `DEFAULT_SSH_KEY_PATH` | Default key location |
| SSH key name | `streamtex-deploy` | `DEFAULT_SSH_KEY_NAME` | Name in Hetzner |
| SSH user | `deploy` | `DEFAULT_SSH_USER` | Non-root user |
| Server type | `cax21` | `DEFAULT_SERVER_TYPE` | Default ARM server |
| Location | `fsn1` | `DEFAULT_LOCATION` | Falkenstein datacenter |
| Coolify port | `8000` | `DEFAULT_COOLIFY_PORT` | Dashboard before domain setup |
| Streamlit port | `8501` | `DEFAULT_STREAMLIT_PORT` | App port inside Docker |
