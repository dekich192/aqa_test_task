#!/usr/bin/env python3
"""
Quick setup verification script
"""
import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 10:
        print("ERROR: Python 3.10+ is required")
        return False
    
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "playwright",
        "pytest", 
        "allure-pytest",
        "pytest-playwright"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0


def check_project_structure():
    """Check if project structure is correct"""
    required_dirs = ["pages", "tests", "utils", "config"]
    required_files = [
        "requirements.txt",
        "pytest.ini", 
        "conftest.py",
        "Dockerfile",
        "README.md"
    ]
    
    missing_items = []
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✓ {directory}/ directory exists")
        else:
            print(f"✗ {directory}/ directory missing")
            missing_items.append(directory)
    
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            missing_items.append(file)
    
    return len(missing_items) == 0


def check_environment():
    """Check environment setup"""
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file exists")
        return True
    else:
        print("⚠ .env file missing (copy .env.example to .env)")
        return False


def main():
    print("Effective Mobile Test Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Environment", check_environment)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All checks passed! Project is ready to run.")
        print("\nNext steps:")
        print("1. Run: pytest")
        print("2. Or: python run_tests.py --generate-report")
        print("3. Or: make test")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nTo install dependencies:")
        print("pip install -r requirements.txt")
        print("playwright install chromium")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
