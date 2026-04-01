# /stx-deploy:scale — Scale infrastructure up or out

Arguments: $ARGUMENTS

## Argument parsing

Parse `$ARGUMENTS` as: `[TARGET] [OPTIONS]`

**Positional**:
- `TARGET` — Service name, subdomain, or Coolify UUID to scale (required for `--replicas`)

**Options**:
- `--replicas N` — Scale a specific service to N containers (same FQDN, load-balanced by Traefik)
- `--analyze` — Analyze current metrics and recommend a scaling strategy (no action)
- `--vertical TYPE` — Upgrade the primary server to TYPE (e.g. `cax41`)
- `--horizontal` — Add a worker server + load balancer
- `--help` — Show scaling decision guide

### Examples

```
/stx-deploy:scale ai4se6d-genai-intro --replicas 5   # scale for a course session
/stx-deploy:scale ai4se6d-genai-intro --replicas 1   # scale back after the session
/stx-deploy:scale --analyze
/stx-deploy:scale --vertical cax41
/stx-deploy:scale --horizontal
/stx-deploy:scale --help
```

## Required readings BEFORE execution

1. `.claude/developer/skills/hetzner-infrastructure.md` — server types, pricing, capacity
2. `.claude/developer/agents/deploy-operator.md` — deployment protocol

## Workflow

### Step 1: Adopt the Deploy Operator role

Read and adopt `.claude/developer/agents/deploy-operator.md`.

### Step 2: Handle `--help`

Display the scaling decision table:

| Signal                           | Action                          |
|----------------------------------|---------------------------------|
| RAM > 80% sustained             | Vertical scaling (upgrade)      |
| RAM > 80% AND already on CCX43  | Horizontal scaling (add worker) |
| Need zero downtime              | Horizontal (multi-server + LB)  |
| Response time > 3s              | Check CPU; if saturated, scale  |
| LB connections > 80% capacity   | Upgrade load balancer           |
| 60+ projects on one server      | Add a server                    |

### Step 3: Check CDN status first

Read `.stx-deploy.json` and check `cdn.enabled`. If CDN is NOT configured:
```
Before scaling, consider adding Cloudflare CDN (free):
  - CDN caching reduces server load significantly
  - Bot/crawler blocking prevents wasted resources
  - Rate limiting stops abusive traffic
  - This may resolve your performance issue without scaling

Set up CDN: /stx-deploy:configure-domain $DOMAIN
```

### Step 4: Analyze (--analyze or default)

Collect metrics via SSH:
```bash
# RAM usage
ssh $USER@$IP "free -m | awk '/Mem:/{printf \"%.0f\", \$3/\$2*100}'"

# CPU usage
ssh $USER@$IP "top -bn1 | grep 'Cpu(s)' | awk '{print \$2}'"

# Disk usage
ssh $USER@$IP "df -h / | awk 'NR==2{print \$5}'"

# Container count and memory
ssh $USER@$IP "sudo docker stats --no-stream --format '{{.Name}} {{.MemUsage}}'"

# Number of projects
# (from .stx-deploy.json)
```

Display analysis:
```
Current Infrastructure Analysis:
  Server:     cax21 (4 vCPU, 8 GB RAM)
  RAM usage:  6.2 GB / 8 GB (78%)
  CPU usage:  35%
  Disk usage: 45%
  Projects:   22 deployed
  Capacity:   ~8 more projects (Doc profile)

Recommendation: RAM is approaching 80%. Consider:
  - Vertical: /stx-deploy:scale --vertical cax41 (32 GB, ~32 EUR/mo)
  - Horizontal: /stx-deploy:scale --horizontal (add worker, ~17 EUR/mo + LB ~6 EUR/mo)

Vertical is simpler. Horizontal provides redundancy.
```

### Step 5: Replica scaling (--replicas N)

Use the CLI to scale a single service to N containers:

```bash
stx deploy scale $TARGET --replicas $N
```

This calls `CoolifyClient.scale_app()` which:
- **Scale up**: Creates additional Coolify applications with the **same FQDN** — Traefik load-balances automatically via round-robin. Copies env vars (FOLDER, STX_SERVE_MODE, STX_PASSWORD) from the primary. Triggers a build for each new replica.
- **Scale down**: Stops and deletes excess replicas from the end.

Each Streamlit container handles ~10-15 concurrent users (limited by Python GIL). With N replicas, a service supports ~N×15 concurrent users.

**Capacity reference** (cax21, 16 GB RAM):
| Replicas | Concurrent users | Extra RAM |
|----------|-----------------|-----------|
| 1        | ~15             | 0         |
| 3        | ~45             | ~120 MB   |
| 5        | ~75             | ~240 MB   |
| 7        | ~100            | ~360 MB   |

After scaling, update `.stx-deploy.json` (done automatically by the CLI) and the CI workflow `services.json` if the project uses GitHub Actions auto-deploy (add replica UUIDs to the `"replicas"` array so CI rebuilds them too).

Display result:
```
ai4se6d-genai-intro scaled to 5 replica(s)
  Primary: x45el0zeq6eqhhv1vo99mz20
  Replica 2: aaa...
  Replica 3: bbb...
  ...
```

### Step 6: Vertical scaling (--vertical)

**IMPORTANT**: Vertical scaling requires a brief server shutdown (2-5 minutes of downtime).

1. Confirm with user:
```
Scaling streamtex-prod from cax21 → cax41:
  RAM:  8 GB → 32 GB
  vCPU: 4 → 16
  Cost: ~8.49 → ~31.99 EUR/month (+23.50 EUR)
  Downtime: 2-5 minutes

Proceed? (yes/no)
```

2. Shutdown, resize, restart:
```bash
hcloud server shutdown streamtex-prod
# Wait for status powered-off
hcloud server change-type streamtex-prod $NEW_TYPE
hcloud server poweron streamtex-prod
```

3. Wait for server to come back:
```bash
# Poll SSH until server responds
for i in $(seq 1 20); do
  ssh -o ConnectTimeout=5 $USER@$IP "echo ok" 2>/dev/null && break
  sleep 15
done
```

4. Verify all containers are running:
```bash
ssh $USER@$IP "sudo docker ps --format 'table {{.Names}}\t{{.Status}}'"
```

5. Run health checks on all projects.

6. Update `.stx-deploy.json` with new server type.

### Step 7: Horizontal scaling (--horizontal)

1. Provision and secure a new worker (reuse provision + secure logic)
2. If no load balancer exists, create one (reuse setup-loadbalancer logic)
3. Add the worker to Coolify
4. Suggest which projects to move to the new worker

```
Horizontal scaling complete!
  New worker: streamtex-worker-1 (cax21, 8 GB)
  Load balancer: streamtex-lb (lb11)
  Total capacity: 16 GB (2 servers)

To move projects to the new worker:
  In Coolify → Application → Settings → Server → select streamtex-worker-1
```

### Step 8: Update state and display result

Update `.stx-deploy.json` with all changes and display final status.
