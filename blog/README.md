# Blog Finiteck — Guide pour ajouter un nouvel article

Le blog est en HTML statique pur (aucun build tool). Pour publier un nouvel article, suivez ces étapes.

## 1. Créer le fichier de l'article

Copiez `economiser-argent-par-ou-commencer-2026.html` comme template et renommez-le :

```
blog/<slug-en-kebab-case>.html
```

Le slug doit refléter le sujet et inclure des mots-clés SEO. Exemples : `negocier-assurance-auto-2026.html`, `pel-vs-livret-a-comparaison.html`.

## 2. Mettre à jour le head

Dans le nouveau fichier, modifiez :

- `<title>` — titre court (50-60 caractères)
- `<meta name="description">` — résumé 150-160 caractères
- `<link rel="canonical">` — URL absolue de l'article
- `<link rel="alternate" hreflang="fr">` — même URL
- Tous les `<meta property="og:*">` (titre, description, URL, date publication)
- `<meta property="article:published_time">` — date ISO 8601
- Schema JSON-LD `BlogPosting` : `headline`, `description`, `datePublished`, `dateModified`, `mainEntityOfPage.@id`
- Schema JSON-LD `BreadcrumbList` : nom et URL du dernier item

## 3. Référencer l'article dans le listing

Dans `blog/index.html`, ajoutez une nouvelle `<a class="post-card">` **en haut** de la liste `.post-list` (ordre antéchronologique) :

```html
<a href="<slug>.html" class="post-card" aria-label="Lire : <Titre>">
    <div class="post-meta">
        <time datetime="2026-MM-DD">DD mois 2026</time>
        <span class="post-tag">Catégorie</span>
        <span>X min de lecture</span>
    </div>
    <h2>Titre de l'article</h2>
    <p>Résumé de 1-2 phrases qui donne envie de cliquer.</p>
    <span class="post-cta">Lire l'article <span aria-hidden="true">→</span></span>
</a>
```

## 4. Mettre à jour le flux RSS

Dans `blog/feed.xml`, ajoutez un nouvel `<item>` **en haut** des items existants :

```xml
<item>
    <title>Titre de l'article</title>
    <link>https://finiteck.com/blog/<slug>.html</link>
    <guid isPermaLink="true">https://finiteck.com/blog/<slug>.html</guid>
    <pubDate>Day, DD Mon YYYY HH:MM:SS +0200</pubDate>
    <category>Catégorie</category>
    <description>Résumé identique au listing.</description>
</item>
```

Pensez aussi à actualiser `<lastBuildDate>` du channel.

## 5. Mettre à jour le sitemap

Dans `/sitemap.xml` (à la racine), ajoutez une nouvelle entrée `<url>` :

```xml
<url>
    <loc>https://finiteck.com/blog/<slug>.html</loc>
    <lastmod>YYYY-MM-DD</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
</url>
```

## 6. Vérifier puis pousser

- Ouvrir l'article dans un navigateur localement (`open blog/<slug>.html`) pour vérifier le rendu
- Valider le JSON-LD sur https://validator.schema.org/
- Commit + push — GitHub Pages déploie automatiquement en 30-60 secondes

## Catégories suggérées

Pour la cohérence, utilisez l'une de ces catégories en `<span class="post-tag">` :

- **Méthode** — guides pas-à-pas, démarches structurées
- **Analyse** — comparaisons, études de marché
- **Astuce** — conseils courts et actionnables
- **Produit** — nouveautés Finiteck, retours d'expérience utilisateurs
