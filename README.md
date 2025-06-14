🎬 Telegram Movie Search Bot
A Telegram bot that helps users search for movies and TV shows from channel posts. The bot monitors film channels, stores content information, and provides intelligent search functionality across groups and private messages.
✨ Features

Channel Monitoring: Automatically captures and indexes posts from film channels
Smart Search: Find movies and TV shows by title with fuzzy matching
Group Integration: Works seamlessly in Telegram groups with interactive responses
Private Search: Direct search functionality via private messages
User Management: Tracks group membership and manages user permissions
Admin Commands: Statistics and management tools for administrators
Interactive UI: Inline keyboards for better user experience

🏗️ Architecture
├── config.py              # Bot configuration and environment variables
├── main.py                 # Application entry point
├── db/
│   └── db.py              # Database operations (SQLite)
├── handlers/
│   ├── channel.py         # Channel post monitoring
│   ├── groups.py          # Group message handling
│   ├── private.py         # Private message handling
│   └── stats.py           # Admin statistics
└── services/
    └── post_storage.py    # Content storage and search logic
🚀 Quick Start
Prerequisites

Python 3.8+
Telegram Bot Token (from @BotFather)
Admin access to target channels/groups

Installation

Clone the repository
bashgit clone https://github.com/yourusername/telegram-movie-bot.git
cd telegram-movie-bot

Install dependencies
bashpip install -r requirements.txt

Set up environment variables
bashcp .env.example .env
# Edit .env with your configuration

Configure the bot
python# .env file
BOT_TOKEN=your_bot_token_here
FILMS_CHAT=-100xxxxxxxxx    # Channel ID for monitoring
TESTA=-100yyyyyyyyy         # Test group ID
DEST=-100zzzzzzzzz          # Destination chat ID
ADMINS_IDS=123456789        # Admin user IDs (comma-separated)

Run the bot
bashpython main.py


📋 Configuration
Environment Variables
VariableDescriptionExampleBOT_TOKENTelegram Bot API token1234567890:ABC...FILMS_CHATChannel ID to monitor for content-1001234567890TESTATest group chat ID-1001234567891DESTDestination chat ID-1001234567892ADMINS_IDSComma-separated admin user IDs123456789,987654321
Bot Permissions
The bot requires the following permissions:

In channels: Read messages
In groups: Send messages, read messages, send inline keyboards
Admin commands: Restricted to users in ADMINS_IDS

🔧 Usage
For Users
In Groups:

Mention trigger words: "movie", "film", "series", "show", etc.
Reply to bot's prompt with movie/show title
Use gratitude words for quick reactions: "thanks", "thank you", etc.

Private Messages:

Send movie/show title directly
Must be a member of configured groups

Search Examples:
User: Interstellar
Bot: 🎯 Found 3 results for 'Interstellar':
[Interstellar (2014)](https://t.me/c/1234567890/123)
[Interstellar Documentary](https://t.me/c/1234567890/124)
For Admins
Statistics Command:
/stats - View user count and bot statistics
🛠️ Development
Project Structure

config.py: Centralized configuration management
main.py: Bot initialization and polling setup
db/db.py: SQLite database operations for user management
handlers/: Message handlers split by chat type
services/: Business logic and data processing

Key Components
Database Schema:
sqlCREATE TABLE known_users (
    user_id INTEGER PRIMARY KEY
);
Content Storage:

Posts stored in data/posts.txt format: "Title: https://t.me/c/chatid/msgid"
File-based search with regex pattern matching

Adding New Features

New Handler: Create handler in appropriate handlers/ module
Register Handler: Add to dispatcher in main.py
Database Changes: Modify schema in db/db.py
Business Logic: Implement in services/ modules

📊 Monitoring & Logs

Log Files: Stored in data/bot.log with rotation (5MB max)
Log Levels: INFO level for normal operation, ERROR for issues
Monitoring: Built-in error handling with user-friendly messages

🔒 Security Features

Group Membership Validation: Users must be group members for private searches
Admin Restrictions: Sensitive commands limited to configured admins
Input Sanitization: Markdown escaping for safe message rendering
Error Isolation: Graceful error handling prevents bot crashes

🤝 Contributing

Fork the repository
Create feature branch: git checkout -b feature/amazing-feature
Commit changes: git commit -m 'Add amazing feature'
Push to branch: git push origin feature/amazing-feature
Open Pull Request

Development Guidelines

Follow PEP 8 style guidelines
Add type hints for new functions
Include error handling for external API calls
Write descriptive commit messages
Test with multiple group configurations

📝 TODO / Roadmap

 Database Migration: Replace file storage with full SQLite implementation
 Search Optimization: Add fuzzy search and ranking algorithms
 Rate Limiting: Implement user request throttling
 Caching: Add Redis for frequently searched content
 Metrics Dashboard: Web interface for bot statistics
 Multi-language: Support for multiple interface languages
 Content Validation: Verify link accessibility before storage

🐛 Known Issues

File Storage: Large posts.txt files may cause slow search performance
Memory Usage: No pagination for large result sets
Concurrent Access: File operations not thread-safe for high load

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
