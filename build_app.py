#!/usr/bin/env python3
"""
Build script for Canva File Namer application
This script uses Nuitka to compile the application, which typically results in
faster startup times and smaller executable size compared to PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_folders():
    """Remove previous build folders"""
    folders_to_clean = ['build', 'file_namer.build', 'file_namer.dist']
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            print(f"Cleaning {folder}...")
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(f"Error cleaning {folder}: {e}")
    
    # Special handling for dist folder
    dist_folder = 'dist'
    if os.path.exists(dist_folder):
        print(f"Cleaning {dist_folder}...")
        try:
            # Instead of removing the entire directory, remove only the files
            for item in os.listdir(dist_folder):
                item_path = os.path.join(dist_folder, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Error removing {item_path}: {e}")
        except Exception as e:
            print(f"Error cleaning {dist_folder}: {e}")

def build_with_nuitka():
    """Build the application using Nuitka"""
    print("Building with Nuitka...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",               # Create a standalone executable
        "--follow-imports",           # Follow imports for better dependency tracking
        "--windows-disable-console",  # No console window
        "--enable-plugin=tk-inter",   # Support for tkinter
        "--include-package=babel",    # Required by tkcalendar
        "--include-package=tkcalendar",
        "--windows-product-name=Canva File Namer",
        "--windows-company-name=TFCSS",
        "--windows-file-description=Canva Design File Namer Tool",
        "--windows-file-version=1.0.0",
        "--assume-yes-for-downloads", # Don't prompt for downloads
        "--low-memory",               # Use less memory during compilation
        "--output-dir=dist",          # Output to dist directory
        "--remove-output",            # Clean up previous builds
        # Exclude packages we don't need
        "--nofollow-import-to=numpy,pandas,matplotlib,PIL,scipy",
        # Add options for faster build
        "--jobs=0",                   # Use all available cores
        "--lto=yes",                  # Link time optimization
        "file_namer.py"              # The main script to compile
    ]
    
    try:
        print("Starting Nuitka build - this may take a few minutes...")
        result = subprocess.run(cmd, check=True)
        print("Build completed successfully!")
        
        # Rename the executable for consistency
        source_exe = os.path.join("dist", "file_namer.exe")
        target_exe = os.path.join("dist", "Canva File Namer.exe")
        
        if os.path.exists(source_exe):
            if os.path.exists(target_exe):
                os.remove(target_exe)
            os.rename(source_exe, target_exe)
            print(f"Executable renamed to: {target_exe}")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during build: {e}")
        return False

if __name__ == "__main__":
    print("=== Building Canva File Namer Application ===")
    clean_build_folders()
    success = build_with_nuitka()
    
    if success:
        exe_path = os.path.join("dist", "Canva File Namer.exe")
        print("\nBuild successful!")
        print(f"Executable is located at: {os.path.abspath(exe_path)}")
        print("You can now double-click the executable to run the application.")
    else:
        print("\nBuild failed. Please check the error messages above.")