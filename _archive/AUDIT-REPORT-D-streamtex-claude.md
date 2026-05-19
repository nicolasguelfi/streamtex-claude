# Rapport Agent-D — streamtex-claude (profiles + skills + cheatsheets)

## Résumé

État global : **partiel**. La vague de refonte Wave 3 Phase 5 + Phase 4
non-CE a très largement modernisé le vocabulaire CE et les commandes
stx-block / stx-ce (33 fichiers sur les 36 modifiés). Les remplacements
`patterns → components`, `block-blueprints → reuse-architecture`,
`stx patterns → stx pack/component/ds/kit` sont systématiques dans les
fichiers CE. Cependant **trois zones contiennent encore du contenu legacy
substantiel** : (a) les 4 templates `CLAUDE.md.j2` continuent à exposer
`st_ai_image` / `st_ai_image_widget` comme l'API moderne et le manifest
`stx_manual_deploy` mentionne Render ; (b) le `streamtex-quick-reference`,
`slide-designer`, `slide-reviewer`, `project-architect`, `course.md` et
`structure-architect` (CE) gardent les sections « Blueprint », « Pattern
awareness », `# @pattern:`, ou des exemples `st_ai_image` ; (c) les
cheatsheets partagées `streamtex_cheatsheet_en.md` et `presentation_*` ont
encore des sections AI image qui documentent l'API supprimée. Les 2
fichiers modifiés non anticipés (`stx-ce/plan.md`, `stx-ce/prototype.md`)
sont propres.

## Périmètre vérifié

- **D1** — 4 templates CLAUDE.md.j2 (`documentation`, `library`,
  `presentation`, `project`).
- **D2** — 8 agents CE, 7 skills CE, 2 templates CE.
- **D3** — 3 agents designer, 1 skill (streamtex-quick-reference),
  1 template (course.md), 4 commandes stx-block (`audit`, `init`, `new`,
  `update`).
- **D4** — 5 fichiers partagés (`streamtex_cheatsheet_en.md`,
  `presentation_cheatsheet_en.md`, `ce_cheatsheet_en.md`, `stx-guide.md`,
  `stx-import/marp.md`).
- **D5** — `cursor/PLAN-generate-cursor.md`.
- **Bonus** — `git diff --stat` complet (36 fichiers), coverage table
  fournie.

### Tableau de couverture des fichiers modifiés

| # | Fichier modifié | Item plan | Statut |
|---|-----------------|-----------|--------|
| 1 | `cursor/PLAN-generate-cursor.md` | D5 | OK |
| 2 | `profiles/presentation/overlay/CLAUDE.md.j2` | D1 | partiel (residual `st_ai_image*`) |
| 3 | `profiles/project/CLAUDE.md.j2` | D1 | partiel (Render mention + `st_ai_image*`) |
| 4-11 | `profiles/project/ce/agents/{audience-advocate,content-strategist,format-explorer,learnings-researcher,prototype-designer,structure-architect,style-consistency-checker,visual-reviewer}.md` | D2 | mostly OK ; `structure-architect` blueprint résidus |
| 12-18 | `profiles/project/ce/skills/{ce-assess,ce-compound,ce-fix,ce-integrate,ce-plan,ce-produce,ce-prototype}.md` | D2 | partiel (`ce-integrate` legacy presets + typo « packsitory » ; `ce-assess` Render dans R14) |
| 19-20 | `profiles/project/ce/templates/{master-plan,prototype-report}.md` | D2 | OK |
| 21-24 | `profiles/project/commands/stx-block/{audit,init,new,update}.md` | D3 | partiel (`@pattern:`, `st_ai_image_widget` dans `audit.md` ligne 126) |
| 25-26 | `profiles/project/commands/stx-ce/{plan,prototype}.md` | **non anticipés** | OK (vérifiés en bonus) |
| 27-29 | `profiles/project/designer/agents/{project-architect,slide-designer,slide-reviewer}.md` | D3 | partiel (Blueprint table, `st_ai_image`, `@pattern:`) |
| 30 | `profiles/project/designer/skills/streamtex-quick-reference.md` | D3 | partiel (section `st_ai_image*` intacte ; section « Patterns vs blueprints ») |
| 31 | `profiles/project/designer/templates/course.md` | D3 | partiel (Blueprint pervasif) |
| 32-33 | `shared/commands/stx-guide.md`, `shared/commands/stx-import/marp.md` | D4 | OK (legacy purgé) |
| 34-36 | `shared/references/{ce_cheatsheet_en,presentation_cheatsheet_en,streamtex_cheatsheet_en}.md` | D4 | partiel (sections AI image legacy ; `monties_color` ligne 659 ; `Render` ligne 214/2268 dans `streamtex_cheatsheet`) |

