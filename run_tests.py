#!/usr/bin/env python3
"""
Script to run tests with various options and generate reports
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"Command failed with return code: {result.returncode}")
        return False
    
    return True


def ensure_directories():
    """Create necessary directories"""
    directories = ["allure-results", "allure-reports", "screenshots"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import playwright
        import pytest
        import allure
        print("✓ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Effective Mobile website tests")
    parser.add_argument("--headed", action="store_true", help="Run tests with visible browser")
    parser.add_argument("--browser", default="chromium", choices=["chromium", "firefox", "webkit"], help="Browser to use")
    parser.add_argument("--generate-report", action="store_true", help="Generate Allure report after tests")
    parser.add_argument("--serve-report", action="store_true", help="Serve Allure report after generation")
    parser.add_argument("--specific-test", help="Run specific test file or method")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--reruns", type=int, default=0, help="Number of reruns on failure")
    parser.add_argument("--check-deps", action="store_true", help="Check dependencies before running tests")
    
    args = parser.parse_args()
    
    # Check dependencies if requested
    if args.check_deps:
        if not check_dependencies():
            sys.exit(1)
        print("\nDependencies check completed.\n")
    
    # Ensure directories exist
    ensure_directories()
    
    # Build pytest command
    pytest_cmd = "pytest"
    
    if args.verbose:
        pytest_cmd += " -v"
    
    if args.headed:
        pytest_cmd += " --headed"
    
    pytest_cmd += f" --browser={args.browser}"
    pytest_cmd += " --alluredir=./allure-results"
    
    if args.reruns > 0:
        pytest_cmd += f" --reruns {args.reruns}"
    
    if args.specific_test:
        pytest_cmd += f" {args.specific_test}"
    
    # Run tests
    success = run_command(pytest_cmd, "Running automated tests")
    
    if not success:
        print("Tests failed!")
        sys.exit(1)
    
    print("Tests completed successfully!")
    
    # Generate report if requested
    if args.generate_report or args.serve_report:
        print("\nGenerating Allure report...")
        success = run_command(
            "allure generate allure-results -o allure-reports --clean",
            "Generating Allure report"
        )
        
        if success and args.serve_report:
            print("\nStarting Allure report server...")
            print("Report will be available at: http://localhost:8080")
            print("Press Ctrl+C to stop the server")
            run_command("allure serve allure-results", "Serving Allure report")
    
    print("\nTest execution completed!")


if __name__ == "__main__":
    main()
