# Stage for Node.js build (example, adjust as needed)
FROM node:18 AS builder
WORKDIR /app
COPY . /app/
RUN npm ci --prefer-offline --no-audit
RUN npm run build

# Production image (optional, for static builds or Node servers)
FROM node:18-slim
WORKDIR /app
COPY --from=builder /app ./
CMD ["npm", "start"]