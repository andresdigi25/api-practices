.PHONY: build clean run-gunicorn run-uvicorn run-all test help

# Default target
help:
	@echo "Available targets:"
	@echo "  build         - Build both Gunicorn and Uvicorn Docker images"
	@echo "  clean         - Remove all Docker containers and images"
	@echo "  run-gunicorn  - Run the Gunicorn version"
	@echo "  run-uvicorn   - Run the Uvicorn version"
	@echo "  run-all       - Run both versions simultaneously"
	@echo "  test          - Run the test script"
	@echo "  stop          - Stop all running containers"

# Build both versions
build:
	@echo "Building Docker images..."
	docker compose build

# Clean up Docker resources
clean:
	@echo "Cleaning up Docker resources..."
	docker compose down --rmi all
	docker system prune -f

# Run Gunicorn version
run-gunicorn:
	@echo "Starting Gunicorn version..."
	docker compose --profile gunicorn up -d

# Run Uvicorn version
run-uvicorn:
	@echo "Starting Uvicorn version..."
	docker compose --profile uvicorn up -d

# Run both versions
run-all:
	@echo "Starting both versions..."
	docker compose --profile gunicorn --profile uvicorn up -d

# Run tests
test:
	@echo "Running tests..."
	@chmod +x test.sh
	@./test.sh

# Stop all containers
stop:
	@echo "Stopping all containers..."
	docker compose down 