import yaml
import argparse
import sys
from pathlib import Path

def merge_visit_data(visit_links_path, config_path, output_path):
    # Read visit_links.yml
    try:
        with open(visit_links_path, 'r', encoding='utf-8') as f:
            visit_data = yaml.safe_load(f)
        print(f"Loaded visit data with {len(visit_data)} entries")
    except Exception as e:
        print(f"Error reading visit_links.yml: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Read config.yml if it exists
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"Loaded config with {len(config)} entries")
    except FileNotFoundError:
        config = {}  # Start with empty dict if file doesn't exist
        print("No existing config found, starting fresh")
    except Exception as e:
        print(f"Error reading config.yml: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Update config with visit data
    updates = 0
    for md5, data in visit_data.items():
        for config_url, config_data in config.items():
            if config_data.get('md5') == md5:
                print(f"Found match! Updating {config_url}")
                config_data.update({
                    'snippet': data.get('snippet', ''),
                    'title': data.get('title', ''),
                    'visited_date': data.get('visited_date', '')
                })
                updates += 1
                break

    print(f"Completed with {updates} updates")

    # Write updated config
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)
        print(f"Successfully updated {output_path} with visit data")
    except Exception as e:
        print(f"Error writing output file: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Merge visit_links data into config.yml')
    parser.add_argument('--visit-links', default='../../visit_links.yml',
                      help='Path to visit_links.yml file')
    parser.add_argument('config', 
                      help='Path to input config.yml file')

    args = parser.parse_args()

    # Ensure input files exist
    if not Path(args.visit_links).exists():
        print(f"Error: visit_links file not found: {args.visit_links}", file=sys.stderr)
        sys.exit(1)

    # Use config path as both input and output
    merge_visit_data(args.visit_links, args.config, args.config)

if __name__ == "__main__":
    main()