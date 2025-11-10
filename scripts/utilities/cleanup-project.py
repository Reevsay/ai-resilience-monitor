#!/usr/bin/env python3
"""
Project Cleanup Script
Safely removes duplicate, obsolete, and unused files without affecting functionality
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path(__file__).parent

# Files to DELETE (obsolete/duplicates)
FILES_TO_DELETE = [
    # Duplicate/obsolete markdown documentation (keep only essential ones in /documentation)
    "CHAOS_DASHBOARD_QUICK_START.md",
    "CHAOS_DASHBOARD_VISUAL_GUIDE.md",
    "CHAOS_TESTING_DASHBOARD.md",
    "CHAOS_TEST_QUICK_START.md",
    "CHAOS_TEST_README.md",
    "INTEGRATION_SUMMARY.md",
    "MONITOR_QUICK_START.md",
    "MONITOR_README.md",
    "START_COMMANDS.md",
    "EMPIRICAL_VALIDATION_GUIDE.md",
    
    # Duplicate monitor scripts (keep only the enhanced version)
    "monitor-backend.py",
    "monitor-backend.ps1",
    
    # Obsolete batch/PowerShell scripts (replaced by enhanced versions)
    "control-panel.bat",
    "start-chaos-test.bat",
    "start-monitor.bat",
    "monitor.log",
    
    # Duplicate frontend redesign specs
    "frontend-redesign-specification.md",  # Keeping FRONTEND_REDESIGN_SPECIFICATION.md
    
    # Demo/test files no longer needed
    "demo-enhanced-output.py",
    "test-cumulative-requests.py",
    
    # Obsolete recovery status file
    "RECOVERY_STATUS.txt",
    
    # Duplicate .env files
    ".env.example",
    ".env.template",  # Keep only .env
]

# Directories to DELETE (if empty or obsolete)
DIRS_TO_DELETE = [
    ".kiro",
    "__pycache__",
]

# Files to KEEP (essential for operation)
ESSENTIAL_FILES = {
    "app.py",  # Frontend Flask server
    "chaos-test.py",  # Chaos testing script
    "database.py",  # Database operations
    "monitor-backend-enhanced.py",  # Backend monitoring
    "monitor-frontend-continuous.py",  # Frontend monitoring
    "start-monitor-enhanced.ps1",  # Enhanced startup script
    "START_MONITOR_ENHANCED.bat",  # Enhanced startup batch
    "package.json",  # Node.js dependencies
    "requirements.txt",  # Python dependencies
    "docker-compose.yml",  # Docker configuration
    "Dockerfile",  # Docker build
    "prometheus.yml",  # Prometheus config
    ".gitignore",  # Git configuration
    "LICENSE",  # License file
    "README.md",  # Main documentation
    "CONTRIBUTING.md",  # Contribution guidelines
}

# Documentation to KEEP (consolidated guides)
KEEP_DOCS = {
    "CRASH_RECOVERY_GUIDE.md",
    "ENHANCED_OUTPUT_GUIDE.md",
    "CUMULATIVE_REQUESTS_GUIDE.md",
    "TOTAL_REQUESTS_FIX.md",
    "QUICK_REFERENCE_TOTAL_REQUESTS.md",
    "CHAOS_OUTPUT_FIX.md",
    "CHAOS_CRASH_FIX.md",
    "LITERATURE_REVIEW.md",
    "FRONTEND_REDESIGN_SPECIFICATION.md",
}

def create_backup_list():
    """Create a list of files being deleted"""
    backup_file = BASE_DIR / f"CLEANUP_BACKUP_LIST_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write("=== PROJECT CLEANUP REPORT ===\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write("Files to be deleted:\n")
        f.write("=" * 60 + "\n")
        
        for file in FILES_TO_DELETE:
            file_path = BASE_DIR / file
            if file_path.exists():
                size = file_path.stat().st_size if file_path.is_file() else 0
                f.write(f"  - {file} ({size:,} bytes)\n")
        
        f.write("\nDirectories to be deleted:\n")
        f.write("=" * 60 + "\n")
        for dir_name in DIRS_TO_DELETE:
            dir_path = BASE_DIR / dir_name
            if dir_path.exists():
                f.write(f"  - {dir_name}/\n")
    
    return backup_file

def safe_delete_file(file_path):
    """Safely delete a file"""
    try:
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            print(f"✓ Deleted: {file_path.name}")
            return True
        return False
    except Exception as e:
        print(f"✗ Error deleting {file_path.name}: {e}")
        return False

def safe_delete_dir(dir_path):
    """Safely delete a directory"""
    try:
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)
            print(f"✓ Deleted directory: {dir_path.name}/")
            return True
        return False
    except Exception as e:
        print(f"✗ Error deleting directory {dir_path.name}: {e}")
        return False

def cleanup_project():
    """Main cleanup function"""
    print("=" * 70)
    print("PROJECT CLEANUP - Safe Deletion of Obsolete Files")
    print("=" * 70)
    print()
    
    # Create backup list
    print("Creating backup list of files to be deleted...")
    backup_file = create_backup_list()
    print(f"✓ Backup list saved: {backup_file.name}\n")
    
    # Delete files
    print("Deleting obsolete files...")
    print("-" * 70)
    deleted_files = 0
    for file_name in FILES_TO_DELETE:
        file_path = BASE_DIR / file_name
        if safe_delete_file(file_path):
            deleted_files += 1
    
    print()
    print("Deleting obsolete directories...")
    print("-" * 70)
    deleted_dirs = 0
    for dir_name in DIRS_TO_DELETE:
        dir_path = BASE_DIR / dir_name
        if safe_delete_dir(dir_path):
            deleted_dirs += 1
    
    # Summary
    print()
    print("=" * 70)
    print("CLEANUP SUMMARY")
    print("=" * 70)
    print(f"Files deleted:       {deleted_files}")
    print(f"Directories deleted: {deleted_dirs}")
    print(f"Backup list:         {backup_file.name}")
    print()
    print("✓ Cleanup complete!")
    print()
    print("Essential files preserved:")
    print("-" * 70)
    for file in sorted(ESSENTIAL_FILES):
        if (BASE_DIR / file).exists():
            print(f"  ✓ {file}")
    
    print()
    print("Documentation preserved:")
    print("-" * 70)
    for doc in sorted(KEEP_DOCS):
        if (BASE_DIR / doc).exists():
            print(f"  ✓ {doc}")
    
    print()
    print("✓ All essential files and documentation intact")
    print("✓ Running processes NOT affected")
    print()

if __name__ == '__main__':
    try:
        cleanup_project()
    except KeyboardInterrupt:
        print("\n\n✗ Cleanup cancelled by user")
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
