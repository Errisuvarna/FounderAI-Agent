#!/usr/bin/env python3
"""
Quick script to verify that the project is ready for Render deployment.
Run this before pushing to GitHub and deploying to Render.
"""
import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ MISSING {description}: {file_path}")
        return False

def check_file_content(file_path, search_text, description):
    """Check if a file contains specific text."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_text in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description} - not found in {file_path}")
                return False
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 FounderAI Deployment Readiness Check")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check required files
    print("📁 Checking Required Files...")
    print("-" * 60)
    
    files_to_check = [
        ("render.yaml", "Render configuration at root"),
        ("backend/Dockerfile", "Backend Dockerfile"),
        ("backend/.dockerignore", "Backend .dockerignore"),
        ("backend/requirements.txt", "Backend requirements"),
        ("backend/app/main.py", "Backend main application"),
        ("frontend/package.json", "Frontend package.json"),
        ("frontend/vite.config.js", "Frontend Vite config"),
        (".env.example", "Environment variables example"),
        ("README.md", "Project README"),
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    print()
    
    # Check render.yaml configuration
    print("⚙️  Checking render.yaml Configuration...")
    print("-" * 60)
    
    render_checks = [
        ("render.yaml", "dockerfilePath: ./backend/Dockerfile", "Backend Dockerfile path"),
        ("render.yaml", "dockerContext: ./backend", "Backend Docker context"),
        ("render.yaml", "runtime: docker", "Docker runtime for backend"),
        ("render.yaml", "healthCheckPath: /health", "Health check endpoint"),
    ]
    
    for file_path, search_text, description in render_checks:
        if not check_file_content(file_path, search_text, description):
            all_checks_passed = False
    
    print()
    
    # Check Dockerfile
    print("🐳 Checking Dockerfile...")
    print("-" * 60)
    
    dockerfile_checks = [
        ("backend/Dockerfile", "FROM python:3.11", "Python 3.11 base image"),
        ("backend/Dockerfile", "COPY requirements.txt", "Requirements copy"),
        ("backend/Dockerfile", "pip install", "Dependencies installation"),
        ("backend/Dockerfile", "uvicorn app.main:app", "Uvicorn command"),
    ]
    
    for file_path, search_text, description in dockerfile_checks:
        if not check_file_content(file_path, search_text, description):
            all_checks_passed = False
    
    print()
    
    # Summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED! Ready for deployment.")
        print()
        print("Next steps:")
        print("1. Review DEPLOYMENT.md for deployment instructions")
        print("2. Ensure you have all required API keys:")
        print("   - MongoDB URI")
        print("   - Gemini API Key")
        print("   - Serper API Key")
        print("   - JWT Secret Key")
        print("3. Push to GitHub: git push origin main")
        print("4. Deploy on Render using Blueprint")
        return 0
    else:
        print("❌ SOME CHECKS FAILED! Please fix the issues above.")
        print()
        print("Review the deployment setup and ensure all files are present.")
        return 1
    print("=" * 60)

if __name__ == "__main__":
    sys.exit(main())
