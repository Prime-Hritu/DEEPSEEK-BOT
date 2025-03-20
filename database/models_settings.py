from database import (
    check_mongo,
    MONGO,
)
from typing import Union, Any, Dict, Optional
from constants import MODELS
from pymongo.database import Database
from pymongo.collection import Collection

modelsdb: Optional[Union[Collection, bool]] = None

if MONGO.URI:
    db: Database = check_mongo()
    modelsdb = db["models"] if db != False else False
else:
    modelsdb = False


def set_ai_mode(user_id: Union[str, int], mode: MODELS) -> None:
    """
    Updates the 'ai_mode' field for the given user in the models collection.

    Args:
        user_id (Union[str, int]): The identifier of the user.
        mode (MODELS): The AI mode to be set for the user.

    Returns:
        None: This function does not return any value.
    """
    if not modelsdb == False:
        modelsdb.update_one(
            {"userid": user_id}, {"$set": {"ai_mode": mode.value}}, upsert=True
        )


def get_ai_mode(user_id: Union[str, int]) -> Union[str, bool]:
    """
    Retrieves the 'ai_mode' for the given user from the models collection.

    Args:
        user_id (Union[str, int]): The identifier of the user.
    """
    if not modelsdb == False:
        user: Optional[Dict[str, Any]] = modelsdb.find_one({"userid": user_id})
        if user and "ai_mode" in user:
            return user["ai_mode"]
        else:
            return None
    else:
        return None
