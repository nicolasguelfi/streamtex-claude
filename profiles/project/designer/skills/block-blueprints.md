# Block Blueprints — Catalogue de modeles

Ce fichier documente 10 modeles de blocks courants que Claude utilise comme reference
lorsqu'il genere du code via `/designer:block-new` ou `/project:project-init`.

## Comment utiliser

Quand l'utilisateur demande un type de block connu, utiliser le blueprint
correspondant comme base et l'adapter au contexte (sujet, nombre de bullets,
palette de couleurs, public cible).

Les blueprints definissent la **structure** (quels `stx.*` appels, dans quel ordre),
pas le contenu exact. Le contenu est toujours adapte a la demande de l'utilisateur.

---

## Blueprint 1 : Titre (bck_title)

Un slide de titre avec nom du cours/projet, sous-titre, auteur.

**Quand l'utiliser** : premier slide d'une presentation, page d'accueil d'un projet.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_space(size=4)
        st_write(bs.title, "Titre du cours", tag=t.div, toc_lvl="1")
        st_space(size=2)
        st_write(bs.subtitle, "Sous-titre descriptif", tag=t.div)
        st_space(size=3)
        st_write(bs.author, "Auteur — Date", tag=t.div)
```

**Styles typiques** :
- `title` : `s.huge + s.bold + s.center_txt`
- `subtitle` : `s.Large + s.center_txt`
- `author` : `s.large + s.center_txt + s.text.colors.muted`

---

## Blueprint 2 : Section Header (bck_section)

Slide d'introduction de section avec numero et titre.

**Quand l'utiliser** : transition entre les grandes parties d'une presentation.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_space(size=3)
        st_write(bs.section_num, "Section N", tag=t.div)
        st_space(size=1)
        st_write(bs.section_title, "Titre de la section", tag=t.div, toc_lvl="1")
        st_space(size=2)
        st_write(bs.description, "Description courte (1-2 lignes)", tag=t.div)
```

**Styles typiques** :
- `section_num` : `s.huge + s.bold + s.center_txt + s.text.colors.accent`
- `section_title` : `s.LARGE + s.center_txt`
- `description` : `s.large + s.center_txt + s.text.colors.muted`

---

## Blueprint 3 : Contenu textuel (bck_content)

Slide avec titre + bullets. Le pattern le plus courant.

**Quand l'utiliser** : expliquer un concept, lister des points cles.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Titre du sujet", tag=t.div, toc_lvl="2")
        st_space(size=2)
        st_list(
            bs.body,
            items=[
                "Premier point important",
                "Deuxieme point avec detail",
                "Troisieme point concis",
            ],
            list_type=lt.ul,
        )
```

**Styles typiques** :
- `heading` : `s.huge + s.bold`
- `body` : `s.Large` (amphi) ou `s.large` (ecran)

---

## Blueprint 4 : Comparaison 2 colonnes (bck_comparison)

Slide avec 2 colonnes comparant des concepts.

**Quand l'utiliser** : "X vs Y", avantages/inconvenients, avant/apres.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Concept A vs Concept B", tag=t.div, toc_lvl="2")
        st_space(size=2)
        with st_grid([1, 1]):
            with st_block():
                st_write(bs.col_title, "Concept A", tag=t.div)
                st_space(size=1)
                st_list(bs.body, items=["Point 1", "Point 2", "Point 3"], list_type=lt.ul)
            with st_block():
                st_write(bs.col_title, "Concept B", tag=t.div)
                st_space(size=1)
                st_list(bs.body, items=["Point 1", "Point 2", "Point 3"], list_type=lt.ul)
```

**Styles typiques** :
- `heading` : `s.huge + s.bold + s.center_txt`
- `col_title` : `s.Large + s.bold + s.text.colors.accent`
- `body` : `s.large`

---

## Blueprint 5 : Image + Texte (bck_image_text)

Slide avec image a gauche et texte explicatif a droite (ou inversement).

**Quand l'utiliser** : illustrer un concept avec un schema, diagramme, photo.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Titre illustre", tag=t.div, toc_lvl="2")
        st_space(size=2)
        with st_grid([1, 1]):
            st_image("static/images/illustration.png", caption="Description de l'image")
            with st_block():
                st_write(bs.body, "Texte explicatif accompagnant l'image.")
                st_space(size=1)
                st_list(bs.body, items=["Detail 1", "Detail 2"], list_type=lt.ul)
