FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json first for better Docker layer caching
COPY frontend/package.json ./

# Install dependencies and generate package-lock.json
RUN npm install --production=false

# Copy source code
COPY frontend/ ./

# Expose port
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
