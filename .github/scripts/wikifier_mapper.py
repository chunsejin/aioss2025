import os
import requests
import subprocess
import re
import json

API_URL = "http://www.wikifier.org/annotate-article"
API_KEY = os.environ.get("WIKIFIER_API_KEY")

def get_modified_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    files = result.stdout.strip().split('\n')
    return [f for f in files if os.path.isfile(f)]

def extract_keywords_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    words = re.findall(r'\b[a-zA-Z]{4,}\b', content)  # 길이 4 이상 단어
    return list(set(words))[:20]  # 최대 20개 추출

def call_wikifier(text):
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
        print(f"Wikifier API error: {response.status_code}")
        return {}

def main():
    print(API_KEY)
    all_keywords = set()
    for file in get_modified_files():
        print(f"Processing: {file}")
        keywords = extract_keywords_from_file(file)
        all_keywords.update(keywords)

    text_block = ' '.join(all_keywords)
    result = call_wikifier(text_block)
    if 'annotations' in result:
        for ann in result['annotations']:
            print(f"{ann['title']} => {ann['url']}")
    else:
        print("No annotations found.")

if __name__ == '__main__':
    main()
