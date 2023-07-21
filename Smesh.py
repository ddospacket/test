import re
from telethon import events, utils

@loader.tds
class WordFilterMod(loader.Module):
    """Модуль для фильтрации слов в чате смиша"""

    def __init__(self):
        self.words_to_filter = ["смиш", "смеш", "smesh"]

    async def filter_words(self, message):
        text = utils.get_display_name(message.sender) + ":\n" + message.text
        for word in self.words_to_filter:
            if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                await message.delete()
                break

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message):
        if isinstance(message, events.NewMessage.Incoming) and not message.is_private:
            await self.filter_words(message)
