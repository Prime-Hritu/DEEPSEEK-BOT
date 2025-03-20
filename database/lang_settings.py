from database import (
    check_mongo,
    MONGO,
)
from typing import Union, Optional
from pymongo.database import Database
from pymongo.collection import Collection

langdb: Optional[Union[Collection, bool]] = None

if MONGO.URI:
    db: Database = check_mongo()
    langdb = db["lang"] if db != False else False
else:
    langdb = False

VALID_LANGUAGES = ["en", "es", "fr", "de", "hi", "ru", "zh", "ar", "ja"]


def set_language(user_id, language):
    """
    Set the language preference for the user.

    Args:
        user_id: The identifier of the user.
        language: The language to set. Must be one of VALID_LANGUAGES.

    Returns:
        The language that was set if the update was successful,
        or an empty list if the language database (langdb) is unavailable.
    """
    if language not in VALID_LANGUAGES:
        raise ValueError(f"Invalid language. Choose from: {VALID_LANGUAGES}")

    if not langdb == False:
        langdb.update_one(
            {"userid": user_id},
            {"$set": {"language": language}},
            upsert=True
        )
        return language
    else:
        return []


def get_language(user_id):
    """
    Retrieve the language preference for the user.

    Args:
        user_id: The identifier of the user.

    Returns:
        The language set for the user if found, otherwise None.
    """
    if not langdb == False:
        user = langdb.find_one({"userid": user_id})
        return user["language"] if user and "language" in user else None
    else:
        return None
