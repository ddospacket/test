from telethon import events

from .. import loader, utils

BOT_ID = 6069820430

@loader.tds
class NumberCheckerMod(loader.Module):
    """Модуль для проверки номеров через бота @FR_NoNameBot"""

    async def send_inline_choice(self, response):
        if response.reply_markup and hasattr(response.reply_markup, "rows"):
            buttons = response.reply_markup.rows
            if buttons and len(buttons) >= 1:
                for button in buttons[0].buttons:
                    if button.text == "Пробив":
                        await button.click()
                        break

    @loader.unrestricted
    @loader.ratelimit
    async def numbercmd(self, message):
        """Проверяет номер через бота @FR_NoNameBot и обновляет сообщение с результатом"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Введите номер для проверки: .number номер</b>")
            return

        number = args.strip()

        try:
            async with message.client.conversation(BOT_ID) as conv:
                await conv.send_message(number)
                response = await conv.get_response()
                await self.send_inline_choice(response)
                await message.edit(response.text)
        except Exception as e:
            await message.edit("<b>Ошибка при обращении к боту. Пожалуйста, попробуйте позже.</b>")