**Files modifiés non anticipés par le plan** : 2 commandes
`profiles/project/commands/stx-ce/plan.md` et `.../prototype.md`. Toutes
deux propres (`block-blueprints → reuse-architecture`, `patterns → components`).
Aucun fichier modifié n'a échappé à l'audit.

## Constat

### D1 — Profile overlays CLAUDE.md.j2

**Note de migration `/stx-pattern:*` removed** : présente et conforme
dans les 4 templates :
- `documentation/overlay/CLAUDE.md.j2:156-157`
- `library/overlay/CLAUDE.md.j2:124-125`
- `presentation/overlay/CLAUDE.md.j2:129-130`
- `project/CLAUDE.md.j2` indirect (renvoie vers `reuse-architecture` skill)

**Skill `reuse-architecture` référencé** : oui dans les 4 templates.

**Aucune instruction de lire `streamtex-patterns/` ou
`_pattern_library`** : confirmé.

**Mais** : 3 templates exposent encore les APIs supprimées en 0.7.2 :
- `documentation/overlay/CLAUDE.md.j2:56-59` : décrit `st_ai_image()`
  et `st_ai_image_widget()` comme partie active de la « Media & Visual »
  surface. Ligne 57 dit que `st_image(editable=True)` « replaces
  st_ai_image for new code » — formulation correcte mais lignes 56/59
  ne le retirent pas du catalogue.
- `presentation/overlay/CLAUDE.md.j2:62-63` : idem, sans mention de
  remplacement.
- `project/CLAUDE.md.j2` : ne liste pas `st_ai_image` (bon) mais ligne
  103 mentionne `stx_manual_deploy/blocks/ — deployment (Docker, Render,
  CI/CD)` — Render purge incomplète.

### D2 — CE workflows

**Aucune occurrence** de `streamtex-patterns`, `_pattern_library`,
`/stx-pattern:*` ou `stx patterns` dans les 17 fichiers CE en scope
(grep exhaustif fait).

**Vocab `capture` / `promote` ↔ `stx component new/promote`** :
- `ce-prototype.md:95` : « runs `/stx-component:new --from <pilot_block>` »
  — utilise la commande slash `/stx-component:` (qui existe) ; mais le
  flag `--from` n'est pas une convention CLI standard et `stx component
  new` (sans le slash colon) serait plus aligné avec le PLAN A3.
- `ce-compound.md:101` : même schéma `/stx-component:new --from <block>`.
- `ce-integrate.md:31` : `stx component promote <name> --to=<pack>` ✓
  (forme CLI propre, kebab attendu).

**Résidus legacy détectés** :

1. `profiles/project/ce/agents/structure-architect.md:41-42` :
   « Map content to blocks using **blueprints catalog** » et « For each
   section, select appropriate **block blueprints** » + ligne 86 dans
   le template output : colonne `| Block | Blueprint | Content Summary
   | Complexity | Source |`. Vocabulary `block-blueprints` legacy non
   remplacée alors que la lecture en ligne 18 pointe bien vers
   `reuse-architecture`.

2. `profiles/project/ce/skills/ce-integrate.md` :
   - Ligne 3 : « **and patterns promoted from the local catalog to the
     shared `streamtex-design` packsitory** » — typo `packsitory`
     (devait être `repository`). Et conserve `patterns promoted`.
   - Ligne 93 sous-section « 4d. Pattern Promotion to Shared Catalog »
     reste sur « Pattern ».
   - Lignes 95-103 : utilisent encore `pattern file`, `pattern_name`,
     `pattern's intent`.
   - Ligne 100 : « Copy the pattern file into the appropriate **preset
     folder (`core/`, `slides/`, `docs/`, or `projects/<X>/`)** of the
     shared repo » — les dossiers `core/`, `slides/`, `docs/`,
     `presets/`, `projects/` ont été supprimés de `streamtex-design`
     en 0.2.1 (cf. Agent-C C2). Cette instruction est **techniquement
     fausse** maintenant.

