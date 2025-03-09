import os
import argparse
import tempfile
import subprocess
import logging
from pathlib import Path
import multiprocessing
from functools import partial
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global args variable to be accessible by all processes
args = None

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

def process_file(file_path, prompt_template, gen_script_path, output_dir, total_files, process_idx):
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
    
    # Print input content
    print(f"Process {process_idx} - input_content:")
    print("============================================")
    print(input_content)
    print("============================================")
    
    # Create directory for output file if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
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
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check if there was a Gemini API error
        if "Gemini API error" in result.stdout or "PROHIBITED_CONTENT" in result.stdout:
            logging.warning(f"Process {process_idx} - Gemini API error for {file_path}, skipping this file")
            print(f"Process {process_idx} - Gemini API error:")
            print("============================================")
            print(result.stdout)
            print("============================================")
            # Remove the output file if it was partially created
            if os.path.exists(output_path):
                os.remove(output_path)
            return True  # Return True to indicate we handled this case and want to continue
        
        # If there was any other error
        if result.returncode != 0:
            logging.error(f"Error processing {file_path}: {result.stderr}")
            return False
        
        # Log progress
        logging.info(f"Process {process_idx} - Successfully processed {file_path} -> {output_path}")
        
        # Check if output file exists before trying to read it
        if os.path.exists(output_path):
            # Print output content
            output_content = read_file_content(output_path)
            print(f"Process {process_idx} - output_content:")
            print("============================================")
            print(output_content)
            print("============================================")
        else:
            logging.warning(f"Process {process_idx} - Output file not created: {output_path}")
        
        return True

    except Exception as e:
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

def worker(args_tuple):
    """Worker function for multiprocessing that unpacks arguments and calls process_file."""
    idx, (file_path, prompt_template, gen_script_path, output_dir, total_files) = args_tuple
    try:
        # Ensure output directory exists before processing
        rel_path = os.path.relpath(file_path, start=args.src)
        output_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        return process_file(file_path, prompt_template, gen_script_path, output_dir, total_files, idx)
    except FileNotFoundError as e:
        logging.error(f"Process {idx} - FileNotFoundError: {e}")
        return False
    except Exception as e:
        logging.error(f"Process {idx} - Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Process files using a prompt template')
    parser.add_argument('src', help='Source directory containing input files')
    parser.add_argument('dst', help='Destination directory for output files')
    parser.add_argument('prompt', help='Path to prompt template file')
    parser.add_argument('--gen', help='Path to gen.py script', default='scripts/ai/gen.py')
    parser.add_argument('--pattern', default='*.*', help='File pattern to match (default: *.*)')
    parser.add_argument('--skip-size-check', action='store_true', default=True, help='Skip initial file size check (default: True)')
    parser.add_argument('--processes', type=int, default=1, help='Number of parallel processes to use (default: 16)')

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
    files = [str(file_path) for file_path in src_path.rglob(args.pattern) if file_path.is_file()]
    total_files = len(files)
    
    logging.info(f"Found {total_files} files to process using {args.processes} parallel processes")
    
    # Prepare arguments for each file
    file_args = [(file_path, prompt_template, args.gen, args.dst, total_files) for file_path in files]
    # Add process index to each argument tuple
    indexed_args = list(enumerate(file_args))
    
    # Process files in parallel
    start_time = time.time()
    try:
        with multiprocessing.Pool(processes=min(args.processes, len(files))) as pool:
            results = list(pool.map(worker, indexed_args))
    except Exception as e:
        logging.error(f"Error during parallel processing: {e}")
        results = []
    
    # Calculate statistics
    end_time = time.time()
    elapsed_time = end_time - start_time
    successful = sum(1 for result in results if result)
    
    # Log summary
    logging.info(f"Processing complete in {elapsed_time:.2f} seconds.")
    logging.info(f"Successfully processed {successful}/{total_files} files.")
    if total_files > 0:
        logging.info(f"Average processing time: {elapsed_time/total_files:.2f} seconds per file.")

if __name__ == "__main__":
    main()