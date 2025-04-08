import os
import requests
import subprocess
import re

API_KEY = os.environ.get("WIKIFIER_API_KEY")
API_URL = "http://www.wikifier.org/annotate-article"

def get_modified_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        stdout=subprocess.PIPE,
        text=True,
    )
    files = result.stdout.strip().split('\n')
    return [f for f in files if os.path.isfile(f) and (f.endswith('.py') or f.endswith('.md'))]

def extract_keywords_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
    return list(set(words))[:30]  # 최대 30개 키워드

def call_wikifier(text):
    if not API_KEY:
        print("WIKIFIER_API_KEY is not set.")
        return {}

    response = requests.post(API_URL, data={
        'text': text,
        'lang': 'en',
        'userKey': API_KEY,
        'pageRankSqThreshold': '0.8',
        'applyPageRankSqThreshold': 'true',
        'support': 'true',
        'ranges': 'false',
        'nTopDfValuesToIgnore': '200',
        'fastMode': 'true'
    })

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Wikifier API returned status {response.status_code}")
        return {}

def main():
    modified_files = get_modified_files()
    if not modified_files:
        print("No modified files detected.")
        return

    all_keywords = set()
    for file in modified_files:
        print(f"Processing file: {file}")
        keywords = extract_keywords_from_file(file)
        all_keywords.update(keywords)

    if not all_keywords:
        print("No keywords extracted.")
        return

    text_block = ' '.join(all_keywords)
    result = call_wikifier(text_block)
    if 'annotations' in result:
        for ann in result['annotations']:
            print(f"{ann['title']} => {ann['url']}")
    else:
        print("No annotations found.")

if __name__ == '__main__':
    main()
