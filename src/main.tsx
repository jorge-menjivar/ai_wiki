import React from "react";
import ReactDOM from "react-dom/client";
import Root from "./routes/App";
import Page from "./routes/Page";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "/styles/index.scss";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
  },
  {
    path: "wiki/:level/:title",
    element: <Page />,
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
