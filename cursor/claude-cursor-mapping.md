# Claude Code / Cursor IDE — Table de correspondance complète

> Version : 2026-03-16
> Objectif : permettre la conversion bidirectionnelle des composants de configuration
> entre l'écosystème Claude Code et l'écosystème Cursor IDE.

---

## Partie 1 — Taxonomie des concepts et correspondances

### 1.1 Instructions système (System Prompts)

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Instructions globales utilisateur** | Directives appliquées à tous les projets, personnalité et style de communication de l'IA | `~/.claude/CLAUDE.md` (fichier utilisateur) | **User Rules** dans Cursor Settings > Rules (texte brut, non versionné) |
| **Instructions projet** | Règles spécifiques au projet, partagées avec l'équipe via git | `./CLAUDE.md` ou `./.claude/CLAUDE.md` à la racine du projet | `.cursor/rules/*.mdc` avec `alwaysApply: true` (fichiers MDC versionnés) |
| **Instructions modulaires par sujet** | Règles organisées par thème, chargées conditionnellement | `.claude/rules/*.md` avec frontmatter `paths:` optionnel | `.cursor/rules/*.mdc` avec types : Always, Auto Attached, Agent Requested, Manual |
| **Instructions contextuelles par chemin** | Règles activées uniquement quand certains fichiers sont touchés | `.claude/rules/rule.md` avec `paths: ["src/**/*.ts"]` | `.cursor/rules/rule.mdc` avec `globs: "src/**/*.ts"` et `alwaysApply: false` |
| **Instructions ancêtres (héritage arborescent)** | Chargement récursif en remontant l'arborescence des répertoires | CLAUDE.md découverts dans les répertoires parents automatiquement | Non supporté — les règles sont uniquement dans `.cursor/rules/` |
| **Instructions gérées (entreprise)** | Politiques imposées par l'IT, non modifiables par l'utilisateur | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Pas d'équivalent natif (déploiement via MDM/GPO possible) |
| **Imports de fichiers dans les instructions** | Inclusion de fichiers externes dans les instructions | `@path/to/file` dans CLAUDE.md (max 5 niveaux) | Pas de syntaxe d'import — chaque `.mdc` est autonome |

### 1.2 Commandes personnalisées (Custom Commands)

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Commande slash simple** | Prompt réutilisable invoqué par `/nom` | Fichier `.md` dans `.claude/commands/nom.md` | Fichier `.md` dans `.cursor/commands/nom.md` |
| **Commande slash avec sous-commandes** | Groupe de commandes sous un namespace (`/group:sub`) | Dossier `.claude/commands/group/sub.md` | Dossier `.cursor/commands/group/sub.md` (même convention) |
| **Arguments de commande** | Passage de paramètres utilisateur à la commande | `$ARGUMENTS`, `$1`, `$2`, ... dans le corps du fichier | Pas de substitution dynamique — le texte du `.md` est envoyé tel quel |
| **Commandes globales (tous projets)** | Commandes disponibles dans tous les projets | `~/.claude/commands/nom.md` | Non supporté — commandes uniquement au niveau projet |

### 1.3 Skills (Compétences spécialisées)

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Skill invocable par l'utilisateur** | Prompt spécialisé avec outils restreints, invoqué par `/skill` | `.claude/skills/nom/SKILL.md` avec frontmatter complet (tools, model, context) | Pas d'équivalent direct — approximable par `.cursor/commands/nom.md` + `.cursor/rules/nom.mdc` |
| **Skill invocable par l'IA** | Compétence que l'IA charge automatiquement quand pertinent | `SKILL.md` avec `user-invocable: false` + description | `.cursor/rules/nom.mdc` de type **Agent Requested** (`alwaysApply: false`, `description` renseignée, `globs` vide) |
| **Skill avec outils restreints** | Limiter les outils disponibles pour une tâche | `allowed-tools: Read, Grep` dans frontmatter SKILL.md | Non supporté — pas de restriction d'outils par commande |
| **Skill avec modèle dédié** | Forcer un modèle spécifique pour la skill | `model: sonnet` dans frontmatter | Non supporté au niveau commande (modèle configurable globalement) |
| **Skill avec contexte isolé** | Exécuter la skill dans un sous-agent isolé | `context: fork` + `agent: Explore` dans frontmatter | Non supporté — toutes les commandes partagent le même contexte |

