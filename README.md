# Book Club Discord Bot

<p align="middle">
<img width="300px" src="https://github.com/hi-rachel/X/assets/103404125/a5ddae76-7940-4335-bcf4-069ac7f5c2e3">
</p>

> A Discord bot for managing a developer book club where members gather to study or read development books together.

This bot was created to automate attendance checks when using Discord for study sessions at specific days and times. By creating and setting up an app through [discord.dev](https://discord.com/developers/docs/quick-start/getting-started), downloading this code, and modifying the environment variables to match your conditions, you can conduct attendance checks tailored to each study session.

## Setup

1. Clone the repository and navigate to the project directory.

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a virtual environment:
   > If Python is not installed on your system, download and install it from the [official Python website](https://www.python.org/downloads/).
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies

   ```bash
    pip install -r requirements.txt
   ```

4. Set up your environment variables in a .env file. Here is an example:

   ```json
   DISCORD_TOKEN=your_discord_bot_token
   TARGET_DAYS=Sunday,Monday
   TARGET_HOUR=21
   TARGET_MINUTE=00
   ```

5. Run the bot
   ```bash
    python bot.py
   ```

---

## Inquiry

For [bug reports](https://github.com/hi-rachel/discord-study-bot/issues), improvement suggestions, or inquiries about joining the developer book reading study(📚 모각북클럽), please email 📬 rachel.uiux@gmail.com.

---

## License

This repository is MIT licensed.
