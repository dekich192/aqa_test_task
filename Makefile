.PHONY: help install test test-headed test-firefox test-report clean docker-build docker-run docker-compose

# Default target
help:
	@echo "Effective Mobile Test Automation"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies and setup environment"
	@echo "  test         - Run all tests"
	@echo "  test-headed  - Run tests with visible browser"
	@echo "  test-firefox - Run tests with Firefox"
	@echo "  test-report  - Run tests and generate Allure report"
	@echo "  serve-report - Serve Allure report locally"
	@echo "  clean        - Clean up temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run tests in Docker container"
	@echo "  docker-compose - Run tests and report with Docker Compose"
	@echo ""

# Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	playwright install chromium
	playwright install-deps chromium
	@echo "Installation completed!"

# Test commands
test:
	@echo "Running tests..."
	pytest --alluredir=./allure-results -v

test-headed:
	@echo "Running tests with visible browser..."
	pytest --alluredir=./allure-results -v --headed

test-firefox:
	@echo "Running tests with Firefox..."
	pytest --alluredir=./allure-results -v --browser=firefox

test-report:
	@echo "Running tests and generating report..."
	pytest --alluredir=./allure-results -v
	allure generate allure-results -o allure-reports --clean

serve-report:
	@echo "Starting Allure report server..."
	allure serve allure-results

# Cleanup
clean:
	@echo "Cleaning up..."
	rm -rf allure-results/
	rm -rf allure-reports/
	rm -rf screenshots/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	@echo "Cleanup completed!"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t effective-mobile-tests .

docker-run:
	@echo "Running tests in Docker..."
	docker run --rm -v $(PWD)/allure-results:/app/allure-results effective-mobile-tests

docker-compose:
	@echo "Running tests and report with Docker Compose..."
	docker-compose up --build

docker-stop:
	@echo "Stopping Docker containers..."
	docker-compose down

# Development
dev-setup:
	@echo "Setting up development environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  Windows: venv\\Scripts\\activate"
	@echo "  Linux/Mac: source venv/bin/activate"
	@echo "Then run: make install"

# Quick test run
quick-test:
	@echo "Running quick test..."
	python run_tests.py --verbose --generate-report

# Full test suite
full-test:
	@echo "Running full test suite..."
	python run_tests.py --verbose --generate-report --serve-report
