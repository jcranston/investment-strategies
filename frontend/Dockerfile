# Stage 1: Build the React frontend
FROM node:20 AS builder

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy source code and build the app
COPY frontend/ ./
RUN npm run build

# Stage 2: Serve the build using Nginx
FROM nginx:alpine

# Copy custom nginx config (you should create this next to the Dockerfile)
COPY nginx.conf /etc/nginx/nginx.conf

# Copy build output from the React build
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Nginx will run as default CMD
