# /project:project-customize — Personnaliser un projet StreamTeX

Arguments: $ARGUMENTS (description des changements souhaites en langage naturel)

## Declencheur

L'utilisateur decrit les changements de personnalisation souhaites. Exemples :

- `"passer en theme clair avec palette verte"`
- `"ajouter un TOC sidebar avec numerotation"`
- `"activer l'export HTML et le mode banner"`
- `"adapter pour projection en amphitheatre (gros texte)"`
- `"changer la palette en bleu et orange, ajouter la pagination"`

## Lectures obligatoires

1. `book.py` — configuration actuelle du projet
2. `custom/styles.py` — palette et styles actuels
3. `custom/themes.py` — theme actuel (si le fichier existe)
4. `.streamlit/config.toml` — configuration Streamlit actuelle
5. `.claude/references/coding_standards.md`
6. `.claude/designer/skills/style-conventions.md`

## Domaines de personnalisation

### 1. Theme et couleurs

**Fichiers concernes** : `custom/styles.py`, `custom/themes.py`, `.streamlit/config.toml`

- Palette de couleurs : `primary`, `accent`, `highlight`, `success`, `muted`
- Theme Streamlit : dark / light (dans `.streamlit/config.toml`)
- Couleurs de fond des blocks (via `Style.create()`)
- Couleurs d'accent pour les titres, liens, bullets

### 2. Typographie

**Fichiers concernes** : `custom/styles.py`, tous les blocks

- Tailles de police : ecran (`s.large` corps) vs amphitheatre (`s.Large` corps)
- Hierarchie des titres : `s.huge` > `s.Large` > `s.large`
- Style des bullets dans les listes
- Police personnalisee (si demandee)

### 3. Navigation

**Fichiers concernes** : `book.py`

- **TOC** : on/off, mode `numbering=NumberingMode.SIDEBAR_ONLY` (defaut), `sidebar_max_level=2` (defaut)
- **Sidebar** : `initial_sidebar_state="expanded"` (toujours ouvert par defaut)
- **Pagination** : on/off (paginate=True/False dans st_book)
- **Marker** : on/off, touches de navigation (PageUp/PageDown par defaut)
- **Banner** : on/off, configuration (titre, logo, couleur)

### 4. Fonctionnalites

**Fichiers concernes** : `book.py`, `custom/styles.py`

- **Export HTML** : on/off (ExportConfig dans book.py)
- **Inspector** : on/off (mode debug live)
- **Zoom** : on/off, valeur par defaut
- **Mode collection** : conversion projet → collection (ajout collection.toml)

## Workflow

### Etape 1 : Lire la configuration actuelle

Lire les fichiers du projet pour comprendre l'etat actuel :
- Quel theme est utilise ?
- Quelles fonctionnalites sont activees ?
- Quelle palette de couleurs ?
- Quel public cible ?

### Etape 2 : Identifier les changements demandes

Parser la description de l'utilisateur et determiner :
- Quels domaines sont concernes (theme, typo, navigation, fonctionnalites)
- Quels fichiers doivent etre modifies
- Y a-t-il des conflits avec la configuration actuelle ?

### Etape 3 : Proposer les modifications

Afficher un resume clair des changements proposes :

```
Changements proposes :

1. custom/styles.py
   - primary : #1a1a2e → #2d5016 (vert fonce)
   - accent  : #e94560 → #4caf50 (vert)
   + highlight : #81c784 (vert clair) [nouveau]

2. .streamlit/config.toml
   - base = "dark" → base = "light"

3. book.py
   + toc_config = TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY, sidebar_max_level=2, search=True)
   + initial_sidebar_state="expanded"
   + paginate = True

Fichiers touches : 3
Blocks a mettre a jour : 0
```

**Demander confirmation avant d'appliquer.**

### Etape 4 : Appliquer les modifications

Modifier les fichiers dans l'ordre :
1. `custom/styles.py` (palette, styles project-level)
2. `custom/themes.py` (theme si necessaire)
3. `.streamlit/config.toml` (theme Streamlit)
4. `book.py` (navigation, fonctionnalites)
5. Blocks individuels (seulement si les tailles de police changent)

### Etape 5 : Valider

- Verifier qu'aucun style reference n'est manquant
- Verifier la coherence entre theme Streamlit et styles custom
- Afficher un resume des modifications appliquees

```
Modifications appliquees :
  custom/styles.py       — palette mise a jour (3 couleurs)
  .streamlit/config.toml — theme passe en light
  book.py                — TOC + pagination actives

Tester : uv run streamlit run book.py
```

## Regles

- Ne JAMAIS supprimer du contenu existant dans les blocks
- Ne modifier les blocks que pour les tailles de police (changement de public cible)
- Toujours utiliser `Style.create()` pour les couleurs, jamais de raw CSS
- Toujours proposer un diff avant d'appliquer
- Si le changement affecte tous les blocks (ex: changement de public), avertir l'utilisateur du nombre de fichiers touches

## Contraintes

- Suivre TOUTES les regles de CLAUDE.md
- Pas de hardcoded black/white — utiliser le systeme de styles
- Pas de raw HTML/CSS
- Noms de styles en anglais uniquement
