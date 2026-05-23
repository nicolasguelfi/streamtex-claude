# PE Audit

Sub-mode skill for the **audit** scenario : run a standalone health audit
of an existing pack — independent of any extraction or retrofit cycle.

Read `pe-conventions.md` and `pe-go.md` before invoking.

## When to use

The user wants to evaluate the health of a pack : unused components,
duplicates, bundle gaps, naming conflicts, drift between contract and
implementation. The audit is **read-only** — it produces a report but
modifies no source files.

Triggers (from `ce-task.md` PACK_AUDIT archetype or `/stx-pe:audit`) :
- "audit my pack"
- "check the health of <pack>"
- "find unused components / duplicates in <pack>"

Note : audit is also auto-run by `bootstrap` and `specialize` at Step 6.
This standalone sub-mode is for invoking it OUTSIDE of an extraction
cycle.

## Inputs

- `<pack>` (mandatory) : pack ref or path. May be local path
  (`../streamtex-pack-design`) or remote ref (`git:url@rev`).
- `<projects>` (optional) : list of consumer projects to widen the
  audit's scope (usage statistics, drift detection). If omitted, auto-
  detect all projects in cwd's workspace whose `stx.toml` declares the
  pack.

## Workflow

1. **Resolve pack location** : if `<pack>` is a remote ref, clone to a
   temp directory ; otherwise use the local path directly.

2. **Detect consumer projects** : if `<projects>` not provided, scan
   sibling directories for `stx.toml` files declaring the pack. Surface
   QCM if zero or many found :

   > "Audit of pack `<name>`. <N> consumer projects found:
   > <list>. Include in the analysis?"
   > - Yes, all (Recommended)
   > - Selection to be specified
   > - None (audit the pack alone, no usage stats)
   > - Let's discuss

3. **Initialize pack-master-plan** (only if a plan file does NOT already
   exist) : write a minimal plan with `pack.mode = audit-only`. If a
   plan exists, append a new entry under `phases_completed` with mode
   `audit`.

4. **Run `pe-go` Step 6 only** :
   - Step 6 AUDIT : `pack-auditor` invoked with `<pack-path>` and
     `<consumer-projects>`. Output : `audit-report.md`.

5. **No gate** — audit is read-only. The report is presented to the
   user with a follow-up QCM if findings warrant action :

   > "The audit identified <N> recommendations: <H> HIGH, <M> MEDIUM,
   > <L> LOW. What do you do?"
   > - Launch a refine cycle to fix the HIGH items (Recommended)
   > - Keep the report for later
   > - Let's discuss

6. **No Step 7 PUBLISH** — audit doesn't change the pack so no version bump.

## Outputs

- `docs/pack-engineering/<ts>/audit-report.md` with the full health
  report (sections : Unused components, Duplicates, Bundle gaps,
  Naming conflicts, Contract-implementation drift, Test coverage).
- `pack-master-plan.yaml` populated `audit` section with the summary
  counts (decisions_log entry : `audit_completed`).

## Specific QCMs

When the audit detects HIGH-severity issues :

> "The following HIGH issues are immediately actionable: <list>.
> Launch a refine cycle targeted at these components?"
> - Yes (Recommended)
> - Selection to be specified
> - No, I'll handle it manually
> - Let's discuss
