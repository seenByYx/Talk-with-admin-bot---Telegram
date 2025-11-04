Here is a **README.md** template for your Telegram forwarding & broadcast bot project:

***

# Telegram Forwarding & Broadcast Bot

A simple and efficient **Telegram bot** using `python-telegram-bot` for forwarding user messages to an admin, replying privately, and broadcasting announcements to all users.

## Features

- **Automatic Forwarding:** User messages (text, media, stickers, etc.) are forwarded to the admin chat.
- **Admin Replies:** Admin replies are sent back to the correct user, maintaining privacy and threaded conversation.
- **Broadcast Mode:** The admin can broadcast messages or media to all users using the `/broadcast` command.
- **User Persistence:** User IDs are collected and stored in `users.json` for broadcasting and analytics.
- **Donation Command:** `/donate` shares ways users can support the bot (UPI, Razorpay links, etc.).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```
2. Install dependencies:
   ```bash
   pip install python-telegram-bot
   ```
3. Set up your environment:
   - Insert your Telegram bot token into `BOT_TOKEN`.
   - Set your Telegram chat ID as `ADMIN_CHAT_ID` in the script.
4. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `/start` — Start interacting; new users are registered.
- `/donate` — Shows support options for development.
- `/broadcast` — Admin-only; send announcements or media to all users.

## License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

## Contributing

Contributions, suggestions, and issue reports are welcome. Please submit a pull request or open an issue on GitHub.

## Credits

Made with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
