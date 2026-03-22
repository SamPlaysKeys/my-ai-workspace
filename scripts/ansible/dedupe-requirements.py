#!/usr/bin/env python3
"""Remove duplicate entries from Ansible requirements.yml files."""
import sys
import yaml

def dedupe(items):
    """Remove duplicates based on name+version, return (unique, duplicates)."""
    seen, unique, dupes = set(), [], []
    for item in items:
        key = (item.get('name'), item.get('version'))
        (dupes if key in seen else unique).append(item)
        seen.add(key)
    return unique, dupes

def main():
    if len(sys.argv) < 2 or '-h' in sys.argv:
        print(f"Usage: {sys.argv[0]} <requirements.yml> [--dry-run]")
        sys.exit(0 if '-h' in sys.argv else 1)
    
    filename, dry_run = sys.argv[1], '--dry-run' in sys.argv
    data = yaml.safe_load(open(filename))
    
    if not data:
        print("Empty file"); sys.exit(0)
    
    all_dupes = []
    if isinstance(data, list):
        data, dupes = dedupe(data)
        all_dupes.extend(('root', d) for d in dupes)
    else:
        for section, items in data.items():
            if isinstance(items, list):
                data[section], dupes = dedupe(items)
                all_dupes.extend((section, d) for d in dupes)
    
    if not all_dupes:
        print("No duplicates found."); sys.exit(0)
    
    print(f"Found {len(all_dupes)} duplicate(s):")
    for section, item in all_dupes:
        print(f"  - {item.get('name')} (version: {item.get('version', 'unspecified')}) [{section}]")
    
    if dry_run:
        print("\n[DRY RUN] No changes made.")
    else:
        yaml.safe_dump(data, open(filename, 'w'), default_flow_style=False, sort_keys=False)
        print(f"\nRemoved {len(all_dupes)} duplicate(s) from {filename}")

if __name__ == '__main__':
    main()
