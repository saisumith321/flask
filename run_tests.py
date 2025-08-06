#!/usr/bin/env python3
"""
Test runner script for comment CRUD API tests
"""
import sys
import subprocess
import os


def run_tests():
    """Run all tests with coverage"""
    print("🧪 Running Comment CRUD API Tests...")
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/task/",
        "-v",
        "--tb=short",
        "--cov=task",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        return e.returncode


def run_unit_tests():
    """Run only unit tests"""
    print("🧪 Running Unit Tests...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/task/test_comment_service.py",
        "tests/task/test_comment_reader.py", 
        "tests/task/test_comment_writer.py",
        "-v",
        "-m", "not integration"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Unit tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Unit tests failed with exit code {e.returncode}")
        return e.returncode


def run_integration_tests():
    """Run only integration tests"""
    print("🧪 Running Integration Tests...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/task/test_comment_api_integration.py",
        "-v",
        "-m", "integration"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Integration tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Integration tests failed with exit code {e.returncode}")
        return e.returncode


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "unit":
            sys.exit(run_unit_tests())
        elif sys.argv[1] == "integration":
            sys.exit(run_integration_tests())
        else:
            print("Usage: python run_tests.py [unit|integration]")
            sys.exit(1)
    else:
        sys.exit(run_tests())