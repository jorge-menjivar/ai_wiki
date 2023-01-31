import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import "cors";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    manifest: true,
    rollupOptions: {
      output: {
        dir: "../server/",
      },
    },
  },
  server: {
    origin: "http://localhost:4000",
  },
});
