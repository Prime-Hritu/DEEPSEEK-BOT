from typing import Union, List, Dict, Any
from constants import MODELS
from config import HUGGINGFACE
from database.ai_db import about_chat
from huggingface_hub import InferenceClient


class DEEPSEEK:
    def __init__(self) -> None:
        pass

    def huggingface(self, text: str, user_id: Union[str, int], model: MODELS) -> str:
        old_chats_including_current_one: List[Dict[str, Any]] = about_chat(
            text, user_id, model
        )
        api: str = HUGGINGFACE.API_KEY
        client: InferenceClient = InferenceClient(
            provider="together",
            api_key=api,
        )
        completion: Any = client.chat.completions.create(
            model=model.value, messages=old_chats_including_current_one, max_tokens=500
        )
        text: str = completion.choices[0].message.content
        about_chat(text, user_id, model, text_return_from_ai=True)
        text = str(text).replace("<think>", "<i>").replace("</think>", "</i>")
        return text
