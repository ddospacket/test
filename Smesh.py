import re
from telethon import events, utils

@loader.tds
class WordFilterMod(loader.Module):
    """Модуль для фильтрации слов в чате"""

    def __init__(self):
        self.words_to_filter = ["смиш", "смеш", "smesh"]
        self.is_filter_enabled = False

    async def filter_words(self, message):
        text = utils.get_display_name(message.sender) + ":\n" + message.text
        for word in self.words_to_filter:
            if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                await message.delete()
                break

    async def client_ready(self, client, db):
        self.client = client

    async def toggle_filter(self, message):
        args = utils.get_args_raw(message).strip()
        if args == "on":
            self.is_filter_enabled = True
            await message.edit("Фильтрация слов включена.")
        elif args == "off":
            self.is_filter_enabled = False
            await message.edit("Фильтрация слов отключена.")
        else:
            await message.edit("Используйте команды /onsmesh или /offsmesh для включения и отключения фильтрации.")

    async def watcher(self, message):
        if isinstance(message, events.NewMessage.Incoming) and not message.is_private and self.is_filter_enabled:
            await self.filter_words(message)
