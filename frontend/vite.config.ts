import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

// Frontend builds to ./dist, which the backend serves in local/production runs.
// During dev, /api is proxied to the FastAPI server on port 8000.
export default defineConfig({
	plugins: [react()],
	build: { outDir: "dist" },
	server: {
		port: 5173,
		proxy: {
			"/api": "http://127.0.0.1:8000",
		},
	},
})
