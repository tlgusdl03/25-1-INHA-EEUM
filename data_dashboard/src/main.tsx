import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { BrowserRouter } from "react-router";
import { Provider } from "react-redux";
import { persistor, store } from "./app/store.ts";
import { PersistGate } from "redux-persist/integration/react";

createRoot(document.getElementById("root")!).render(
  <BrowserRouter basename="/frontend">
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <StrictMode>
          <App />
        </StrictMode>
      </PersistGate>
    </Provider>
  </BrowserRouter>
);
