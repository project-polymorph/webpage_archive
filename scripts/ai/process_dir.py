import os
import argparse
import tempfile
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file_content(file_path):
    """Read content from a file with various encodings."""
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    logging.error(f"Failed to read {file_path} with any supported encoding")
    return None

def process_file(file_path, prompt_template, gen_script_path, output_dir, counter, total_files):
    """Process a single file using the provided prompt template."""
    # Skip if file is larger than 100KB
    if os.path.getsize(file_path) > 100 * 1024:
        logging.info(f"Skipping {file_path} - file size exceeds 100KB")
        return True

    # Create output path in dst directory
    rel_path = os.path.relpath(file_path, start=args.src)
    output_path = os.path.join(output_dir, rel_path)
    
    # Skip if output file already exists
    if os.path.exists(output_path):
        logging.info(f"Skipping {file_path} - output file already exists: {output_path}")
        return True
    
    # skip page.yml
    if file_path.endswith('page.yml'):
        logging.info(f"Skipping {file_path} - it's a page.yml file")
        return True

    content = read_file_content(file_path)
    if content is None:
        return False

    # Format the prompt template with the file content
    try:
        input_content = prompt_template.format(file=content)
    except KeyError as e:
        logging.error(f"Invalid placeholder in template: {e}")
        return False
    
    print("input_content:")
    print("============================================")
    print(input_content)
    print("============================================")
    print(f"Processed file {counter}/{total_files}")

    # Create temporary file for input
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_input:
        temp_input.write(input_content)
        temp_input_path = temp_input.name

    try:
        # Run gen.py
        cmd = [
            'python', gen_script_path,
            temp_input_path, output_path
        ]
        
        subprocess.run(cmd, check=True)
        logging.info(f"Successfully processed {file_path} -> {output_path}")
        print("============================================")
        print(read_file_content(output_path))
        print("============================================")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {file_path}: {e}")
        return False

    finally:
        os.unlink(temp_input_path)

def check_file_sizes(src_dir, pattern, max_size_kb=50):
    """Check if any file in the directory exceeds the maximum size."""
    src_path = Path(src_dir)
    oversized_files = False
    for file_path in src_path.rglob(pattern):
        if file_path.is_file() and file_path.stat().st_size > max_size_kb * 1024 and not str(file_path).endswith('.yml'):
            logging.warning(f"File {file_path} exceeds {max_size_kb}KB")
            print(f"File {file_path} size: {file_path.stat().st_size / 1024} KB")
            oversized_files = True
    return not oversized_files

def main():
    parser = argparse.ArgumentParser(description='Process files using a prompt template')
    parser.add_argument('src', help='Source directory containing input files')
    parser.add_argument('dst', help='Destination directory for output files')
    parser.add_argument('prompt', help='Path to prompt template file')
    parser.add_argument('--gen', help='Path to gen.py script', default='scripts/ai/gen.py')
    parser.add_argument('--pattern', default='*.*', help='File pattern to match (default: *.*)')
    parser.add_argument('--skip-size-check', action='store_true', default=True, help='Skip initial file size check (default: True)')

    global args
    args = parser.parse_args()

    # Check file sizes before processing, unless skipping is specified
    if not check_file_sizes(args.src, args.pattern) and not args.skip_size_check:
        logging.error("One or more files exceed the maximum allowed. Exiting.")
        exit(1)

    # Read prompt template
    try:
        with open(args.prompt, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
    except Exception as e:
        logging.error(f"Failed to read prompt template: {e}")
        return

    # Create destination directory if it doesn't exist
    os.makedirs(args.dst, exist_ok=True)

    # Process all files in source directory
    src_path = Path(args.src)
    files = list(src_path.rglob(args.pattern))
    total_files = len(files)
    counter = 0

    for file_path in files:
        if file_path.is_file():
            counter += 1
            process_file(str(file_path), prompt_template, args.gen, args.dst, counter, total_files)
            print(f"Processed {counter}/{total_files} files")

if __name__ == "__main__":
    main()