3. `profiles/project/ce/skills/ce-assess.md:72` (et les 3 templates
   `assess-{create,import,improve}.md` lignes ~53-64) : « R14:
   Deployment target (local, **Render**, Hetzner, other) » — Render
   reste listé alors qu'il est supprimé en 0.7.x.

4. `profiles/project/ce/skills/ce-produce.md:66,88` : « Use
   `st_ai_image(prompt)` for standalone generated images » et « Verify
   all `st_ai_image()` and `st_image(editable=True)` calls render
   without errors » — API supprimée 0.7.2.

5. `profiles/project/ce/agents/prototype-designer.md` : conserve la
   terminologie « pattern strategy », « pattern file », `reuse_as_is /
   reuse_adapted / create_new / ad_hoc `, output table colonne `Pattern`.
   Discutable : le PLAN n'interdit pas le terme « pattern » comme nom
   d'archétype visuel ; mais combiné au mapping vers
   `master-plan.yaml -> components.applied` (renommé via diff) ça crée
   une dissonance entre le code mappé et le vocab agent.

### D3 — Designer profile

**`TOCConfig(numbering=NumberingMode.NONE, ...)`** :
- `streamtex-quick-reference.md:207` : ✓ exact diff applied.
  *Minor cosmetic* : `NumberingMode` n'est pas dans l'import ligne 205
  (`from streamtex import st_book, TOCConfig, MarkerConfig, BannerConfig`).
- `course.md:13` : `NumberingMode.SIDEBAR_ONLY` ✓.

**Résidus `block-blueprints` (legacy)** :

6. `profiles/project/designer/agents/project-architect.md` : lignes
   96-111 « Block-to-blueprint mapping » avec table 10 blueprints
   numérotés (1 — Title, …, 10 — Conclusion) ; lignes 119, 121 « add
   transition blocks (Blueprint 2) » et « always end with a Blueprint
   10 » ; ligne 134 output template colonne `Blueprint`. La lecture
   ligne 18 pointe bien vers `reuse-architecture` mais le corps du
   document garde la nomenclature numérotée des blueprints supprimés.

7. `profiles/project/designer/templates/course.md` : Lignes 35-81
   utilisent intensivement « Blueprint 1 », « Blueprint 3 », jusqu'à
   « Blueprint 11 ». Section « Blueprint mapping » (50-65) est une
   table de mapping pédagogique → blueprint. Les blueprints numérotés
   n'existent plus.

8. `profiles/project/designer/skills/streamtex-quick-reference.md` :
   - Lignes 110-128 « AI Image Generation — `st_ai_image()` /
     `st_ai_image_widget()` » → section entière documente l'API
     supprimée. Le diff ne touche pas cette section.
   - Lignes 314-325 « Patterns vs blueprints » : section conceptuelle
     qui définit blueprint vs pattern → tout le vocabulaire legacy.
   - Lignes 304-317 « Slash commands » : table avec `/stx-component:list`,
     `/stx-component:show`, `/stx-component:new`, `/stx-component:validate`
     décrits comme listant / créant des **« patterns »**, pas des
     **components**.

9. `profiles/project/designer/agents/slide-designer.md` :
   - Ligne 57 : `st_ai_image(prompt, ...)` recommandé pour génération
     d'images. API supprimée 0.7.2.
   - Lignes 78-92 « Patterns awareness (MANDATORY) » : section entière
     parle de « pattern file », « # @pattern:` annotation », « INVARIANTS »
     en code legacy.

10. `profiles/project/designer/agents/slide-reviewer.md:66-79` :
    « Pattern compliance » : `# @pattern: <name>` annotation, INVARIANTS
    section, `/stx-component:new` (la commande slash existe mais le
    contexte vise la promotion de patterns). Le diff change
    `stx patterns sync → stx pack sync` ; le reste de la section
    reste sur le vocab pattern.

**Commands `stx-block`** :

11. `profiles/project/commands/stx-block/audit.md` :
    - Ligne 126 : `st_ai_image_widget()` — directive à vérifier que
      `editable` n'est pas passé. La directive est correcte
      historiquement mais l'API est supprimée 0.7.2.
    - Lignes 128-142 : sections `Pattern Compliance` et `Pattern
      compliance checks` parlent toujours de `@pattern:` annotations
      et `INVARIANTS`. Le diff a remplacé une mention `stx patterns
      sync → stx pack sync`.

