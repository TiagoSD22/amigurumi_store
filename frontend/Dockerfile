FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json first for better Docker layer caching
COPY frontend/package.json ./

# Install dependencies and generate package-lock.json
RUN npm install --production=false

# Copy source code
COPY frontend/ ./

# Build the application
RUN npm run build

# Use nginx to serve the built app
FROM nginx:alpine

# Copy built app from previous stage
COPY --from=0 /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY scripts/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
