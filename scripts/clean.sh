#!/bin/bash

set -e

safe_remove() {
    if [ -e "$1" ]; then
        rm -rf "$1"
    fi
}

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

find . -type f -name "*.so" -delete 2>/dev/null || true
find . -type f -name "*.c" -delete 2>/dev/null || true
find . -type f -name "*.cpp" -delete 2>/dev/null || true
find . -type f -name "*.html" -path "*/.*" -delete 2>/dev/null || true

find . -type d -name ".pyxbld" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pyxbldinplace" -exec rm -rf {} + 2>/dev/null || true

safe_remove "build"
safe_remove "dist"
safe_remove "*.egg-info"
safe_remove "flask_inputfilter.egg-info"
safe_remove ".eggs"

find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

safe_remove ".coverage"
safe_remove "htmlcov"
safe_remove "coverage.xml"
safe_remove ".coverage.*"

safe_remove ".tox"

safe_remove ".idea/__pycache__"
safe_remove ".vscode/__pycache__"

find flask_inputfilter -type f \( -name "*.c" -o -name "*.cpp" -o -name "*.so" \) -delete 2>/dev/null || true