### 1.4 Agents et sous-agents

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Agent personnalisé** | Agent avec rôle, prompt système, outils et modèle dédiés | `.claude/agents/nom.md` avec frontmatter (tools, model, memory, etc.) | Pas d'équivalent — Cursor n'a pas de système d'agents personnalisés |
| **Agent en arrière-plan** | Agent exécuté sans bloquer l'interaction | `background: true` dans frontmatter agent | **Background Agents** (cloud VMs, jusqu'à 20 en parallèle) — architecture très différente |
| **Agent avec isolation git** | Agent travaillant dans un worktree git séparé | `isolation: worktree` dans frontmatter | Background Agents utilisent des worktrees git isolés automatiquement |
| **Agent avec mémoire persistante** | Agent qui conserve des connaissances entre sessions | `memory: user\|project\|local` → fichiers dans `agent-memory/` | Automations ont un **memory tool** — mais pas les agents interactifs |
| **Composition d'agents** | Orchestrer plusieurs agents spécialisés | Agents peuvent invoquer d'autres agents via l'outil Agent | Non supporté — pas de composition d'agents |
| **Agents intégrés** | Agents pré-définis optimisés pour des tâches courantes | `Explore`, `Plan`, `general-purpose`, etc. | Mode Agent unique (Cmd+.) sans variantes spécialisées |

### 1.5 Templates et outils spécialisés

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Template de projet** | Modèle de scaffolding définissant structure, thème, typographie par défaut | `.claude/designer/templates/nom.md` (project, presentation, collection, course) | `.cursor/commands/templates/nom.md` — reconditionnés en commandes slash |
| **Outil spécialisé** | Agent dédié à une tâche technique spécifique (ex: conversion de captures) | `.claude/designer/tools/nom.md` invoqué via `/stx-block:tool <nom>` | `.cursor/commands/tools/nom.md` — reconditionnés en commandes slash |

### 1.6 Hooks (Automatisations du cycle de vie)

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Hook avant exécution d'outil** | Script exécuté avant qu'un outil soit utilisé (peut bloquer) | `PreToolUse` dans `settings.json` → hooks | `beforeShellExecution`, `beforeMCPExecution`, `beforeReadFile` dans `.cursor/hooks.json` |
| **Hook après exécution d'outil** | Script exécuté après qu'un outil a réussi | `PostToolUse` dans settings.json | `afterFileEdit` dans `.cursor/hooks.json` |
| **Hook au démarrage de session** | Script exécuté quand une session commence | `SessionStart` | Pas d'équivalent direct |
| **Hook à la soumission du prompt** | Script exécuté avant le traitement du prompt utilisateur | `UserPromptSubmit` | `beforeSubmitPrompt` dans `.cursor/hooks.json` |
| **Hook à l'arrêt** | Script exécuté quand l'agent termine | `Stop` | `stop` dans `.cursor/hooks.json` |
| **Hook de notification** | Script exécuté quand l'IA demande l'attention de l'utilisateur | `Notification` | Pas d'équivalent |
| **Hook asynchrone** | Hook qui s'exécute en arrière-plan sans bloquer | `"async": true` dans la config hook | Non documenté |
| **Hook de type prompt/agent** | Hook qui évalue via un LLM au lieu d'un script shell | `type: prompt` ou `type: agent` | Non supporté — hooks uniquement shell |
| **Hook HTTP** | Hook qui envoie un POST à un endpoint | `type: http` | Non supporté |
| **Matcher de hook** | Filtre pour cibler un outil ou événement spécifique | `matcher: "Bash"`, `matcher: "Edit\|Write"`, regex | Pas de matcher — les hooks s'appliquent à tout l'événement |

