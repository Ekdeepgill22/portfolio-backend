.PHONY: help install dev test lint format clean docker-build docker-run docker-stop

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Run development server"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean up cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run with Docker Compose"
	@echo "  docker-stop - Stop Docker containers"

install:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio httpx pytest-cov black isort flake8 mypy

dev:
	python run.py

test:
	pytest

lint:
	flake8 app/
	mypy app/

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

docker-build:
	docker build -t portfolio-backend .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

setup-static:
	mkdir -p app/static/resume
	mkdir -p app/static/certifications
	@echo "Static directories created. Add your resume.pdf and certificate images."

check-env:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp .env .env; \
	fi

init: check-env install setup-static
	@echo "Project initialized! Don't forget to:"
	@echo "1. Update .env file with your MongoDB URI"
	@echo "2. Add resume.pdf to app/static/resume/"
	@echo "3. Add certificate images to app/static/certifications/"
	@echo "4. Run 'make dev' to start the server" commands for development
