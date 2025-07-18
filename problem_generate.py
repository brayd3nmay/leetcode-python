#!/usr/bin/env python3
"""
LeetCode Problem Generator
Creates Python files with proper template structure from LeetCode URLs
"""

import requests
import re
import json
import os
import sys
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_problem_slug_from_url(url):
    """Extract problem slug from LeetCode URL"""
    # Handle different URL formats
    if '/problems/' in url:
        slug = url.split('/problems/')[1].rstrip('/')
        return slug
    else:
        raise ValueError("Invalid LeetCode URL format")

def try_graphql_approach(problem_slug):
    """Try to get problem data using LeetCode's GraphQL API"""
    graphql_url = "https://leetcode.com/graphql"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Referer': 'https://leetcode.com/',
        'Origin': 'https://leetcode.com',
    }
    
    query = {
        "query": """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                difficulty
                content
                codeSnippets {
                    lang
                    langSlug
                    code
                }
            }
        }
        """,
        "variables": {"titleSlug": problem_slug}
    }
    
    try:
        response = requests.post(graphql_url, json=query, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and data['data']['question']:
            return data['data']['question']
        
    except Exception as e:
        print(f"GraphQL approach failed: {e}")
        
    return None

def generate_leetcode_problem(url):
    """Generate LeetCode problem data from problem URL"""
    
    # Extract problem slug from URL
    problem_slug = get_problem_slug_from_url(url)
    
    # Try GraphQL approach first
    print(f"🔍 Attempting to fetch problem data for: {problem_slug}")
    problem_data = try_graphql_approach(problem_slug)
    
    if problem_data:
        print("✅ Successfully fetched via GraphQL API")
        # Extract Python code template
        python_code = ""
        if 'codeSnippets' in problem_data:
            for snippet in problem_data['codeSnippets']:
                if snippet.get('langSlug') == 'python3':
                    python_code = snippet['code']
                    break
        
        # If no code snippets found, create a basic template
        if not python_code:
            python_code = "class Solution:\n    def solution(self):\n        pass"
        
        return {
            'number': problem_data.get('questionFrontendId', ''),
            'title': problem_data.get('title', ''),
            'difficulty': problem_data.get('difficulty', 'Medium'),
            'code': python_code,
            'url': url
        }
    
    # If GraphQL fails, try multiple web approaches
    print("🔄 GraphQL failed, trying web extraction...")
    
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    for attempt in range(3):
        try:
            # Use random user agent
            user_agent = random.choice(user_agents)
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            })
            
            # Add random delay
            time.sleep(random.uniform(1, 3))
            
            print(f"🔄 Attempt {attempt + 1}: Fetching {url}")
            response = session.get(url, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple parsing approaches
            problem_data = None
            
            # Approach 1: Look for JSON data in script tags
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'questionData' in script.string:
                    json_matches = [
                        re.search(r'questionData":(.*?),"isPremium"', script.string),
                        re.search(r'questionData":(.*?),"solution"', script.string),
                        re.search(r'questionData":(.*?),"topicTags"', script.string),
                        re.search(r'questionData":(.*?),"hints"', script.string),
                    ]
                    
                    for json_match in json_matches:
                        if json_match:
                            try:
                                problem_data = json.loads(json_match.group(1))
                                break
                            except json.JSONDecodeError:
                                continue
                    
                    if problem_data:
                        break
            
            # Approach 2: Look for __NEXT_DATA__ or similar
            if not problem_data:
                for script in script_tags:
                    if script.string and '__NEXT_DATA__' in script.string:
                        try:
                            json_str = script.string.split('__NEXT_DATA__')[1].split('</script>')[0].strip()
                            if json_str.startswith('='):
                                json_str = json_str[1:].strip()
                            next_data = json.loads(json_str)
                            
                            # Navigate through the data structure
                            if 'props' in next_data and 'pageProps' in next_data['props']:
                                page_props = next_data['props']['pageProps']
                                if 'dehydratedState' in page_props:
                                    queries = page_props['dehydratedState'].get('queries', [])
                                    for query in queries:
                                        if 'state' in query and 'data' in query['state']:
                                            data = query['state']['data']
                                            if 'question' in data:
                                                problem_data = data['question']
                                                break
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
            
            # Approach 3: Fallback to title parsing
            if not problem_data:
                title_elem = soup.find('title')
                if title_elem:
                    title_text = title_elem.get_text()
                    match = re.match(r'(\d+)\.\s*(.*?)\s*-\s*LeetCode', title_text)
                    if match:
                        number = match.group(1)
                        title = match.group(2)
                        
                        # Try to get difficulty from various selectors
                        difficulty = "Medium"  # Default
                        
                        # Try different selectors for difficulty
                        diff_selectors = [
                            'div[data-e2e-locator="console-question-difficulty"]',
                            'div:contains("Easy")',
                            'div:contains("Medium")', 
                            'div:contains("Hard")',
                            '[class*="difficulty"]',
                            'span[class*="difficulty"]'
                        ]
                        
                        for selector in diff_selectors:
                            try:
                                diff_elem = soup.select_one(selector)
                                if diff_elem:
                                    text = diff_elem.get_text().strip()
                                    if any(d in text for d in ['Easy', 'Medium', 'Hard']):
                                        for d in ['Easy', 'Medium', 'Hard']:
                                            if d in text:
                                                difficulty = d
                                                break
                                        break
                            except:
                                continue
                        
                        problem_data = {
                            'questionFrontendId': number,
                            'title': title,
                            'difficulty': difficulty,
                            'codeSnippets': []
                        }
            
            if problem_data:
                print("✅ Successfully extracted problem data")
                
                # Extract Python code template
                python_code = ""
                if 'codeSnippets' in problem_data:
                    for snippet in problem_data['codeSnippets']:
                        if snippet.get('langSlug') == 'python3':
                            python_code = snippet['code']
                            break
                
                # If no code snippets found, create a basic template
                if not python_code:
                    python_code = "class Solution:\n    def solution(self):\n        pass"
                
                return {
                    'number': problem_data.get('questionFrontendId', ''),
                    'title': problem_data.get('title', ''),
                    'difficulty': problem_data.get('difficulty', 'Medium'),
                    'code': python_code,
                    'url': url
                }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < 2:  # Don't sleep on last attempt
                time.sleep(random.uniform(2, 5))
            continue
        except Exception as e:
            print(f"❌ Parsing error on attempt {attempt + 1}: {e}")
            if attempt < 2:
                time.sleep(random.uniform(2, 5))
            continue
    
    # If all attempts fail, try to extract basic info from URL
    print("⚠️  All extraction attempts failed, parsing basic info from URL...")
    
    try:
        # Extract problem number and title from URL slug
        slug = get_problem_slug_from_url(url)
        
        # Try to extract number from slug
        number_match = re.search(r'^(\d+)', slug)
        if number_match:
            number = number_match.group(1)
            # Convert slug to title
            title = slug.split('-', 1)[1] if '-' in slug else slug
            title = title.replace('-', ' ').title()
        else:
            # No number found, just use slug as title
            number = "1"
            title = slug.replace('-', ' ').title()
        
        print(f"📝 Extracted from URL: {number}. {title}")
        
        return {
            'number': number,
            'title': title,
            'difficulty': 'Medium',  # Default
            'code': 'class Solution:\n    def solution(self):\n        pass',
            'url': url
        }
        
    except Exception as e:
        print(f"❌ Failed to extract from URL: {e}")
        
        # Final fallback
        return {
            'number': '1',
            'title': 'Unknown Problem',
            'difficulty': 'Medium',
            'code': 'class Solution:\n    def solution(self):\n        pass',
            'url': url
        }



def sanitize_filename(title):
    """Convert title to filename-friendly format"""
    # Convert to lowercase and replace spaces with underscores
    filename = title.lower().replace(' ', '_')
    # Remove special characters except underscores
    filename = re.sub(r'[^a-z0-9_]', '', filename)
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    return filename

def get_difficulty_folder(difficulty):
    """Get the appropriate folder for the difficulty level"""
    difficulty_map = {
        'Easy': 'easy',
        'Medium': 'medium', 
        'Hard': 'hard'
    }
    return difficulty_map.get(difficulty, 'medium')

def extract_imports_from_code(code):
    """Extract necessary imports from the code template"""
    imports = []
    
    # Check for common type hints
    if 'List[' in code:
        imports.append('from typing import List')
    if 'Optional[' in code:
        if 'from typing import List' not in imports:
            imports.append('from typing import List, Optional')
        else:
            imports[0] = 'from typing import List, Optional'
    if 'TreeNode' in code:
        imports.append('# Definition for a binary tree node.')
        imports.append('# class TreeNode:')
        imports.append('#     def __init__(self, val=0, left=None, right=None):')
        imports.append('#         self.val = val')
        imports.append('#         self.left = left')
        imports.append('#         self.right = right')
    if 'ListNode' in code:
        imports.append('# Definition for singly-linked list.')
        imports.append('# class ListNode:')
        imports.append('#     def __init__(self, val=0, next=None):')
        imports.append('#         self.val = val')
        imports.append('#         self.next = next')
    
    return imports

def generate_file_content(problem_data):
    """Generate the complete file content with template"""
    number = problem_data['number']
    title = problem_data['title']
    difficulty = problem_data['difficulty']
    code = problem_data['code']
    url = problem_data['url']
    
    # Get current date
    current_date = datetime.now().strftime('%m/%d/%Y')
    
    # Generate header
    header = f"# Problem: {number}. {title}\n"
    header += f"# Difficulty: {difficulty}\n"
    header += f"# Link: {url}\n"
    header += f"# Date: {current_date}\n\n"
    
    # Get imports
    imports = extract_imports_from_code(code)
    import_section = ""
    if imports:
        import_section = "\n".join(imports) + "\n\n"
    
    # Combine everything
    content = header + import_section + code
    
    return content

def create_leetcode_file(url):
    """Main function to create LeetCode file from URL"""
    # Extract problem data
    print(f"Generating LeetCode problem from: {url}")
    problem_data = generate_leetcode_problem(url)
    
    # Generate filename
    number = problem_data['number']
    title = problem_data['title']
    sanitized_title = sanitize_filename(title)
    filename = f"{number}_{sanitized_title}.py"
    
    # Get difficulty folder
    difficulty_folder = get_difficulty_folder(problem_data['difficulty'])
    
    # Create directory if it doesn't exist
    os.makedirs(difficulty_folder, exist_ok=True)
    
    # Full file path
    file_path = os.path.join(difficulty_folder, filename)
    
    # Generate file content
    content = generate_file_content(problem_data)
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {file_path}")
    print(f"📝 Problem: {number}. {title}")
    print(f"🔥 Difficulty: {problem_data['difficulty']}")
    
    return file_path

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create LeetCode problem file from URL')
    parser.add_argument('url', help='LeetCode problem URL')
    parser.add_argument('--number', '-n', help='Problem number (skips problem generation)')
    parser.add_argument('--title', '-t', help='Problem title (skips problem generation)')
    parser.add_argument('--difficulty', '-d', choices=['Easy', 'Medium', 'Hard'], 
                       help='Problem difficulty (skips problem generation)')
    parser.add_argument('--code', '-c', help='Code template (skips problem generation)')
    
    args = parser.parse_args()
    
    # If all manual arguments provided, skip problem generation
    if args.number and args.title and args.difficulty:
        problem_data = {
            'number': args.number,
            'title': args.title,
            'difficulty': args.difficulty,
            'code': args.code or "class Solution:\n    def solution(self):\n        pass",
            'url': args.url
        }
        
        # Generate filename
        sanitized_title = sanitize_filename(args.title)
        filename = f"{args.number}_{sanitized_title}.py"
        
        # Get difficulty folder
        difficulty_folder = get_difficulty_folder(args.difficulty)
        
        # Create directory if it doesn't exist
        os.makedirs(difficulty_folder, exist_ok=True)
        
        # Full file path
        file_path = os.path.join(difficulty_folder, filename)
        
        # Generate file content
        content = generate_file_content(problem_data)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")
        print(f"📝 Problem: {args.number}. {args.title}")
        print(f"🔥 Difficulty: {args.difficulty}")
        
    else:
        create_leetcode_file(args.url)

if __name__ == "__main__":
    main() 