### 1.7 Serveurs MCP (Model Context Protocol)

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Serveur MCP projet** | Serveur MCP partagé via le repo git | `.mcp.json` à la racine du projet | `.cursor/mcp.json` au niveau projet |
| **Serveur MCP utilisateur** | Serveur MCP global pour tous les projets | `~/.claude.json` (section mcpServers) | `~/.cursor/mcp.json` (global) |
| **Transport stdio** | Serveur local communiquant via stdin/stdout | `type: stdio` + `command` + `args` | `command` + `args` (même format) |
| **Transport HTTP** | Serveur distant via HTTP streamable | `type: http` + `url` | Supporté (Streamable HTTP) |
| **Transport SSE** | Serveur via Server-Sent Events (déprécié) | `type: sse` + `url` | Supporté |
| **Variables d'environnement dans MCP** | Injection de secrets dans la config MCP | `${VAR}` et `${VAR:-default}` dans `.mcp.json` | `env: {}` dans la config serveur |
| **OAuth pour MCP** | Authentification OAuth pour serveurs distants | `--callback-port`, `--client-id`, `--client-secret` via CLI | Supporté via l'UI Cursor |
| **MCP géré (entreprise)** | Serveurs imposés par l'IT | `managed-mcp.json` + `allowedMcpServers`/`deniedMcpServers` | Pas d'équivalent natif |

### 1.8 Configuration et permissions

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Fichier de configuration projet** | Paramètres partagés avec l'équipe | `.claude/settings.json` (versionné) | `.cursor/rules/*.mdc` + `.vscode/settings.json` |
| **Fichier de configuration local** | Paramètres personnels non versionnés | `.claude/settings.local.json` (gitignored) | Cursor Settings UI (stocké localement) |
| **Fichier de configuration utilisateur** | Paramètres globaux pour tous les projets | `~/.claude/settings.json` | Cursor Settings > User |
| **Permissions par outil** | Contrôle granulaire allow/ask/deny par outil | `permissions: { allow: ["Bash(npm *)"], deny: [...] }` | Pas d'équivalent granulaire — activation/désactivation globale des fonctionnalités Agent |
| **Mode de permission** | Niveau global d'autonomie de l'IA | `defaultMode: default\|acceptEdits\|plan\|dontAsk\|bypassPermissions` | Auto-run terminal commands (on/off), Allow file deletion (on/off) |
| **Sandbox (isolation)** | Isolation filesystem/réseau pour les commandes | `sandbox: { mode: strict, filesystem: {...}, network: {...} }` | Pas d'équivalent pour l'agent local (Background Agents ont un sandbox cloud) |

### 1.9 Fichiers d'exclusion

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Exclusion IA** | Fichiers invisibles pour l'IA | `.claudeignore` (syntaxe gitignore) | `.cursorignore` (syntaxe gitignore, best-effort) |
| **Exclusion indexation** | Fichiers exclus de l'indexation/recherche | `.claudeignore` (même fichier) | `.cursorindexingignore` (dédié à l'indexation) |

### 1.10 Mémoire et persistance

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Mémoire automatique** | L'IA sauvegarde et rappelle des connaissances entre sessions | `~/.claude/projects/<project>/memory/` avec `MEMORY.md` + fichiers thématiques | Pas d'équivalent natif pour l'agent interactif |
| **Mémoire d'agent** | Connaissances persistantes par agent | `agent-memory/` (user, project, local scopes) | **Memory tool** dans les Automations uniquement |
| **Sessions persistantes** | Reprise de conversation | `~/.claude/projects/<project>/sessions/` — reprise auto, nommage, checkpoint | Historique de chat Cursor (moins structuré, pas de checkpoint) |

