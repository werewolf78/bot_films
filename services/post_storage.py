import os
import re
from config import POSTS_FILE

def add_post_to_file(description: str, chat_id: int, post_id: int):
    url = f"https://t.me/c/{str(chat_id)[4:]}/{post_id}"
    with open(POSTS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{description}: {url}\n")

def find_post_lines_by_title(title: str):
    matches = []
    if not os.path.exists(POSTS_FILE):
        return matches
    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if title.lower() in line.lower() and re.search(r'https://t\.me/c/\d+/[\d?]*', line):
                matches.append(line.strip())
    return matches
