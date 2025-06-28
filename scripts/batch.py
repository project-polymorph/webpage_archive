#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import concurrent.futures
from pathlib import Path

def parse_env_args(args):
    """Parse key=value pairs into a dictionary"""
    env_vars = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            env_vars[key] = value
    return env_vars

def process_file(src_file, dst_path, processor_script, env):
    """Process a single HTML file - for parallel execution"""
    cmd = ["node", processor_script, str(src_file), str(dst_path)]
    try:
        subprocess.run(cmd, env=env, check=True)
        return f"Processed: {src_file.name}"
    except subprocess.CalledProcessError as e:
        return f"Error processing {src_file.name}: {e}"

def clean_directory(src_dir: str, dst_dir: str, processor_script: str, env_vars: dict = None, num_threads: int = 4):
    # Create destination directory if it doesn't exist
    dst_path = Path(dst_dir)
    dst_path.mkdir(parents=True, exist_ok=True)
    
    # Copy page.yml if it doesn't exist in destination
    src_yml = Path(src_dir) / "page.yml"
    dst_yml = dst_path / "page.yml"
    if src_yml.exists() and not dst_yml.exists():
        shutil.copy2(src_yml, dst_yml)
        print(f"Copied page.yml to {dst_path}")
    
    # Prepare environment variables
    env = os.environ.copy()  # Copy current environment
    if env_vars:
        env.update(env_vars)
        print("Using environment variables:", env_vars)
    
    # Get all HTML files to process
    html_files = list(Path(src_dir).glob("*.html"))
    print(f"Found {len(html_files)} HTML files to process with {num_threads} threads")
    
    # Process files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_file, src_file, dst_path, processor_script, env) 
                  for src_file in html_files]
        
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

def main():
    if len(sys.argv) < 4:
        print("Usage: python batch.py <source_dir> <destination_dir> <processor_script> [--threads=N] [KEY1=value1] [KEY2=value2] ...")
        print("Example: python batch.py ./raw_pages ./cleaned_pages ./clean_cheerio.js --threads=8 HTML_CLEANER_CONFIG=./config.json DEBUG=true")
        sys.exit(1)
    
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    processor_script = sys.argv[3]
    
    # Parse remaining arguments
    env_vars = {}
    num_threads = 16  # Default number of threads
    
    for arg in sys.argv[4:]:
        if arg.startswith('--threads='):
            try:
                num_threads = int(arg.split('=')[1])
            except (ValueError, IndexError):
                print(f"Error: Invalid thread count format. Using default {num_threads} threads.")
        elif '=' in arg:
            key, value = arg.split('=', 1)
            env_vars[key] = value
    
    if not os.path.isdir(src_dir):
        print(f"Error: Source directory '{src_dir}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.isfile(processor_script):
        print(f"Error: Processor script '{processor_script}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    clean_directory(src_dir, dst_dir, processor_script, env_vars, num_threads)

if __name__ == "__main__":
    main()
