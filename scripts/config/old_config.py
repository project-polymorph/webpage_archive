import yaml
import json
import re
import argparse
import sys

def parse_results(json_data):
    # Create dictionary to store results
    results = {}
    
    # Parse each entry in the success array
    for entry in json_data["success"]:
        try:
            # Handle both dictionary and list formats
            if isinstance(entry, dict):
                url = entry["url"]
                filename = entry["path"].split('workspace_news/')[-1]
                md5 = entry["md5"]
                title = entry.get("title", "")
                snippet = entry.get("snippet", "")
            else:  # List format
                url = entry[0]
                filename = entry[1].split('workspace_news/')[-1]
                md5 = entry[2]
                # Extract title from filename (everything after _ and before .html)
                title = re.search(r'_(.+?)\.html', filename)
                title = title.group(1) if title else ""
                snippet = ""
            
            # Store as dictionary
            results[filename] = {
                "link": url,
                "md5": md5,
                "title": title,
                "snippet": snippet
            }
        except (IndexError, KeyError) as e:
            print(f"Warning: Skipping malformed entry: {entry}")
            continue
    
    return results

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert JSON results to YAML format')
    parser.add_argument('input', help='Input JSON file path')
    parser.add_argument('output', help='Output YAML file path')
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Read input JSON
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse into desired format
        new_results = parse_results(data)
        
        # Try to load existing YAML file
        existing_results = {}
        try:
            with open(args.output, 'r', encoding='utf-8') as f:
                existing_results = yaml.safe_load(f) or {}
        except FileNotFoundError:
            pass  # File doesn't exist yet, start with empty dict
        
        # Merge existing and new results
        existing_results.update(new_results)
        
        # Write merged YAML output
        with open(args.output, 'w', encoding='utf-8') as f:
            yaml.dump(existing_results, f, allow_unicode=True, sort_keys=False)
            
        print(f"Successfully merged {args.input} into {args.output}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()