```

**Styles typiques** :
- `heading` : `s.huge + s.bold`
- `body` : `s.large`

---

## Blueprint 6 : Code + Resultat (bck_code_demo)

Slide montrant du code source et son resultat / output.

**Quand l'utiliser** : demo de code, tutoriel technique, exemples de syntaxe.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo : titre", tag=t.div, toc_lvl="2")
        st_space(size=2)
        with st_grid([1, 1]):
            st_code(
                bs.code,
                code="""\
                    # Code source
                    def hello():
                        print("Hello!")
                """),
                language="python",
            )
            with st_block(bs.result_box):
                st_write(bs.body, "Resultat / output ici")
```

**Styles typiques** :
- `heading` : `s.huge + s.bold`
- `code` : style par defaut (responsive)
- `result_box` : fond leger d'accent
- `body` : `s.large`

---

## Blueprint 7 : Timeline / Etapes (bck_timeline)

Slide avec une sequence d'etapes numerotees.

**Quand l'utiliser** : processus, workflow, etapes d'installation, methode.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Les etapes du processus", tag=t.div, toc_lvl="2")
        st_space(size=2)
        for i, (step_title, step_desc) in enumerate(steps, 1):
            with st_grid([("80px", ), 1]):
                st_write(bs.step_num, f"{i}.", tag=t.div)
                with st_block():
                    st_write(bs.step_title, step_title, tag=t.div)
                    st_write(bs.step_desc, step_desc, tag=t.div)
            st_space(size=1)
```

**Styles typiques** :
- `heading` : `s.huge + s.bold`
- `step_num` : `s.LARGE + s.bold + s.text.colors.accent`
- `step_title` : `s.Large + s.bold`
- `step_desc` : `s.large + s.text.colors.muted`

---

## Blueprint 8 : Citation / Highlight (bck_quote)

Slide avec une citation ou un message cle mis en avant.

**Quand l'utiliser** : citation d'auteur, message important, conclusion intermediaire.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_space(size=3)
        with st_block(bs.quote_box):
            st_write(bs.quote_text, "La citation ou le message cle ici.", tag=t.div)
            st_space(size=1)
            st_write(bs.attribution, "— Auteur, Source", tag=t.div)
        st_space(size=3)
```

**Styles typiques** :
- `quote_box` : fond accent, padding genereux, bordure gauche
- `quote_text` : `s.Huge + s.italic + s.center_txt`
- `attribution` : `s.Large + s.text.colors.muted + s.center_txt`

---

## Blueprint 9 : Galerie d'images (bck_gallery)

Slide avec une grille d'images.

**Quand l'utiliser** : portfolio, exemples visuels, captures d'ecran multiples.

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Galerie", tag=t.div, toc_lvl="2")
        st_space(size=2)
        with st_grid([1, 1, 1]):
            st_image("static/images/img1.png", caption="Image 1")
            st_image("static/images/img2.png", caption="Image 2")
            st_image("static/images/img3.png", caption="Image 3")
```

**Styles typiques** :
- `heading` : `s.huge + s.bold`

---

## Blueprint 10 : Conclusion / Points cles (bck_conclusion)

Slide de synthese avec les points importants.

**Quand l'utiliser** : dernier slide, resume de section, "a retenir".

**Structure** :
```python
def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Points cles", tag=t.div, toc_lvl="1")
        st_space(size=2)
        st_list(
            bs.body,
            items=[
                "Point essentiel 1",
                "Point essentiel 2",
                "Point essentiel 3",
            ],
            list_type=lt.ul,
        )
        st_space(size=3)
        st_write(bs.next_steps, "Prochaines etapes...", tag=t.div)
```

**Styles typiques** :
- `heading` : `s.huge + s.bold + s.center_txt`
- `body` : `s.Large` (gros texte pour impact)
- `next_steps` : `s.large + s.text.colors.muted + s.italic`

---

## Correspondances rapides

| L'utilisateur demande... | Blueprint |
|--------------------------|-----------|
| "slide de titre", "page d'accueil" | 1 — Titre |
| "introduction de section", "transition" | 2 — Section Header |
| "slide avec des bullets", "expliquer X" | 3 — Contenu textuel |
| "comparaison X vs Y", "avantages/inconvenients" | 4 — Comparaison |
| "image avec texte", "schema + explication" | 5 — Image + Texte |
| "demo de code", "exemple de syntaxe" | 6 — Code + Resultat |
| "etapes", "processus", "workflow" | 7 — Timeline |
| "citation", "message cle", "highlight" | 8 — Citation |
| "galerie", "portfolio", "captures d'ecran" | 9 — Galerie |
| "conclusion", "resume", "a retenir" | 10 — Conclusion |
