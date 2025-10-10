# core/chat_history.py
import json
import os
from typing import List, Dict

class ChatHistory:
    def __init__(self, history_dir: str = "./chat_history"):
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)

    def get_history_file(self, chat_id: str) -> str:
        return os.path.join(self.history_dir, f"{chat_id}.json")

    def save_message(self, chat_id: str, role: str, content: str):
        history = self.load_history(chat_id)
        history.append({"role": role, "content": content})
        with open(self.get_history_file(chat_id), "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def load_history(self, chat_id: str) -> List[Dict[str, str]]:
        file_path = self.get_history_file(chat_id)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def clear_history(self, chat_id: str):
        file_path = self.get_history_file(chat_id)
        if os.path.exists(file_path):
            os.remove(file_path)
