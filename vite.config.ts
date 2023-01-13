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
        dir: "/home/jorge/python_projects/wiki/",
      },
    },
  },
  server: {
    origin: "http://192.168.1.12:4000",
  },
});
