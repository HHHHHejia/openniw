FROM node:20-slim AS build
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY package*.json ./
RUN npm ci
COPY . .
RUN npx next build

FROM node:20-slim
WORKDIR /app
ENV NODE_ENV=production
RUN npm install -g serve@14
COPY --from=build /app/out ./out
EXPOSE 3000
CMD ["sh", "-c", "serve out -l ${PORT:-3000}"]