12. `profiles/project/commands/stx-block/update.md:128-135` : section
    documentant `st_ai_image_widget(...)` recommandé pour les requêtes
    « image AI editable/modifiable » ; reste à mettre à jour vers
    `st_image(prompt=..., editable=True)`.

13. `profiles/project/commands/stx-block/init.md` et `new.md` :
    rafraîchis correctement (diff propre) — pointent vers
    `reuse-architecture` et `stx component list`.

### D4 — Shared cheatsheets

**`stx-guide.md`** : Render et `stx patterns` purgés (diff sur 48
lignes). ✓
**`stx-import/marp.md`** : note D19 transformée en bloc opérationnel
recommandant `.claude/custom/skills/import-<pack>-mapping.md`. ✓
**`ce_cheatsheet_en.md`** : 1 ligne diff (patterns → components mapping). ✓

**`presentation_cheatsheet_en.md`** : section « Slides patterns
(catalog) » → « Slide components (catalog) » avec table
`ptn_* → <name>`. ✓ Mais :

14. `presentation_cheatsheet_en.md:222-232` (section AI Image
    Generation hors-diff) : conserve `st_ai_image(...)` et
    `st_ai_image_widget(...)` comme API recommandée — non traitée par
    cette série.
15. `presentation_cheatsheet_en.md:450` : « `/stx-block:new` | Create
    block from blueprint » — usage legacy block-blueprint.

**`streamtex_cheatsheet_en.md`** : section « Patterns » renommée
« Reuse architecture (packs / components / DS / kits) » avec CLI
modernisée. ✓ Mais :

16. `streamtex_cheatsheet_en.md:186-214` : section AI Image complète
    documente `st_ai_image`, `st_ai_image_widget`, `generate_image`
    comme API recommandée + ligne 214 mention « API keys via
    environment variables (`.env` or **Render**) ».
17. `streamtex_cheatsheet_en.md:659` : commentaire de signature
    `st_book(...)` : « `monties_color=None, # Legacy — use
    banner=BannerConfig(...) instead` ». Le PLAN A1 dit que
    `monties_color` a été supprimé de `st_book()` — la signature
    ne doit plus mentionner cet argument.
18. `streamtex_cheatsheet_en.md:2268` : `stx deploy env-sync # sync
    env vars from render.yaml to Render services` — Render purge
    incomplète.

### D5 — Cursor PLAN-generate-cursor.md

Diff = 1 ligne (`skill-block-blueprints.mdc` retiré du tree). ✓
Grep `blueprint|/stx-pattern:|streamtex-patterns|_pattern_library|
stx patterns|st_ai_image|monties_color|numerate_titles` retourne **0
match**. ✓

## Anomalies détectées

1. **MAJEUR** — `profiles/documentation/overlay/CLAUDE.md.j2:56-59` :
   `st_ai_image()` et `st_ai_image_widget()` documentés comme API
   active dans le panneau « Media & Visual ». L'API a été supprimée
   en streamtex 0.7.2 (cf. plan A1). Le profil documentation est lu
   par tous les rédacteurs de manuels.

2. **MAJEUR** — `profiles/presentation/overlay/CLAUDE.md.j2:62-63` :
   idem `st_ai_image()` / `st_ai_image_widget()` actifs dans le
   panneau Media & Visual sans note de suppression.

3. **MAJEUR** — `profiles/project/CLAUDE.md.j2:103` : « stx_manual_deploy/
   blocks/ — deployment (Docker, **Render**, CI/CD) ». Render purgé
   du manuel deploy (cf. B3) mais cette description périmée subsiste
   ici. Doit devenir « (Docker, Hetzner/Coolify, CI/CD) ».

4. **MAJEUR** — `profiles/project/ce/skills/ce-integrate.md:100` :
   instruction « Copy the pattern file into the appropriate preset
   folder (`core/`, `slides/`, `docs/`, or `projects/<X>/`) of the
   shared repo ». Ces dossiers ont été supprimés de `streamtex-design`
   en 0.2.1 (cf. plan C2). L'instruction conduit à un échec en cas
   d'exécution.

5. **MAJEUR** — `profiles/project/ce/skills/ce-integrate.md:3` :
   « and patterns promoted from the local catalog to the shared
   `streamtex-design` **packsitory** » : (a) typo `packsitory`,
   (b) `patterns` au lieu de `components` alors que tout le reste
   du fichier a migré.

