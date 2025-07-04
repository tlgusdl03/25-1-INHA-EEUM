# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ["./tsconfig.node.json", "./tsconfig.app.json"],
      tsconfigRootDir: import.meta.dirname,
    },
  },
});
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    "react-x": reactX,
    "react-dom": reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs["recommended-typescript"].rules,
    ...reactDom.configs.recommended.rules,
  },
});
```

```
user_dashboard
├─ eslint.config.js
├─ index.html
├─ package-lock.json
├─ package.json
├─ public
│  └─ vite.svg
├─ README.md
├─ src
│  ├─ App.css
│  ├─ App.tsx
│  ├─ components
│  │  ├─ kakao_map
│  │  │  └─ KaKaoMap.tsx
│  │  └─ location
│  │     └─ LocationList.tsx
│  ├─ hooks
│  ├─ index.css
│  ├─ main.tsx
│  ├─ pages
│  │  ├─ DetailPage.tsx
│  │  └─ ListPage.tsx
│  └─ vite-env.d.ts
├─ tsconfig.app.json
├─ tsconfig.json
├─ tsconfig.node.json
└─ vite.config.ts

```

```
user_dashboard
├─ docker-compose.yml
├─ Dockerfile
├─ eslint.config.js
├─ index.html
├─ Jenkinsfile
├─ package-lock.json
├─ package.json
├─ public
│  └─ vite.svg
├─ README.md
├─ src
│  ├─ app
│  │  └─ LocationSlice.ts
│  ├─ App.css
│  ├─ App.tsx
│  ├─ assets
│  ├─ components
│  │  ├─ grafana
│  │  │  └─ GrafanaEmbeding.tsx
│  │  ├─ kakao_map
│  │  │  ├─ KakaoMap.css
│  │  │  └─ KakaoMap.tsx
│  │  ├─ layout
│  │  │  ├─ ListPageLayout.css
│  │  │  ├─ ListPageLayout.tsx
│  │  │  ├─ ListPanelLayout.css
│  │  │  └─ ListPanelLayout.tsx
│  │  ├─ location
│  │  │  ├─ LocationCard.css
│  │  │  ├─ LocationCard.tsx
│  │  │  ├─ LocationList.css
│  │  │  └─ LocationList.tsx
│  │  └─ search_bar
│  │     ├─ SearchBar.css
│  │     └─ SearchBar.tsx
│  ├─ index.css
│  ├─ interface
│  │  ├─ location.ts
│  │  ├─ locationCardProps.ts
│  │  └─ locationState.ts
│  ├─ main.tsx
│  ├─ pages
│  │  ├─ DetailPage.tsx
│  │  └─ ListPage.tsx
│  ├─ store
│  │  ├─ api.ts
│  │  └─ store.ts
│  └─ vite-env.d.ts
├─ tsconfig.app.json
├─ tsconfig.json
├─ tsconfig.node.json
└─ vite.config.ts

```
