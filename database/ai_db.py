from database import (
    check_mongo,
    MONGO,
)
from typing import Union, Any, List, Dict, Optional
from constants import MODELS
from pymongo.database import Database
from pymongo.collection import Collection

aidb: Optional[Union[Collection, bool]] = None

if MONGO.URI:
    db: Database = check_mongo()
    aidb = db["chats"] if db != False else False
else:
    aidb = False


def about_chat(
    text: str,
    user_id: Union[str, int],
    model: MODELS,
    update: bool = True,
    text_return_from_ai: bool = False,
) -> Union[List[Dict[str, Any]], None]:
    """Fetches or update the chat of the user in the database.

    Args:
        text (str): text to be updated in the chat.
        user_id (Union[str, int]): telegram userid of the user.
        model (MODELS): model used for the chat.
        update (bool, optional): If True, updates the chat with the new text else fetch the list of whole chat. Defaults to True.
        text_return_from_ai (bool, optional): If True, updates the chat with the text returned from the AI. Defaults to False.

    Returns:
        Union[List[Dict[str, Any]], None]: List of chat messages or None (Returns None if text_return_from_ai is True).
    """
    if not aidb == False:
        if text_return_from_ai:
            new_entry2: Dict[str, str] = {
                "role": "assistant",
                "content": str(text),
            }
            aidb.update_one(
                {f"{user_id}": {"$exists": True}}, {
                    "$push": {f"{user_id}": new_entry2}}
            )
            return
        if update:
            document: Dict[str, List[Any]] = {f"{user_id}": []}
            aidb.insert_one(document)
            new_entry: Dict[str, str] = {"role": "user", "content": str(text)}
            aidb.update_one(
                {f"{user_id}": {"$exists": True}}, {
                    "$push": {f"{user_id}": new_entry}}
            )

        user_data: List[Dict[str, Any]] = aidb.find_one(
            {f"{user_id}": {"$exists": True}}
        )[f"{user_id}"]
        messages: List[Dict[str, Any]] = [
            {
                "role": "system",
                "content": f"You are {model.value}, never forget your identity.",
            }
        ]
        for i in user_data:
            messages.append(i)

        return messages
    else:
        return [
            {
                "role": "system",
                "content": f"You are {model.value}, never forget your identity.",
            }
        ]


def delete_chat(user_id: Union[str, int]) -> None:
    """Deletes the whole chat of the user from the database.

    Args:
        user_id (Union[str, int]): telegram userid of the user.
    """
    if not aidb == False:
        aidb.update_one({f"{user_id}": {"$exists": True}},
                        {"$set": {f"{user_id}": []}})