6. **MAJEUR** — `profiles/project/ce/skills/ce-produce.md:66,88` :
   directives explicites « Use `st_ai_image(prompt)` for standalone
   generated images » et vérification « `st_ai_image()` and
   `st_image(editable=True)` calls render without errors ». Génère
   du code qui ne fonctionne plus.

7. **MAJEUR** — `profiles/project/designer/skills/streamtex-quick-reference.md:110-128` :
   section « AI Image Generation — `st_ai_image()` /
   `st_ai_image_widget()` » entièrement legacy. C'est le skill chargé
   par tous les agents designer / slide-designer.

8. **MAJEUR** — `profiles/project/designer/agents/slide-designer.md:57` :
   « use `st_ai_image(prompt, ...)` to generate and display the image
   directly » — API supprimée, le slide-designer va générer du code
   cassé.

9. **MAJEUR** — `shared/references/streamtex_cheatsheet_en.md:186-214` :
   section AI Image complète documente l'API supprimée + ligne 214
   référence Render. C'est la cheatsheet partagée principale,
   re-synchronisée vers les projets via `stx claude update`.

10. **MAJEUR** — `shared/references/streamtex_cheatsheet_en.md:659` :
    signature `st_book(monties_color=None, # Legacy — use
    banner=BannerConfig(...))` contradit la suppression A1
    (`monties_color` retiré de `st_book`).

11. **MAJEUR** — `shared/references/streamtex_cheatsheet_en.md:2268` :
    « stx deploy env-sync — sync env vars from render.yaml to Render
    services ». La commande `stx deploy env-sync` reste documentée
    dans la cheatsheet partagée alors que Render est purgé du workflow.

12. **MAJEUR** — `shared/references/presentation_cheatsheet_en.md:222-232` :
    section AI Image montre encore `st_ai_image()` /
    `st_ai_image_widget()` comme API recommandée pour les slides.

13. **MAJEUR** — `profiles/project/commands/stx-block/audit.md:126` :
    checklist `--target presentation` valide encore l'usage de
    `st_ai_image_widget()` (avec garde sur le kwarg `editable`).
    L'audit va ignorer un usage d'API supprimée.

14. **MAJEUR** — `profiles/project/commands/stx-block/update.md:128-135` :
    le workflow `add block` répond aux requêtes « interactive AI
    image » par `st_ai_image_widget(...)`. Génère un appel à une
    fonction supprimée.

15. **MINEUR** — `profiles/project/ce/agents/structure-architect.md:41-42, 86` :
    « blueprints catalog » et « select appropriate block blueprints » +
    colonne `| Blueprint |` dans la table output. Doit migrer vers
    « components catalog » et colonne `| Component |`.

16. **MINEUR** — `profiles/project/designer/agents/project-architect.md` :
    section « Block-to-blueprint mapping » (96-111), Anti-patterns
    « Blueprint 2 / Blueprint 10 » (119, 121), output template colonne
    `Blueprint` (134). Cohabite avec la modernisation `kit install`
    réalisée juste au-dessus (74-94).

17. **MINEUR** — `profiles/project/designer/templates/course.md:33-81` :
    nomenclature « Blueprint 1 … Blueprint 11 » pervasive. Doit
    devenir « Component <name> ».

18. **MINEUR** — `profiles/project/designer/skills/streamtex-quick-reference.md:314-325` :
    section « Patterns vs blueprints » (Blueprint = whole block type,
    Pattern = composition primitive). Vocabulaire legacy contradictoire
    avec `reuse-architecture` qui parle de granularités
    `primitive / composition / block`.

19. **MINEUR** — `profiles/project/designer/agents/slide-designer.md:78-92`,
    `slide-reviewer.md:66-79`, `commands/stx-block/audit.md:128-142` :
    sections « Pattern compliance » / « Patterns awareness » avec
    annotation `# @pattern: <name>`. Si l'annotation `@pattern:` est
    toujours supportée par streamtex 0.7.x (à vérifier côté Agent-A),
    ces sections sont OK ; sinon legacy.

20. **MINEUR** — `profiles/project/ce/agents/prototype-designer.md` :
    output « pattern strategy » avec colonne `Pattern` dans la table.
    Cohérence avec `ce-prototype.md` qui mappe vers
    `components.applied` à confirmer.

