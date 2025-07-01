import json
import os
from utils.cache_manager import cache_iso_standards, get_cached_iso_standards

def precache_iso_standards():
    """
    Loads ISO 27002 standards from the JSON file and caches them.
    """
    # Check if standards are already cached
    if get_cached_iso_standards():
        print("ISO standards are already cached.")
        return

    print("Attempting to cache ISO standards...")
    standards_path = os.path.join('iso_standards', 'iso27002.json')
    
    try:
        with open(standards_path, 'r') as f:
            data = json.load(f)
            standards = {k: v for k, v in data.items() if k != 'metadata'}
            
            # Cache the loaded standards
            cache_iso_standards(standards)
            print("Successfully cached ISO 27002 standards.")
            
    except FileNotFoundError:
        print(f"Error: ISO standards file not found at {standards_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    precache_iso_standards()
