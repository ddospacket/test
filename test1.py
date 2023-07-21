from telethon import events, custom

from .. import loader, utils

# Замените XXXXXXXXX на айди бота @FR_NoNameBot
BOT_ID = 6069820430

@loader.tds
class NumberCheckerMod(loader.Module):
    """Модуль для проверки номеров через бота @FR_NoNameBot"""

    def __init__(self):
        self.name = "NumberChecker"
        self.is_processing = False

    async def get_bot_response(self, number):
        try:
            async with self.client.conversation(BOT_ID) as conv:
                await conv.send_message(f"/number {number}")
                response = await conv.get_response()
                return response
        except Exception as e:
            return None

    async def send_inline_choice(self, response):
        if response.reply_markup and isinstance(response.reply_markup, custom.InlineKeyboard):
            buttons = response.reply_markup.rows
            if buttons and len(buttons) >= 1:
                await response.click(0)

    @loader.unrestricted
    @loader.ratelimit
    async def numbercmd(self, message):
        """Проверяет номер через бота @FR_NoNameBot и обновляет сообщение с результатом"""
        if self.is_processing:
            await message.edit("<b>Запрос уже обрабатывается. Пожалуйста, подождите.</b>")
            return

        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Введите номер для проверки: .number номер</b>")
            return

        number = args.strip()
        result = ""

        for _ in range(10):
            response = await self.get_bot_response(number)
            if not response:
                await message.edit("<b>Ошибка при обращении к боту. Пожалуйста, попробуйте позже.</b>")
                return

            result = response.text
            await self.send_inline_choice(response)

            # Ждем 3 секунды перед следующей проверкой
            await asyncio.sleep(3)

        await message.edit(result)
        self.is_processing = False