21. **MINEUR** — `profiles/project/ce/skills/ce-assess.md:72` +
    `templates/assess-{create,import,improve}.md` : « R14: Deployment
    target (local, **Render**, Hetzner, other) ». Render listé comme
    option valide.

22. **MINEUR** — `profiles/project/ce/skills/ce-prototype.md:95`,
    `ce-compound.md:101` : `/stx-component:new --from <block>` —
    forme `--from` non standard (à vérifier dans CLI A3).

23. **MINEUR** — `profiles/project/designer/skills/streamtex-quick-reference.md:205-207` :
    `NumberingMode.NONE` utilisé en valeur sans `NumberingMode` dans
    l'import ligne 205 (`from streamtex import st_book, TOCConfig,
    MarkerConfig, BannerConfig`). Cosmétique.

24. **MINEUR** — `shared/references/presentation_cheatsheet_en.md:450`,
    `shared/commands/stx-guide.md:85, 400, 414` : usages de
    « blueprint » au sens des templates `/stx-block:init`. Ambigu
    avec la nouvelle notion de **project blueprint** définie dans
    `shared/skills/reuse-architecture.md` (markdown blueprint inside
    a pack). À clarifier ou renommer.

## Propositions de remédiation

**Bloc 1 — AI image API (anomalies 1, 2, 6, 7, 8, 9, 12, 13, 14)** :
réécrire chaque section « AI Image » dans :
- 4 j2 templates
- streamtex-quick-reference
- slide-designer (ligne 57)
- streamtex_cheatsheet_en (186-214)
- presentation_cheatsheet_en (222-232)
- commands stx-block/audit.md ligne 126
- commands stx-block/update.md ligne 128-135
- ce-produce.md lignes 66, 88
pour utiliser exclusivement
`st_image(prompt=..., editable=True, name=...)` (paramètre `ai_size=`
et non `size=`, cf. plan B2). Mentionner `st_ai_image` / widget
**uniquement** comme « supprimé en 0.7.2, voir CHANGELOG » s'il faut
une note de migration.

**Bloc 2 — Render purge (anomalies 3, 11, 21)** :
- `project/CLAUDE.md.j2:103` → « (Docker, Hetzner/Coolify, CI/CD) ».
- `streamtex_cheatsheet_en.md:2268` → supprimer la commande
  `stx deploy env-sync` ou la marquer legacy.
- `ce-assess.md:72` + templates `assess-*.md` R14 → retirer Render des
  options.

**Bloc 3 — `monties_color` (anomalie 10)** :
- `streamtex_cheatsheet_en.md:659` → retirer cet argument du bloc de
  signature `st_book()` (suppression confirmée en 0.7.2).

**Bloc 4 — block-blueprints legacy (anomalies 15, 16, 17, 18)** :
- `structure-architect.md` : « blueprints catalog » → « components
  catalog » ; table output `| Component |` au lieu de `| Blueprint |`.
- `project-architect.md` : remplacer les 10 blueprints numérotés par
  un mapping `archetype → component` (`title_slide`, `slide_heading`,
  `feature_walkthrough`, etc.). Anti-patterns référencent
  « Blueprint 2 / 10 » → remplacer par nom de composant.
- `course.md` : refonte du mapping pédagogique → composants
  (`title_slide`, `slide_heading`, `card_grid`, `feature_walkthrough`,
  `takeaways`, etc.) avec une table reconstruite.
- `streamtex-quick-reference.md` section « Patterns vs blueprints »
  → supprimer ; remplacer par un renvoi à `reuse-architecture` skill
  (granularités primitive / composition / block).

**Bloc 5 — preset folders supprimés (anomalie 4)** :
- `ce-integrate.md:100` : retirer la mention des dossiers `core/`,
  `slides/`, `docs/`, `presets/`, `projects/<X>/` ; remplacer par
  « place the component in the target pack's `components/` directory »
  (cf. structure post-0.2.1 du pack `streamtex-design`).

**Bloc 6 — Typo + vocab ce-integrate (anomalie 5)** :
- `ce-integrate.md:3` : corriger `packsitory → repository`, remplacer
  « patterns promoted » par « components promoted ».

**Bloc 7 — Pattern annotations / vocab `@pattern:` (anomalie 19)** :
décision à valider avec Agent-A : si `# @pattern:` est encore
supporté en 0.7.x, garder. Sinon, remplacer par `# @component:` ou
supprimer la sémantique d'annotation et passer par mapping
`master-plan.yaml -> components.applied`.

