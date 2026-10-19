# One Dockerfile, three stages. Pick one with --target (compose uses "dev").

# --- deps: install packages from the lockfile (reproducible, cached layer) ---
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# --- dev: Vite dev server with hot reload, used by docker-compose ---
FROM deps AS dev
COPY . .
CMD ["npm", "run", "dev"]

# --- build: compile TypeScript + bundle into static files in /app/dist ---
FROM deps AS build
COPY . .
# Vite inlines VITE_* vars at build time, so the API URL is baked into the bundle.
# Pass it with: docker build --build-arg VITE_API_URL=https://api.example.com
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- prod: tiny nginx image serving only the built files (no Node at runtime) ---
FROM nginx:1.27-alpine AS prod
# The official image runs envsubst on /etc/nginx/templates/*.template at startup,
# which fills in ${PORT} (Cloud Run sets it; 8080 by default).
ENV PORT=8080
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
