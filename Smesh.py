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

    async def onsmeshcmd(self, message):
        """Включить фильтрацию слов"""
        self.is_filter_enabled = True
        await message.edit("Фильтрация слов включена.")

    async def offsmeshcmd(self, message):
        """Отключить фильтрацию слов"""
        self.is_filter_enabled = False
        await message.edit("Фильтрация слов отключена.")

    async def watcher(self, message):
        if isinstance(message, events.NewMessage.Incoming) and not message.is_private and self.is_filter_enabled:
            await self.filter_words(message)
