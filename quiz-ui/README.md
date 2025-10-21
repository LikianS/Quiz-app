# quiz-ui

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Tailwind CSS

Tailwind est configuré avec PostCSS et Vite.

Fichiers ajoutés :

- `tailwind.config.js`
- `postcss.config.js`
- Directives Tailwind dans `src/assets/main.css`

### Ajouter une classe utilitaire

Utilise simplement les classes dans tes composants Vue :

```vue
<template>
  <h1 class="text-3xl font-bold text-emerald-600">Quiz</h1>
</template>
```

### Purge / Tree-shaking

Géré automatiquement par Tailwind via la clé `content` du fichier `tailwind.config.js`.

### Mise à jour des dépendances

```sh
npm install -D tailwindcss postcss autoprefixer
```

Les dépendances sont déjà listées dans `devDependencies`. Pour une installation clean :

```sh
npm ci
```

## Docker

L'image de production construit le bundle (`npm run build`) puis le sert via Nginx. Le CSS Tailwind est compilé dans `dist/assets`. Aucune configuration additionnelle n'est nécessaire dans le Dockerfile.
