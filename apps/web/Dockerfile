FROM node:20-bullseye
WORKDIR /app

# Copy manifests and config first
COPY apps/web/package.json apps/web/package-lock.json apps/web/svelte.config.js apps/web/vite.config.ts ./
RUN npm ci

# Copy the rest of the source
COPY apps/web/. .

# Build with local binary via npm script
RUN npm run build

EXPOSE 5173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
