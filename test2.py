from telethon import events

@client.on(events.NewMessage(pattern=r'\.number (.+)'))
async def handle_number(event):
    number = event.pattern_match.group(1)
    await event.edit(f"Waiting... {number}")

    bot_id = 6069820430
    bot_username = "FR_NoNameBot"

    # Отправляем запрос с номером на бота
    response = await client.inline_query(bot_username, number)

    # Проверяем, что есть инлайн кнопки в ответе
    if not response or len(response) == 0:
        await event.edit("Ошибка: Нет доступных инлайн кнопок.")
        return

    # Выбираем определенную инлайн кнопку
    button_to_click = response[1]  # Индекс кнопки, которую хотим выбрать (нумерация с 0)

    # Нажимаем выбранную инлайн кнопку
    result = await button_to_click.click()
    await asyncio.sleep(3)  # Пауза 3 секунды перед выбором следующей инлайн кнопки

    # Проверяем, что после первого нажатия появились новые инлайн кнопки
    if not result or len(result) == 0:
        await event.edit("Ошибка: Нет доступных инлайн кнопок для продолжения.")
        return

    # Выбираем вторую инлайн кнопку (индекс 1)
    second_button_to_click = result[1]
    await second_button_to_click.click()

    # По окончании всех нажатий выводим результат в чат
    await event.edit(f"Результат: {result.text}")
