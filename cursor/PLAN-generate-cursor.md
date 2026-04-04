# Plan d'implémentation — `generate_cursor.py`

> Version : 2026-03-16
> Script : `streamtex-claude/cursor/generate_cursor.py`
> Rôle : Générer un dossier `.cursor/` complet à partir d'un profil Claude installé (`.claude/`)

---

## 1. Table de conversion synthétique

### 1.1 Conversions par type de composant

| # | Source Claude | Destination Cursor | Format cible | Stratégie | Fidélité |
|---|-------------|-------------------|-------------|-----------|----------|
| C1 | `CLAUDE.md` (racine projet) | `.cursor/rules/00-project.mdc` | MDC `alwaysApply: true` | Découper en sections → 1 fichier `.mdc` par section H2 | Haute |
| C2 | `.claude/references/*.md` | `.cursor/rules/01-ref-<name>.mdc` | MDC `alwaysApply: true` | Copie directe + ajout frontmatter MDC | Haute |
| C3 | `.claude/commands/<group>/<cmd>.md` | `.cursor/commands/<group>/<cmd>.md` | Markdown brut | Copie + remplacement `$ARGUMENTS` → note explicative | Moyenne |
| C4 | `.claude/designer/skills/*.md` | `.cursor/rules/skill-<name>.mdc` | MDC Agent Requested | Ajout frontmatter `description:` extrait du H1/blockquote | Moyenne |
| C5 | `.claude/developer/skills/*.md` | `.cursor/rules/skill-<name>.mdc` | MDC Agent Requested | Idem C4 | Moyenne |
| C6 | `.claude/designer/agents/*.md` | `.cursor/rules/agent-<name>.mdc` | MDC `alwaysApply: false` + `description:` | Conversion en règle Agent Requested (pas d'agents Cursor) | Basse |
| C7 | `.claude/designer/templates/*.md` | `.cursor/commands/templates/<name>.md` | Markdown brut | Reconditionnement en commande slash | Moyenne |
| C8 | `.claude/designer/tools/*.md` | `.cursor/commands/tools/<name>.md` | Markdown brut | Reconditionnement en commande slash | Moyenne |
| C9 | `.claude/settings.json` | `.cursor/rules/00-permissions.mdc` | MDC `alwaysApply: true` | Traduction permissions → texte d'instruction | Basse |
| C10 | `.claude/designer/presentation/skills/*.md` | `.cursor/rules/skill-pres-<name>.mdc` | MDC Agent Requested | Idem C4 avec préfixe `pres-` | Moyenne |
| C11 | `.claude/designer/presentation/agents/*.md` | `.cursor/rules/agent-pres-<name>.mdc` | MDC Agent Requested | Idem C6 avec préfixe `pres-` | Basse |

### 1.2 Composants NON convertis (et pourquoi)

| Source Claude | Raison de non-conversion |
|--------------|-------------------------|
| `~/.claude/CLAUDE.md` (utilisateur global) | Scope utilisateur — hors projet, non versionnable |
| `~/.claude/settings.json` (global) | Idem |
| Auto-mémoire (`memory/`) | Pas d'équivalent Cursor — contenu dynamique |
| `.stx-profile` (marqueur) | Interne à l'installeur StreamTeX |
| `manifest.toml` | Métadonnée de profil, pas de pendant Cursor |

### 1.3 Transformations détaillées par fichier

#### C1 — CLAUDE.md → Règles projet découpées

```
CLAUDE.md (1 fichier monolithique)
  ↓ Découpage par section H2
  .cursor/rules/
    00-project-identity.mdc        ← ## Identity
    00-project-environment.mdc     ← ## Environment
    00-project-context-loading.mdc ← ## Context Loading
    00-project-coding.mdc          ← ## Coding Standards (si pas déjà dans references)
    00-project-structure.mdc       ← ## Project Structure
    00-project-workflows.mdc       ← ## Workflows
```

Chaque fichier `.mdc` reçoit :
```yaml
---
description: "<texte du H2 ou première ligne>"
alwaysApply: true
---
```

**Transformation spéciale** : Les références `@path/to/file` dans CLAUDE.md sont :
- Résolues (contenu inliné) si le fichier est un composant interne
- Converties en commentaire `<!-- Claude ref: @path/to/file -->` si externe

#### C2 — Références → Règles Always

```
.claude/references/coding_standards.md     → .cursor/rules/01-ref-coding-standards.mdc
.claude/references/streamtex_cheatsheet_en.md → .cursor/rules/01-ref-streamtex-cheatsheet.mdc
.claude/references/presentation_cheatsheet_en.md → .cursor/rules/01-ref-presentation-cheatsheet.mdc
```

Frontmatter ajouté :
```yaml
---
description: "StreamTeX coding standards — always apply"
alwaysApply: true
---
```

#### C3 — Commandes → Commandes Cursor

```
.claude/commands/stx-block/init.md    → .cursor/commands/stx-block/init.md
.claude/commands/stx-block/update.md  → .cursor/commands/stx-block/update.md
.claude/commands/stx-block/test.md    → .cursor/commands/stx-block/test.md
.claude/commands/stx-issue/bug.md        → .cursor/commands/stx-issue/bug.md
...
```

Transformations appliquées :
1. `$ARGUMENTS` → `{{USER_INPUT}}` + ajout en tête : `> Note: Provide your arguments after the slash command in the chat input.`
2. `$1`, `$2`, ... → supprimés avec note
3. Titre H1 conservé tel quel

#### C4/C5 — Skills → Règles Agent Requested

```
.claude/designer/skills/slide-design-rules.md → .cursor/rules/skill-slide-design-rules.mdc
.claude/designer/skills/visual-design-rules.md → .cursor/rules/skill-visual-design-rules.mdc
.claude/developer/skills/testing-patterns.md   → .cursor/rules/skill-testing-patterns.mdc
```

Description extraite automatiquement :
1. Si blockquote `> **Scope**: ...` → utiliser ce texte
2. Sinon H1 → utiliser le titre
3. Sinon premier paragraphe (tronqué à 200 car.)

```yaml
---
description: "Slide design rules for StreamTeX presentations — viewport constraints, typography, grid system"
alwaysApply: false
---
```

#### C6 — Agents → Règles Agent Requested (dégradé)

```
.claude/designer/agents/project-architect.md → .cursor/rules/agent-project-architect.mdc
.claude/designer/agents/slide-designer.md    → .cursor/rules/agent-slide-designer.mdc
.claude/designer/agents/slide-reviewer.md    → .cursor/rules/agent-slide-reviewer.mdc
```

Frontmatter :
```yaml
---
description: "Project Architect agent — designs project structure, block count, features (originally a Claude subagent)"
alwaysApply: false
---
```

Ajout d'un avertissement en tête du contenu :
```markdown
<!-- Converted from Claude Code agent. Original features lost: subagent isolation, dedicated model, tool restrictions, persistent memory. This rule provides the agent's knowledge as context only. -->
```

#### C7 — Templates → Commandes Cursor

```
.claude/designer/templates/project.md       → .cursor/commands/templates/project.md
.claude/designer/templates/presentation.md  → .cursor/commands/templates/presentation.md
.claude/designer/templates/collection.md    → .cursor/commands/templates/collection.md
.claude/designer/templates/course.md        → .cursor/commands/templates/course.md
```

Ajout d'un en-tête :
```markdown
> Template: Use this command to scaffold a new project using this template.
> Provide your project description after the slash command.
```

#### C8 — Tools → Commandes Cursor

```
.claude/designer/tools/survey-convert.md → .cursor/commands/tools/survey-convert.md
```

Même traitement que C7.

#### C9 — Permissions → Règle informative

Le fichier `.claude/settings.json` :
```json
{ "permissions": { "allow": ["Bash(uv run *)", "Bash(git status*)", ...] } }
```

Est converti en :
```yaml
---
description: "Allowed terminal commands — reference for agent"
alwaysApply: true
---
```
```markdown
# Allowed Commands

The following commands are pre-approved and can be run without confirmation:

- `uv run *` — Python execution via uv
- `uv sync*` — Dependency synchronization
- `git status*`, `git diff*`, `git log*` — Git read operations
- `git add *`, `git commit *` — Git write operations
- `gh issue *`, `gh auth *`, `gh repo view *` — GitHub CLI
```

---

## 2. Architecture du script

### 2.1 Arborescence générée

```
<project>/
├── .cursor/
│   ├── rules/
│   │   ├── 00-project-identity.mdc         ← C1 (CLAUDE.md découpé)
│   │   ├── 00-project-environment.mdc      ← C1
│   │   ├── 00-project-context-loading.mdc  ← C1
│   │   ├── 00-project-workflows.mdc        ← C1
│   │   ├── 00-permissions.mdc              ← C9
│   │   ├── 01-ref-coding-standards.mdc     ← C2
│   │   ├── 01-ref-streamtex-cheatsheet.mdc ← C2
│   │   ├── 01-ref-presentation-cheatsheet.mdc ← C2
│   │   ├── skill-slide-design-rules.mdc    ← C4
│   │   ├── skill-visual-design-rules.mdc   ← C4
│   │   ├── skill-style-conventions.mdc     ← C4
│   │   ├── skill-block-blueprints.mdc      ← C4
│   │   ├── skill-testing-patterns.mdc      ← C5
│   │   ├── skill-docs-lookup.mdc           ← C5
│   │   ├── agent-project-architect.mdc     ← C6
│   │   ├── agent-slide-designer.mdc        ← C6
│   │   └── agent-slide-reviewer.mdc        ← C6
│   └── commands/
│       ├── stx-block/
│       │   ├── init.md                     ← C3
│       │   ├── update.md                   ← C3
│       │   ├── audit.md                    ← C3
│       │   ├── fix.md                      ← C3
│       │   ├── tool.md                     ← C3
│       │   ├── test.md                     ← C3
│       │   └── lint.md                     ← C3
│       ├── stx-issue/
│       │   ├── bug.md                      ← C3
│       │   ├── feature.md                  ← C3
│       │   └── ...                         ← C3
│       ├── templates/
│       │   ├── project.md                  ← C7
│       │   └── ...                         ← C7
│       └── tools/
│           └── survey-convert.md           ← C8
└── .cursorignore                           ← copie de .claudeignore si existant
```

### 2.2 Convention de nommage des `.mdc`

| Préfixe | Source | Type MDC | Justification |
|---------|--------|----------|---------------|
| `00-project-*` | CLAUDE.md sections | Always | Chargé en premier, instructions fondamentales |
| `00-permissions` | settings.json | Always | Contexte permanent |
| `01-ref-*` | references/ | Always | Documentation de référence permanente |
| `skill-*` | skills/ | Agent Requested | L'IA décide quand charger |
| `agent-*` | agents/ | Agent Requested | Contexte d'agent chargé à la demande |

Le préfixe numérique (`00-`, `01-`) assure l'ordre de lecture pour les règles Always.

### 2.3 Modules du script

```
generate_cursor.py
│
├── main()                          # Point d'entrée CLI
├── parse_args()                    # --source, --target, --profile, --dry-run, --verbose
│
├── Convertisseurs (1 par type) :
│   ├── convert_claude_md()         # C1 : CLAUDE.md → règles découpées
│   ├── convert_references()        # C2 : references/ → règles Always
│   ├── convert_commands()          # C3 : commands/ → commands/ (avec $ARGUMENTS)
│   ├── convert_skills()            # C4/C5/C10 : skills/ → règles Agent Requested
│   ├── convert_agents()            # C6/C11 : agents/ → règles Agent Requested
│   ├── convert_templates()         # C7 : templates/ → commandes
│   ├── convert_tools()             # C8 : tools/ → commandes
│   ├── convert_permissions()       # C9 : settings.json → règle informative
│   └── convert_ignore()            # .claudeignore → .cursorignore
│
├── Utilitaires :
│   ├── extract_description()       # Extraire description d'un .md (blockquote > H1 > premier §)
│   ├── wrap_mdc()                  # Envelopper contenu markdown dans frontmatter MDC
│   ├── split_by_h2()              # Découper un fichier markdown par sections H2
│   ├── transform_arguments()       # Remplacer $ARGUMENTS, $1, $2 par notes
│   ├── resolve_imports()           # Résoudre les @path/to/file dans CLAUDE.md
│   └── write_file()               # Écriture avec création de répertoires + rapport
│
└── Rapport :
    └── generate_report()           # Résumé de conversion (fichiers créés, avertissements)
```

---

## 3. Interface CLI

```
usage: generate_cursor.py [-h] [--source SOURCE] [--target TARGET] [--dry-run] [--verbose]

Génère un dossier .cursor/ à partir d'un profil Claude installé.

options:
  --source SOURCE   Chemin vers le dossier .claude/ source (défaut: ./.claude)
  --target TARGET   Chemin vers le dossier .cursor/ cible (défaut: ./.cursor)
  --dry-run         Affiche les opérations sans écrire
  --verbose         Affiche le détail de chaque conversion
```

### 3.1 Modes d'utilisation

**Cas 1 — Depuis un projet StreamTeX existant** (`.claude/` déjà installé) :
```bash
cd mon-projet-stx/
python path/to/generate_cursor.py
# Lit ./.claude/ → Génère ./.cursor/
```

**Cas 2 — Depuis les sources de profils** (conversion directe) :
```bash
python generate_cursor.py --source ../streamtex-claude/profiles/project --target ./mon-projet/.cursor
```

**Cas 3 — Dry run pour vérification** :
```bash
python generate_cursor.py --dry-run --verbose
# Affiche ce qui serait généré sans écrire
```

---

## 4. Détail des transformations

### 4.1 Génération du frontmatter MDC

```python
def wrap_mdc(content: str, *, description: str, always_apply: bool, globs: str = "") -> str:
    """Enveloppe du contenu markdown dans le format MDC Cursor."""
    lines = ["---"]
    lines.append(f"description: {description}")
    if globs:
        lines.append(f'globs: "{globs}"')
    lines.append(f"alwaysApply: {'true' if always_apply else 'false'}")
    lines.append("---")
    lines.append("")
    lines.append(content)
    return "\n".join(lines)
```

### 4.2 Découpage de CLAUDE.md par H2

```python
def split_by_h2(content: str) -> list[tuple[str, str]]:
    """Retourne [(slug, section_content), ...] pour chaque ## du fichier."""
    # Regex : capture chaque section entre deux ## (ou fin de fichier)
    # Le slug est dérivé du titre H2 : "## Environment (MANDATORY)" → "environment"
```

### 4.3 Extraction de description

```python
def extract_description(content: str) -> str:
    """Extrait une description courte d'un fichier markdown.

    Priorité :
    1. Blockquote > **Scope**: ... → texte après "Scope:"
    2. Titre H1 → texte du titre
    3. Premier paragraphe → tronqué à 200 caractères
    """
```

### 4.4 Transformation des arguments

```python
def transform_arguments(content: str) -> str:
    """Remplace les placeholders Claude par des notes Cursor.

    $ARGUMENTS → {{USER_INPUT}} + note en tête
    $1, $2, ... → supprimés + note
    """
```

---

## 5. Gestion des profils avec héritage

Le script doit gérer le cas `presentation` qui étend `project` :

```
.claude/ (profil presentation installé)
├── commands/
│   ├── stx-block/             ← hérité de project
│   ├── stx-presentation/      ← ajouté par presentation
│   └── stx-issue/             ← shared
├── designer/
│   ├── skills/                ← hérité de project
│   ├── agents/                ← hérité de project
│   ├── templates/             ← hérité de project
│   ├── tools/                 ← hérité de project
│   └── presentation/
│       ├── skills/            ← ajouté par presentation
│       └── agents/            ← ajouté par presentation
├── developer/
│   └── skills/                ← hérité de project
└── references/                ← shared
```

Le script n'a **pas besoin** de connaître l'héritage — il parcourt simplement tous les fichiers présents dans `.claude/` après installation. L'héritage est déjà résolu par `install.py`.

---

## 6. Rapport de conversion

À la fin de l'exécution, le script affiche un rapport :

```
╭─ Conversion Claude → Cursor ─╮
│                               │
│  Source : ./.claude/           │
│  Cible  : ./.cursor/          │
│  Profil : project             │
│                               │
│  Règles (.mdc)     : 17      │
│    Always           : 7       │
│    Agent Requested  : 10      │
│  Commandes (.md)    : 28      │
│  Ignore             : 1       │
│                               │
│  ⚠ Avertissements :          │
│  - $ARGUMENTS dans 12 fichiers│
│    (remplacé par note)        │
│  - 3 agents convertis en      │
│    règles (perte isolation)   │
│                               │
│  ✗ Non converti :             │
│  - Mémoire (memory/)          │
│  - Marqueur (.stx-profile)    │
│                               │
╰───────────────────────────────╯
```

---

## 7. Plan d'implémentation par étapes

| Étape | Description | Dépendances | Complexité |
|-------|------------|-------------|------------|
| **E1** | Squelette CLI (`parse_args`, `main`, `write_file`) | Aucune | Faible |
| **E2** | `convert_references()` — C2 (la plus simple) | E1 | Faible |
| **E3** | `wrap_mdc()` + `extract_description()` — utilitaires MDC | E1 | Faible |
| **E4** | `convert_commands()` + `transform_arguments()` — C3 | E1 | Faible |
| **E5** | `convert_skills()` — C4/C5/C10 | E3 | Moyenne |
| **E6** | `convert_agents()` — C6/C11 | E3 | Moyenne |
| **E7** | `convert_claude_md()` + `split_by_h2()` + `resolve_imports()` — C1 | E3 | Haute |
| **E8** | `convert_templates()` + `convert_tools()` — C7/C8 | E1 | Faible |
| **E9** | `convert_permissions()` — C9 | E3 | Faible |
| **E10** | `convert_ignore()` — .claudeignore → .cursorignore | E1 | Faible |
| **E11** | `generate_report()` — rapport final | E2-E10 | Faible |
| **E12** | Tests : conversion du profil `project` complet + validation | E1-E11 | Moyenne |
| **E13** | Tests : profil `presentation` (héritage) + `library` + `documentation` | E12 | Moyenne |

### Ordre recommandé

```
E1 → E3 → E2 → E4 → E5 → E6 → E8 → E9 → E10 → E7 → E11 → E12 → E13
       ↑                                           ↑
   Utilitaires MDC                          Le plus complexe (CLAUDE.md)
   (nécessaires partout)                    (à faire en dernier)
```

---

## 8. Tests de validation

### 8.1 Tests unitaires

| Test | Vérifie |
|------|---------|
| `test_wrap_mdc_always` | Frontmatter MDC correct pour type Always |
| `test_wrap_mdc_agent_requested` | Frontmatter MDC correct pour type Agent Requested |
| `test_extract_description_blockquote` | Extraction depuis `> **Scope**: ...` |
| `test_extract_description_h1` | Extraction depuis titre H1 |
| `test_extract_description_paragraph` | Extraction depuis premier paragraphe |
| `test_split_by_h2` | Découpage correct en sections H2 |
| `test_transform_arguments` | `$ARGUMENTS` → note, `$1` → note |
| `test_resolve_imports` | `@path/to/file` → contenu inliné |

### 8.2 Tests d'intégration

| Test | Vérifie |
|------|---------|
| `test_convert_project_profile` | Conversion complète du profil `project` → nombre de fichiers, noms, types MDC |
| `test_convert_presentation_profile` | Profil `presentation` → inclut les fichiers project + overlay |
| `test_dry_run` | Aucun fichier écrit, rapport correct |
| `test_idempotent` | Deux exécutions successives → même résultat |
| `test_no_data_loss` | Tout le contenu markdown source est présent dans les fichiers cibles |

---

## 9. Limites connues et compromis

| Limite | Impact | Mitigation |
|--------|--------|------------|
| `$ARGUMENTS` non supporté par Cursor | Les commandes deviennent des prompts statiques | Note ajoutée en tête de chaque commande convertie |
| Pas de subagents dans Cursor | Les agents perdent isolation, modèle dédié, mémoire | Conversion en règle Agent Requested — le contenu est préservé comme contexte |
| Pas de Skills avec outils restreints | Cursor ne peut pas limiter les outils par commande | Avertissement dans le rapport |
| Références `@path` dans CLAUDE.md | Cursor `.mdc` n'a pas d'imports | Résolution (inlining) ou commentaire HTML |
| Permissions granulaires | Cursor n'a pas d'équivalent fichier | Conversion en texte informatif (règle Always) |
| Mémoire auto | Non convertible | Exclu de la conversion, mentionné dans le rapport |
| Taille de contexte | Trop de règles Always peuvent saturer le contexte Cursor | Préfixes numériques pour prioriser ; possibilité future de passer certaines règles en Agent Requested |
