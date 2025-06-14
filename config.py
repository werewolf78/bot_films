
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TESTA = int(os.getenv("TESTA", 0))
FILMS_CHAT = int(os.getenv("FILMS_CHAT", 0))
POSTS_FILE = "data/posts.txt"
DEST = int(os.getenv("DEST"))