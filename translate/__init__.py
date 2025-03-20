from translate.translate import translate_to_send


class Dynamic_Translate:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def translate(self, text: str):
        return translate_to_send(text, self.chat_id)