**Bloc 8 — Slash command form (anomalie 22)** :
remplacer `/stx-component:new --from <block>` par la forme CLI
documentée dans le plan A3 (`stx component new <name>` ou
`/stx-component:new`). À aligner avec la sortie de l'audit Agent-A
qui confirme la surface CLI.

**Bloc 9 — Cosmétique (anomalies 20, 23, 24)** :
- ajouter `NumberingMode` à l'import de
  `streamtex-quick-reference.md:205`.
- harmoniser le vocabulaire « project blueprint » vs « block
  template » dans stx-guide.md et presentation_cheatsheet (clarifier
  que le « project blueprint » 0.7.x est un markdown dans un pack,
  pas un type de bloc).

## Vérifications non-faites / hors-périmètre

- **`profiles/documentation/overlay/developer/skills/coherence-checks.md`**
  et **`profiles/library/overlay/developer/skills/architecture.md`**
  contiennent encore beaucoup de références `st_ai_image`,
  `st_ai_image_widget`, `render-deploy.yml`, `Render deploy:` — **non
  modifiés dans cette série**, donc hors périmètre direct, mais à
  flagger comme dette pour une vague future.
- **`profiles/presentation/overlay/designer/presentation/skills/*.md`**
  (skills slide-design-rules, presentation-design-rules,
  survey-chart-conversion) : références `st_ai_image` dans skills non
  modifiés.
- **`shared/references/coding_standards.md`** non listé au plan D4
  mais contient `st_ai_image`, `monties_color` (lignes 89, 332, 834).
  Probablement géré par Agent-B mais à vérifier.
- **`shared/references/streamtex_cheatsheet_en.md`** : audit ciblé sur
  les sections AI / Render / monties_color / TOCConfig. Pas de
  diff systématique vs `streamtex-docs/references/streamtex_cheatsheet_en.md`
  (le plan dit que ce sync se fait via `stx claude update`).
- **Validation des slash commands** : le rapport ne vérifie pas que
  les commandes `/stx-component:new`, `/stx-component:list`, etc.
  sont réellement définies dans `profiles/project/commands/stx-component/`
  ou équivalent. À cross-checker avec Agent-A (A3).
- **`@pattern:` annotation** : on suppose qu'elle est encore un
  protocole supporté (lien avec `streamtex` lib). Si Agent-A confirme
  qu'elle a été supprimée, les anomalies 19 deviennent MAJEURES.

---

## Synthèse 200 mots

Le repo `streamtex-claude` a reçu 36 fichiers de modifications
non-committées qui modernisent **systématiquement** le vocabulaire
CE (`patterns → components`, `block-blueprints → reuse-architecture`,
`stx patterns → stx pack/component/ds/kit`) et purgent les commandes
slash `/stx-pattern:*`. Tous les fichiers diff-modifiés ont été
audités, dont 2 commandes `stx-ce/{plan,prototype}.md` que le plan
n'avait pas anticipées (toutes deux propres). Cependant **3 zones de
dette legacy substantielle** subsistent : (1) les sections AI Image
des 2 cheatsheets partagées, du quick-reference, du slide-designer,
des commandes stx-block et de ce-produce documentent encore
`st_ai_image()` / `st_ai_image_widget()` comme l'API recommandée
alors que ces fonctions ont été supprimées en 0.7.2 ; (2) les
templates `course.md`, `project-architect.md` et `structure-architect.md`
gardent la nomenclature « Blueprint 1 / 2 / … / 11 » périmée ; (3)
`ce-integrate.md` contient une instruction qui pointe vers des
dossiers (`core/`, `slides/`, `docs/`, `presets/`, `projects/`)
supprimés de `streamtex-design` en 0.2.1, plus un typo « packsitory ».
Mineurs : 3 mentions Render résiduelles (R14 deployment target,
`stx deploy env-sync`, `project/CLAUDE.md.j2:103`), 1 signature
`st_book` qui mentionne `monties_color`, et le vocabulaire « project
blueprint » vs « block template » ambigu dans stx-guide. État
global : **partiel** — la migration vocabulaire CE est nette mais
la couche AI Image et les blueprints numérotés n'ont pas été traités
par cette série.
