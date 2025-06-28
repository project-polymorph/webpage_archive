import os
import sys
import subprocess
from pathlib import Path

def process_directory(batch_dir):
    # Convert to Path object
    batch_dir = Path(batch_dir)
    downloads_dir = batch_dir / 'downloads'
    
    if not downloads_dir.exists():
        print(f"Error: downloads directory not found in {batch_dir}")
        return
    
    # Create necessary directories
    cleaned_dir = batch_dir / 'cleaned'
    markdown_dir = batch_dir / 'markdown'
    ready_dir = batch_dir / 'ready'
    
    cleaned_dir.mkdir(exist_ok=True)
    markdown_dir.mkdir(exist_ok=True)
    ready_dir.mkdir(exist_ok=True)
    
    # Step 1: Generate config if page.yml doesn't exist
    page_yml = downloads_dir / 'page.yml'
    results_json = downloads_dir / 'results.json'
    if not page_yml.exists() and results_json.exists():
        print("Generating config...")
        subprocess.run(['python', 'scripts/config/new_config.py', str(results_json), str(page_yml)], check=True)
        subprocess.run(['python', 'scripts/config/add_meta.py', str(page_yml)], check=True)
    
    # Step 2: Clean HTML
    print("Cleaning HTML...")
    domain = batch_dir.name
    cleaner_config = Path(f'./scripts/cleaner/configs/{domain}.json')
    if not cleaner_config.exists():
        cleaner_config = Path('./scripts/cleaner/configs/unclassify_news.json')
        print(f"Warning: No specific cleaner config found for {domain}, using default config")
    
    subprocess.run([
        'python', 'scripts/batch.py',
        str(downloads_dir) + '/',
        str(cleaned_dir) + '/',
        './scripts/cleaner/clean_cheerio.js',
        f'HTML_CLEANER_CONFIG={cleaner_config}'
    ], check=True)
    
    # Step 3: Convert to Markdown
    print("Converting to Markdown...")
    subprocess.run([
        'python', 'scripts/batch.py',
        str(cleaned_dir) + '/',
        str(markdown_dir) + '/',
        'scripts/markdown/html2md.js'
    ], check=True)
    
    # Step 4: AI Processing
    print("Running AI processing...")
    subprocess.run([
        'python', 'scripts/ai/process_dir.py',
        str(markdown_dir) + '/',
        str(ready_dir) + '/',
        'scripts/ai/prompt/clean.template',
        '--skip-size-check'
    ], check=True)
    
    print(f"Processing complete. Files are ready in {ready_dir}")
    return batch_dir

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_raw_dir.py <batch_directory>")
        sys.exit(1)
    
    batch_dir = sys.argv[1]
    if not os.path.exists(batch_dir):
        print(f"Error: Directory {batch_dir} does not exist")
        sys.exit(1)
        
    processed_dir = process_directory(batch_dir)
    print(f"\nYou can now run file_processor.py with:")
    print(f"python file_processor.py {processed_dir} <target_directory>")
