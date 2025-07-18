import os
import re

# Difficulty folders + display names
difficulty_map = {
    'easy': 'Easy',
    'medium': 'Medium',
    'hard': 'Hard'
}

def extract_number_from_filename(filename):
    """Extract problem number from filename, handling various formats."""
    # Remove .py extension
    name_only = filename.replace('.py', '')
    
    # Try different patterns to extract number
    patterns = [
        r'^(\d+)_',           # Standard: 123_problem_name.py
        r'^(\d+)-',           # Alternative: 123-problem-name.py
        r'^(\d+)\.',          # Alternative: 123.problem.name.py
        r'(\d+)'              # Fallback: any number in filename
    ]
    
    for pattern in patterns:
        match = re.match(pattern, name_only)
        if match:
            return match.group(1)
    
    return None

def format_title(filename, number):
    """Extract and format title from filename."""
    name_only = filename.replace('.py', '')
    
    # Remove the number prefix with various separators
    title_part = re.sub(r'^\d+[_\-\.]\s*', '', name_only)
    
    # Convert underscores/hyphens to spaces and title case
    title = title_part.replace('_', ' ').replace('-', ' ').title()
    
    # Handle common programming terms that should have specific capitalization
    replacements = {
        'Leetcode': 'LeetCode',
        'Api': 'API',
        'Sql': 'SQL',
        'Html': 'HTML',
        'Css': 'CSS',
        'Json': 'JSON',
        'Xml': 'XML'
    }
    
    for old, new in replacements.items():
        title = title.replace(old, new)
    
    return title

try:
    # Step 1: Load README.md and extract what's already there
    if not os.path.exists('README.md'):
        print("❌ README.md not found!")
        exit(1)
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 2: Find where the table starts and ends
    table_start = content.find("## Problems by Difficulty")
    if table_start == -1:
        print("❌ Could not find '## Problems by Difficulty' section in README.md")
        exit(1)
    
    table_end = content.find("## Resources", table_start)
    if table_end == -1:
        print("❌ Could not find '## Resources' section after the problems table")
        exit(1)

    # Capture the existing sections
    before_table = content[:table_start]
    table_block = content[table_start:table_end]
    after_table = content[table_end:]

    # Step 3: Find already included problem numbers
    existing_numbers = set()
    for line in table_block.splitlines():
        # Look for table rows with problem numbers
        match = re.search(r'\|\s*(\d+)\s*\|', line)
        if match:
            existing_numbers.add(match.group(1))

    print(f"📋 Found {len(existing_numbers)} existing problems in README")

    # Step 4: Generate new rows for problems not yet in table
    new_rows = []
    processed_count = 0

    for folder, difficulty in difficulty_map.items():
        if not os.path.exists(folder):
            print(f"⚠️  Folder '{folder}' does not exist, skipping...")
            continue
        
        try:
            files = [f for f in os.listdir(folder) if f.endswith('.py')]
            print(f"📁 Processing {len(files)} Python files in '{folder}' folder")
            
            for filename in sorted(files):
                processed_count += 1
                number = extract_number_from_filename(filename)
                
                if not number:
                    print(f"⚠️  Could not extract problem number from: {filename}")
                    continue
                
                if number in existing_numbers:
                    print(f"⏭️  Problem {number} already exists in README, skipping")
                    continue
                
                title = format_title(filename, number)
                path = f"{folder}/{filename}"
                row = f"| {number} | {title} | [Link]({path}) | {difficulty} |"
                new_rows.append((int(number), row))  # Store as tuple for sorting
                
        except OSError as e:
            print(f"❌ Error reading folder '{folder}': {e}")
            continue

    # Sort new rows by problem number
    new_rows.sort(key=lambda x: x[0])
    new_row_strings = [row[1] for row in new_rows]

    # Step 5: Insert new rows before ## Resources
    if new_row_strings:
        # Handle the existing table structure (which currently has empty rows)
        table_lines = table_block.splitlines()
        
        # Find the header separator line (the line with |---|)
        header_end_idx = -1
        for i, line in enumerate(table_lines):
            if '|---|' in line or '|--' in line:
                header_end_idx = i
                break
        
        if header_end_idx == -1:
            # If no header separator found, assume basic table structure
            table_header = """## Problems by Difficulty
| # | Title | Solution | Difficulty |
|---|-------|----------|------------|"""
            updated_table = table_header + '\n' + '\n'.join(new_row_strings) + '\n\n'
        else:
            # Insert new rows after the header separator
            before_data = '\n'.join(table_lines[:header_end_idx + 1])
            # Remove any existing empty rows
            existing_data_rows = [line for line in table_lines[header_end_idx + 1:] 
                                if line.strip() and line.startswith('|') and not line.strip() == '|']
            
            all_rows = existing_data_rows + new_row_strings
            updated_table = before_data + '\n' + '\n'.join(all_rows) + '\n\n'
        
        new_content = before_table + updated_table + after_table
        
        # Write updated content
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Added {len(new_row_strings)} new problem(s) to README.md:")
        for _, row in new_rows:
            # Extract problem number and title for display
            parts = row.split('|')
            if len(parts) >= 3:
                number = str(parts[1]).strip()
                title = str(parts[2]).strip()
                print(f"   • Problem {number}: {title}")
    else:
        print("✅ No new problems to add - all existing problems are already in README.md")
        
    print(f"📊 Processed {processed_count} total files")

except FileNotFoundError as e:
    print(f"❌ File not found: {e}")
except PermissionError as e:
    print(f"❌ Permission denied: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()