### 1.11 Contexte et références

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Référence à un fichier** | Inclure un fichier dans le contexte | Outil Read / mention de chemin dans le prompt | `@File` ou `#file` dans le chat |
| **Référence à un dossier** | Inclure la structure d'un répertoire | Outil Glob / Bash ls | `@Folder` dans le chat |
| **Recherche web** | Chercher sur internet | Outils WebSearch / WebFetch | `@Web` dans le chat |
| **Référence documentation externe** | Indexer et référencer de la doc externe | WebFetch sur une URL | `@Docs` (indexation persistante d'URLs de documentation) |
| **Recherche dans le codebase** | Recherche sémantique dans tout le projet | Outils Grep / Glob / Agent Explore | `@Codebase` (recherche sémantique vectorielle) |
| **Référence à un symbole de code** | Cibler une fonction/classe spécifique | Grep + Read (manuel) | `@Code` (navigation de symboles intégrée) |
| **Référence Git** | Inclure commits, diffs, PRs | Outil Bash (git log, git diff) | `@Git` (intégré, commits/diffs/PRs) |
| **Référence à une URL** | Charger le contenu d'une URL | WebFetch | `@Link` |
| **Erreurs lint** | Inclure les erreurs de linting | Bash (exécuter le linter) | `@Lint Errors` (intégré) |
| **Changements récents** | Voir les modifications récentes | Bash (git diff, git log) | `@Recent Changes` (intégré) |
| **Référence à une règle** | Inclure explicitement une règle | `@path/to/file` dans CLAUDE.md | `@Cursor Rules` + `@ruleName` (type Manual) |

### 1.12 Plugins et extensibilité

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Plugin / Extension** | Package distribuable de composants | `.claude-plugin/plugin.json` + skills, agents, hooks, MCP | Extensions VS Code (architecture complètement différente) |
| **Marketplace** | Distribution centralisée de plugins | `.claude-code-marketplace.json` (repo GitHub) | VS Code Marketplace (extensions IDE, pas de composants IA) |
| **Installation de plugin** | Ajouter un plugin au projet | `/plugin install` depuis un marketplace | `ext install publisher.extension` |

### 1.13 Raccourcis clavier

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Configuration des raccourcis** | Personnaliser les raccourcis clavier | `~/.claude/keybindings.json` (format JSON avec contextes) | `keybindings.json` de VS Code (format JSON, hérité de VS Code) |
| **Chords (séquences)** | Raccourcis multi-touches | `ctrl+k ctrl+s` (supporté) | `ctrl+k ctrl+s` (supporté, hérité de VS Code) |

### 1.14 Automatisations externes

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Automatisation par événement externe** | Déclenchement par Slack, GitHub, Linear, etc. | Non natif — possible via MCP + hooks | **Automations** (cursor.com/automations) : Slack, Linear, GitHub, PagerDuty, cron, webhooks |
| **Agent cloud** | Exécution dans un sandbox cloud | Non natif (exécution locale uniquement) | **Background Agents** dans des VMs Ubuntu cloud |
| **Agents parallèles** | Plusieurs agents simultanés | Oui (subagents locaux avec isolation worktree) | Jusqu'à 20 Background Agents parallèles (cloud) |

### 1.15 Intégration IDE

| Concept | Description / Finalité | Claude Code | Cursor IDE |
|---------|----------------------|-------------|------------|
| **Extension VS Code** | Intégration dans VS Code | Extension Claude Code pour VS Code | Natif (Cursor EST un fork de VS Code) |
| **Extension JetBrains** | Intégration dans IntelliJ/PyCharm | Extension Claude Code pour JetBrains | Plugin Cursor pour JetBrains (via ACP) |
| **Inline editing** | Modification de code en place | Via outil Edit dans le terminal | `Cmd+K` (édition inline contextuelle) |
| **Application desktop** | Interface graphique autonome | Claude Desktop (séparé de Claude Code CLI) | Cursor IDE (application complète) |

---

## Partie 2 — Conversion Claude Code → Cursor IDE

Guide pour convertir chaque composant Claude Code vers son équivalent Cursor.

### 2.1 CLAUDE.md → Cursor Rules

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `~/.claude/CLAUDE.md` (utilisateur) | Copier le contenu dans **Cursor Settings > Rules** (User Rules) | Pas de syntaxe `@import` — aplatir les références. Pas de versionnement. |
| `./CLAUDE.md` (projet) | Créer `.cursor/rules/project.mdc` avec `alwaysApply: true` | Pas d'héritage arborescent — un seul niveau de règles projet. Frontmatter MDC requis. |
| `.claude/rules/rule.md` sans `paths:` | `.cursor/rules/rule.mdc` avec `alwaysApply: true` | Format MDC (YAML frontmatter) au lieu de Markdown pur. |
| `.claude/rules/rule.md` avec `paths: ["src/**"]` | `.cursor/rules/rule.mdc` avec `globs: "src/**"` et `alwaysApply: false` | Syntaxe de glob légèrement différente. |
| Imports `@path/to/file` dans CLAUDE.md | Copier le contenu du fichier référencé directement dans le `.mdc` | Pas d'import — duplication nécessaire. Maintenance plus difficile. |

**Procédure de conversion :**
```
CLAUDE.md / .claude/rules/*.md
  ↓ Pour chaque fichier :
  1. Identifier le scope (global, projet, conditionnel par chemin)
  2. Résoudre les imports @path (inliner le contenu)
  3. Créer le fichier .mdc avec le frontmatter approprié :
     ---
     description: "<description pour l'IA>"
     globs: "<pattern>" (si conditionnel)
     alwaysApply: true|false
     ---
  4. Placer dans .cursor/rules/
```

### 2.2 Commandes slash → Cursor Commands

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `.claude/commands/nom.md` | `.cursor/commands/nom.md` | **Pas de substitution `$ARGUMENTS`** — le prompt est statique. L'utilisateur doit ajouter le contexte manuellement dans le chat. |
| `.claude/commands/group/sub.md` | `.cursor/commands/group/sub.md` | Même structure de sous-dossiers — compatible. |
| `~/.claude/commands/nom.md` (global) | Pas de conversion directe | Copier dans chaque projet `.cursor/commands/` ou utiliser un script de sync. |

**Limites importantes :**
- Pas de `$ARGUMENTS`, `$1`, `$2` — les commandes Cursor sont des prompts statiques
- Pas de commandes globales — uniquement au niveau projet
- Pas de frontmatter (description, argument-hint) — le fichier entier est le prompt

### 2.3 Skills → Rules + Commands (approximation)

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| Skill invocable par l'utilisateur (`/skill`) | `.cursor/commands/skill.md` (prompt) + `.cursor/rules/skill.mdc` (connaissances) | **Perte** : restriction d'outils, modèle dédié, contexte isolé, substitution d'arguments. |
| Skill invocable par l'IA | `.cursor/rules/skill.mdc` type **Agent Requested** (`alwaysApply: false`, `description` renseignée) | L'IA Cursor choisit de charger la règle selon la description. Pas de contrôle d'outils. |
| Skill avec `allowed-tools` | Pas de conversion | Cursor ne permet pas de restreindre les outils par commande/règle. |
| Skill avec `model: sonnet` | Pas de conversion | Le modèle est global dans Cursor, pas par commande. |
| Skill avec `context: fork` | Pas de conversion | Pas d'isolation de contexte dans Cursor. |

**Stratégie recommandée :**
1. Séparer le contenu de la skill en deux fichiers :
   - `.cursor/rules/skill-knowledge.mdc` → les connaissances/règles (Agent Requested)
   - `.cursor/commands/skill-action.md` → le workflow/prompt d'action
2. Accepter la perte de fonctionnalités (outils, modèle, isolation)

### 2.4 Agents → Non convertible (approximation partielle)

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `.claude/agents/nom.md` | `.cursor/rules/agent-nom.mdc` (Always) contenant le prompt système de l'agent | **Perte majeure** : pas de subagents dans Cursor. Le prompt est chargé mais sans isolation, outils dédiés, mémoire, ni modèle séparé. |
| Agent avec `memory: project` | Pas de conversion | Pas de mémoire persistante par agent dans Cursor. |
| Agent avec `isolation: worktree` | Background Agent (cloud) | Architecture complètement différente — cloud vs local. |
| Composition d'agents | Pas de conversion | Cursor n'a pas d'orchestration d'agents. |

**Stratégie recommandée :**
- Convertir le prompt système de l'agent en règle `.mdc` Always
- Documenter les limitations dans un fichier `MIGRATION-NOTES.md`
- Pour les workflows multi-agents, créer des commandes séquentielles

### 2.5 Hooks → Cursor Hooks (partiel)

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `PreToolUse` (Bash) | `beforeShellExecution` dans `.cursor/hooks.json` | **Pas de matcher** — s'applique à toutes les commandes shell. Pas de filtrage par pattern. |
| `PreToolUse` (Read) | `beforeReadFile` | OK — équivalent direct. |
| `PreToolUse` (MCP) | `beforeMCPExecution` | OK — équivalent direct. |
| `PostToolUse` (Edit/Write) | `afterFileEdit` | OK — reçoit ancien/nouveau contenu. |
| `UserPromptSubmit` | `beforeSubmitPrompt` | OK — équivalent direct. |
| `Stop` | `stop` | OK — équivalent direct. |
| `SessionStart` | Pas de conversion | Pas de hook de démarrage dans Cursor. |
| `Notification` | Pas de conversion | Pas de hook de notification. |
| `SubagentStart/Stop` | Pas de conversion | Pas de subagents dans Cursor. |
| `PostToolUseFailure` | Pas de conversion | Cursor n'a pas de hook d'échec spécifique. |
| Hook `type: prompt` (évaluation LLM) | Pas de conversion | Cursor hooks uniquement shell. |
| Hook `type: http` | Pas de conversion | Cursor hooks uniquement shell. |
| Hook `type: agent` | Pas de conversion | Cursor hooks uniquement shell. |
| Hook avec `matcher` | Pas de conversion | Pas de matcher dans Cursor — le hook s'applique à tout l'événement. |
| Hook `async: true` | Pas de conversion | Non documenté dans Cursor. |

**Format de conversion :**
```json
// Claude: .claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "./scripts/guard.sh" }]
    }]
  }
}

// Cursor: .cursor/hooks.json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      { "command": "./scripts/guard.sh" }
    ]
  }
}
```

### 2.6 MCP → Cursor MCP (bonne compatibilité)

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `.mcp.json` (projet) | `.cursor/mcp.json` | Même format JSON. Déplacer dans `.cursor/`. |
| `~/.claude.json` mcpServers | `~/.cursor/mcp.json` | Extraire la section `mcpServers` et copier. |
| Transport `stdio` | `command` + `args` | Compatible — même format. |
| Transport `http` | Supporté | Compatible. |
| `${VAR:-default}` dans config | `env: { "VAR": "value" }` | La syntaxe `${VAR:-default}` peut ne pas être supportée — utiliser `env` explicitement. |
| MCP géré (`managed-mcp.json`) | Pas de conversion | Pas d'équivalent entreprise natif dans Cursor. |

### 2.7 Permissions → Configuration limitée

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `permissions.allow` / `deny` / `ask` | Cursor Settings > Features > Agent | **Perte de granularité** : Cursor offre uniquement on/off pour "auto-run terminal" et "allow file deletion". Pas de patterns par outil. |
| `sandbox` (filesystem/réseau) | Pas de conversion | Cursor local n'a pas de sandbox. Background Agents ont un sandbox cloud non configurable. |
| `.claudeignore` | `.cursorignore` | Même syntaxe gitignore. Renommer le fichier. Cursor est "best-effort" (pas garanti). |

### 2.8 Mémoire → Pas d'équivalent

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `memory/MEMORY.md` + fichiers | `.cursor/rules/memory.mdc` (Always) | **Dégradé** : pas de mise à jour automatique. Contenu statique figé au moment de la conversion. L'IA Cursor ne peut pas écrire dans les rules. |
| Mémoire d'agent | Pas de conversion | Non supporté. |

### 2.9 Plugins → Non convertible

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `.claude-plugin/` | Pas d'équivalent | L'écosystème de plugins Claude Code (skills + agents + hooks + MCP bundlés) n'a pas de pendant dans Cursor. Les extensions VS Code couvrent un périmètre différent (UI, LSP, etc.). |

### 2.10 Raccourcis clavier → keybindings.json VS Code

| Composant Claude | Conversion Cursor | Limites |
|-----------------|-------------------|---------|
| `~/.claude/keybindings.json` | `keybindings.json` de Cursor/VS Code | Formats différents. Les actions Claude Code (`chat:submit`, etc.) n'existent pas dans Cursor. Conversion manuelle action par action nécessaire. |

---

## Partie 3 — Conversion Cursor IDE → Claude Code

Guide pour convertir chaque composant Cursor vers son équivalent Claude Code.

### 3.1 Cursor Rules → CLAUDE.md / .claude/rules/

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| User Rules (Cursor Settings) | `~/.claude/CLAUDE.md` | OK — copier le texte. |
| `.cursorrules` (legacy, racine) | `./CLAUDE.md` | OK — renommer et placer à la racine. |
| `.cursor/rules/rule.mdc` `alwaysApply: true` | `.claude/rules/rule.md` sans `paths:` | Retirer le frontmatter MDC, garder uniquement le contenu Markdown. |
| `.cursor/rules/rule.mdc` avec `globs:` | `.claude/rules/rule.md` avec `paths:` | Convertir `globs: "src/**/*.ts"` → `paths: ["src/**/*.ts"]`. |
| `.cursor/rules/rule.mdc` type Agent Requested | `.claude/rules/rule.md` sans `paths:` (toujours chargé) **ou** skill auto-invocable | Claude rules ne supportent pas le chargement conditionnel par description. Option : créer une skill avec `user-invocable: false`. |
| `.cursor/rules/rule.mdc` type Manual (`@ruleName`) | `.claude/rules/rule.md` avec `paths:` très spécifique **ou** skill manuelle | Pas d'équivalent exact de `@ruleName`. Utiliser une skill `/rule-name` pour l'invocation manuelle. |
| Règles dans sous-dossiers (auto-attach) | `.claude/rules/` avec `paths:` correspondants | Claude rules ne s'auto-attachent pas par position dans l'arborescence — utiliser `paths:` explicitement. |

**Procédure de conversion :**
```
.cursor/rules/*.mdc
  ↓ Pour chaque fichier :
  1. Lire le frontmatter YAML
  2. Si alwaysApply: true → .claude/rules/nom.md (sans frontmatter paths)
  3. Si globs défini → .claude/rules/nom.md avec paths: ["<glob>"]
  4. Si Agent Requested → créer .claude/skills/nom/SKILL.md
     avec user-invocable: false et la description
  5. Si Manual → créer .claude/skills/nom/SKILL.md
     avec disable-model-invocation: true
  6. Copier le contenu Markdown (retirer le frontmatter MDC)
```

### 3.2 Cursor Commands → Claude Commands

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| `.cursor/commands/nom.md` | `.claude/commands/nom.md` | OK — format identique. Claude supporte en plus `$ARGUMENTS` pour le paramétrage dynamique. |
| `.cursor/commands/group/sub.md` | `.claude/commands/group/sub.md` | OK — même convention de sous-dossiers. Invocation : `/group:sub`. |

**Bonus à la conversion :** Ajouter `$ARGUMENTS` pour rendre les commandes paramétrables.

### 3.3 Cursor Hooks → Claude Hooks

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| `beforeShellExecution` | `PreToolUse` avec `matcher: "Bash"` | **Gain** : Claude permet un `matcher` regex pour filtrer par commande. |
| `beforeReadFile` | `PreToolUse` avec `matcher: "Read"` | OK. |
| `beforeMCPExecution` | `PreToolUse` avec `matcher: "mcp__.*"` | OK. |
| `afterFileEdit` | `PostToolUse` avec `matcher: "Edit\|Write"` | OK. |
| `beforeSubmitPrompt` | `UserPromptSubmit` | OK. |
| `stop` | `Stop` | OK. |

**Format de conversion :**
```json
// Cursor: .cursor/hooks.json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      { "command": "./scripts/guard.sh" }
    ],
    "afterFileEdit": [
      { "command": "./scripts/format.sh" }
    ]
  }
}

// Claude: .claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "./scripts/guard.sh" }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "./scripts/format.sh" }]
    }]
  }
}
```

**Gains à la conversion :**
- Matchers regex pour cibler des outils/commandes spécifiques
- Hooks `type: prompt` et `type: agent` (évaluation LLM)
- Hooks `type: http` (webhooks)
- Hooks asynchrones (`async: true`)
- Événements supplémentaires : `SessionStart`, `Notification`, `SubagentStart/Stop`, etc.

### 3.4 Cursor MCP → Claude MCP

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| `.cursor/mcp.json` | `.mcp.json` (racine du projet) | Déplacer à la racine et adapter le format si nécessaire. |
| `~/.cursor/mcp.json` (global) | `~/.claude.json` (section mcpServers) | Intégrer dans la config utilisateur Claude. |
| Serveurs stdio | `type: stdio` + `command` + `args` | Format compatible. |
| Serveurs HTTP | `type: http` + `url` | Format compatible. |

### 3.5 `.cursorignore` → `.claudeignore`

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| `.cursorignore` | `.claudeignore` | Renommer le fichier. Même syntaxe gitignore. Claude est plus strict (exclusion garantie vs best-effort Cursor). |
| `.cursorindexingignore` | `.claudeignore` | Fusionner avec `.claudeignore` — Claude n'a qu'un seul fichier d'exclusion. |

### 3.6 @-Mentions → Outils Claude

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| `@File` | Mentionner le chemin dans le prompt ou utiliser l'outil Read | Claude charge les fichiers via des outils, pas via des @-mentions. |
| `@Folder` | Outil Glob ou Bash `ls` | Pas de syntaxe dédiée — l'IA utilise ses outils. |
| `@Codebase` | Outil Grep / Glob / Agent Explore | Pas de recherche vectorielle — recherche textuelle + agents. |
| `@Web` | Outil WebSearch | OK — fonctionnalité équivalente. |
| `@Docs` | Outil WebFetch sur l'URL | **Pas d'indexation persistante** — chaque fetch est ponctuel. |
| `@Git` | Outil Bash (`git log`, `git diff`) | Fonctionnel mais pas intégré nativement — passe par le shell. |
| `@Link` | Outil WebFetch | OK — fonctionnalité équivalente. |
| `@Code` | Outil Grep + Read | Pas de navigation de symboles intégrée — recherche textuelle. |
| `@Lint Errors` | Bash (exécuter le linter) | Pas d'intégration native — exécuter manuellement. |
| `@Recent Changes` | Bash (`git diff`, `git log`) | Pas de vue intégrée — passe par le shell. |
| `@Cursor Rules` / `@ruleName` | Référence `@path` dans CLAUDE.md ou `/skill` | Pas d'invocation manuelle de règle par nom. Utiliser des skills. |

### 3.7 Automations → Hooks + MCP (approximation)

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| Automations (événements Slack, GitHub, etc.) | Hooks `type: http` + serveur MCP externe | **Architecture très différente** : Claude Code est local, pas de cloud. Il faut un serveur intermédiaire (webhook → MCP) pour reproduire le comportement. |
| Background Agents (cloud VMs) | Subagents avec `isolation: worktree` + `background: true` | **Local vs cloud** : les subagents Claude sont locaux. Pas de VMs isolées. Échelle limitée. |
| Memory tool (Automations) | `memory: project` dans frontmatter agent | OK pour la persistance, mais le format et l'API diffèrent. |

### 3.8 Composer / Agent Mode → Modes Claude Code

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| Normal mode (Composer) | Mode par défaut de Claude Code | OK. |
| Agent mode (`Cmd+.`) | Mode par défaut (Claude Code est toujours en mode agent) | Claude Code est nativement agentique — pas besoin de toggle. |
| Inline edit (`Cmd+K`) | Pas d'équivalent direct dans le CLI | Claude Code est un CLI — pas d'édition inline dans l'éditeur (sauf via l'extension VS Code). |

