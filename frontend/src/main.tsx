import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { Provider } from "react-redux";
import { persistStore } from "redux-persist";
import { store } from "@/redux";
import { PersistGate } from "redux-persist/integration/react";
import { Toaster } from "react-hot-toast";

import axios from "axios";
axios.defaults.baseURL =
  // "https://recipe-agent-app.greenmeadow-35e3d21d.westus3.azurecontainerapps.io";
  axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.withCredentials = true;

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistStore(store)}>
        <App />
        <Toaster position="top-right" />
      </PersistGate>
    </Provider>
  </React.StrictMode>,
);
