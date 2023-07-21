from telethon import events

from .. import loader, utils

BOT_ID = 1022435554

@loader.tds
class OldNameCheckerMod(loader.Module):
    """Модуль для проверки старых имен в VK через бота проверки"""

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
    async def idcmd(self, message):
        """Проверяет старое имя в VK через бота проверки и обновляет сообщение с результатом"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Введите старое имя для проверки: .id имя</b>")
            return

        name = args.strip()

        try:
            async with message.client.conversation(BOT_ID) as conv:
                await conv.send_message(name)
                response = await conv.get_response()
                await self.send_inline_choice(response)
                await message.edit(response.text)
        except Exception as e:
            await message.edit("<b>Ошибка при обращении к боту. Пожалуйста, попробуйте позже.</b>")