### 3.9 Notepads (déprécié) → Skills ou Rules

| Composant Cursor | Conversion Claude | Limites |
|-----------------|-------------------|---------|
| Notepads (déprécié oct. 2025) | `.claude/skills/notepad-name/SKILL.md` ou `.claude/rules/notepad.md` | Les Notepads étaient des collections de contexte réutilisable — les skills Claude sont l'équivalent le plus proche. |

---

## Annexe A — Matrice de compatibilité résumée

| Concept | Claude → Cursor | Cursor → Claude | Qualité |
|---------|:-:|:-:|---------|
| Instructions système | Oui | Oui | Bonne (format différent) |
| Commandes slash | Oui | Oui | Bonne (perte `$ARGUMENTS` vers Cursor) |
| Skills | Partiel | N/A | Dégradée (perte outils, modèle, isolation) |
| Agents | Partiel | N/A | Très dégradée |
| Hooks | Partiel | Oui | Moyenne (perte matchers, types prompt/http) |
| MCP | Oui | Oui | Excellente |
| Permissions | Partiel | Partiel | Dégradée |
| Mémoire | Non | N/A | Non convertible |
| Plugins | Non | N/A | Non convertible |
| @-Mentions | N/A | Oui | Bonne (via outils) |
| Ignore files | Oui | Oui | Excellente |
| Automations | N/A | Partiel | Très dégradée |

## Annexe B — Glossaire des formats

| Format | Utilisé par | Extension | Structure |
|--------|------------|-----------|-----------|
| MDC | Cursor Rules | `.mdc` | YAML frontmatter + Markdown body |
| Markdown + paths frontmatter | Claude Rules | `.md` | YAML `paths:` + Markdown body |
| SKILL.md | Claude Skills | `.md` | YAML frontmatter riche + Markdown body |
| Agent frontmatter | Claude Agents | `.md` | YAML frontmatter (tools, model, memory, etc.) + Markdown body |
| JSON settings | Les deux | `.json` | Objets JSON imbriqués |
| TOML manifest | StreamTeX profiles | `.toml` | Déclaration de composants par catégorie |
