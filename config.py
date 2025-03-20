import os
from dotenv import load_dotenv

load_dotenv()


class MONGO:
    """
    URI: MongoDB Url (optional)
    NAME: MongoDB collection name (optional)
    """

    URI = os.environ.get(
        "MONGO_URI",
        "",
    )
    NAME = os.environ.get("MONGO_NAME", "Deepseek")


class HUGGINGFACE:
    API_KEY = os.environ.get(
        "HUGGINGFACE", "")


class BOT:
    """
    TOKEN: Bot token generated from @BotFather
    SOURCE: Source code's url of the bot
    """

    TOKEN = os.environ.get("TOKEN", "")
    SOURCE = "https://github.com/prime-hritu"


class API:
    """
    HASH: Telegram API hash from https://my.telegram.org
    ID = Telegram API ID from https://my.telegram.org
    """

    HASH = os.environ.get("API_HASH", "")
    ID = int(os.environ.get("API_ID", 0))


class FORCE:
    """
    FORCE_SUB: True or False
    CHANNEL_LINK: Force sub channel link as url.
    CHANNEL_USERNAME: Force sub channel username with @
    """

    FORCE_SUB = os.environ.get("FORCE", "")
    FORCE_BOOL = True if str(FORCE_SUB).lower() == "true" else False
    # https://t.me/Private_Bots
    CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "")
    CHANNEL_USERNAME = os.environ.get(
        "CHANNEL_USERNAME", ""
    )  # with @ ( @Private_Bots )


class OWNER:
    """
    ID: Owner's user id, get it from @userinfobot
    """

    ID = int(os.environ.get("OWNER", 0))


class WEB:
    """
    PORT: Specific port no. on which you want to run your bot, DON'T TOUCH IT IF YOU DON'T KNOW WHAT IS IT.
    """

    PORT = int(os.environ.get("PORT", 8000))  # 8000 port for koyeb
