import os
from requests import RequestException
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from main import get_repos


TOKEN = os.environ.get("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Hello! Your bot is working.\nUse /repos <username>"
    )


async def repos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_message.reply_text(
            "Please provide a GitHub username.\nExample: /repos Pulkit2007"
        )
        return

    username = context.args[0]

    try:
        repositories = get_repos(username)
    except RequestException:
        await update.effective_message.reply_text(
            "GitHub could not be reached or the username does not exist."
        )
        return

    if not repositories:
        await update.effective_message.reply_text(
            f"{username} has no public repositories."
        )
        return

    repository_names = "\n".join(
        f"- {repository['name']}" for repository in repositories
    )
    await update.effective_message.reply_text(
        f"Repositories for {username}:\n{repository_names}"
    )


async def get_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_message.reply_text(
            "Pls Provide a username for github repo!"
        )
        return

    username = context.args[0]


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("repos", repos))

    app.run_polling()


if __name__ == "__main__":
    main()
