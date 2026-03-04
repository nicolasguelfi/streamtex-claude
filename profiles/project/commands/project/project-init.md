# /project:project-init — Initialiser un projet StreamTeX complet

Arguments: $ARGUMENTS (description en langage naturel du projet souhaite)

## Declencheur

L'utilisateur decrit un projet en langage naturel. Exemples :

- `"cours Docker pour debutants, 8 slides, style presentation sombre"`
- `"documentation technique API REST, 12 sections, avec exemples de code"`
- `"portfolio de projets recherche, 5 projets, mode collection"`

## Lectures obligatoires AVANT generation

1. `.claude/references/coding_standards.md`
2. `.claude/references/streamtex_cheatsheet_en.md`
3. `.claude/designer/skills/visual-design-rules.md`
4. `.claude/designer/skills/style-conventions.md`
5. `.claude/designer/skills/block-blueprints.md`
6. `.claude/designer/agents/project-architect.md`
7. `book.py` existant (si le projet a deja ete scaffold)

## Workflow

### Etape 1 : Analyser la demande

Extraire de la description de l'utilisateur :

- **Type** : presentation | documentation | collection
- **Nombre de sections/slides** : N
- **Theme visuel** : sombre (dark) | clair (light) | custom
- **Fonctionnalites** : TOC, pagination, banner, export, interactivite
- **Public cible** : amphitheatre (gros texte, `s.Large` min) | ecran (texte normal, `s.large`)

Si des informations manquent, utiliser les valeurs par defaut :
- Type : presentation
- Theme : dark
- TOC : `numbering=NumberingMode.SIDEBAR_ONLY, sidebar_max_level=2` (numerotation dans le sidebar seulement, jusqu'au niveau 2)
- Sidebar : `initial_sidebar_state="expanded"` (toujours ouvert par defaut)
- Pagination : oui
- Public : ecran

### Etape 2 : Proposer un plan

Adopter le role de **Project Architect** (`.claude/designer/agents/project-architect.md`)
et proposer a l'utilisateur :

1. **Liste des N blocks** avec noms, blueprints associes, et descriptions
2. **Structure du book.py** (pagination, TOC, banner, marker)
3. **Palette de couleurs** proposee
4. **Fonctionnalites activees**

Utiliser le format de sortie defini dans `project-architect.md`.

**Demander confirmation avant de generer.** Ne jamais generer sans accord explicite.

### Etape 3 : Generer les fichiers

Pour chaque block :

1. Creer `blocks/bck_NN_<nom>.py` avec :
   - Docstring descriptive du contenu du block
   - Imports conformes a `coding_standards.md` :
     ```python
     from streamtex import *
     from streamtex.styles import Style as ns
     from streamtex.enums import Tags as t, ListTypes as lt
     from custom.styles import Styles as s
     ```
   - `BlockStyles` class avec styles adaptes au theme et au public cible
   - `bs = BlockStyles` alias
   - `def build()` implementant la structure du blueprint choisi
   - Contenu placeholder structure (pas de Lorem Ipsum) :
     - Titres descriptifs du sujet reel
     - Bullet points avec `"[A completer : description du contenu attendu]"`
     - Emplacements d'images avec commentaires `# TODO: ajouter image`
   - `toc_lvl` sur le titre principal pour le sommaire

2. Mettre a jour `book.py` :
   - Importer `blocks` (registry)
   - Configurer `st.set_page_config(initial_sidebar_state="expanded")`
   - Configurer `TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY, sidebar_max_level=2, search=True)`
   - Configurer `st_book()` avec la liste des blocks dans l'ordre
   - Activer les fonctionnalites choisies (pagination, TOC, banner, marker)

3. Adapter `custom/styles.py` :
   - Definir la palette de couleurs choisie
   - Creer les styles project-level (titles, containers, colors)

4. Adapter `custom/themes.py` si le theme n'est pas le defaut

5. Mettre a jour `.streamlit/config.toml` si necessaire (theme dark/light)

### Etape 4 : Valider

- Verifier que tous les blocks ont une fonction `build()`
- Verifier que `book.py` reference tous les blocks generes
- Verifier la coherence des styles (pas de style reference non defini)
- Afficher un resume des fichiers generes :

```
Fichiers generes :
  book.py                          (mis a jour)
  custom/styles.py                 (mis a jour)
  blocks/bck_01_titre.py           (cree)
  blocks/bck_02_intro.py           (cree)
  ...
  blocks/bck_NN_conclusion.py      (cree)

Prochaines etapes :
  1. Remplir le contenu des blocks (remplacer les "[A completer : ...]")
  2. Ajouter les images dans static/images/
  3. Tester : uv run streamlit run book.py
  4. Utiliser /designer:slide-audit pour verifier la conformite
```

## Regles de generation

- Tous les blocks suivent le pattern `BlockStyles` + `build()`
- Les noms de styles sont en anglais (`style-conventions.md`)
- Les tailles de texte respectent le public cible :
  - Amphitheatre : `s.Large` (48pt) minimum pour le corps
  - Ecran : `s.large` (32pt) pour le corps
- Chaque block a un `toc_lvl` pour le sommaire
- Le contenu est du placeholder structure (pas du Lorem Ipsum)
- Les blocks sont numerotes : `bck_01_`, `bck_02_`, etc.
- Pas de raw HTML/CSS — utiliser uniquement les fonctions `stx.*`
- Pas de hardcoded black/white — utiliser le systeme de styles

## Contraintes

- Suivre TOUTES les regles de CLAUDE.md
- Maximum 15 blocks par projet (sinon, suggerer une collection)
- Toujours inclure un block de titre (Blueprint 1) et un de conclusion (Blueprint 10)
- Si le projet est deja scaffold (`book.py` existe), adapter plutot que re-creer
