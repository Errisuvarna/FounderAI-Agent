# Multi-stage build for FounderAI

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend with frontend static files
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create chroma data directory
RUN mkdir -p ./backend/chroma_data

# Expose port
EXPOSE 8000

# Set working directory to backend
WORKDIR /app/backend

# Run the application
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
