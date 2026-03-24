version: "3.9"

services:
  backend:
    build: ./backend
    container_name: backend
    restart: always
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
      - ollama

  frontend:
    build: ./frontend
    container_name: frontend
    restart: always
    ports:
      - "3000:80"

  db:
    image: postgres:15
    container_name: postgres
    restart: always
    environment:
      POSTGRES_USER: ai
      POSTGRES_PASSWORD: ai
      POSTGRES_DB: ai_grader
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    container_name: redis
    restart: always
    ports:
      - "6379:6379"

  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"