async def create_paste_desc(messages):
    text_to_paste = ""
    messages.reverse()
    for message in messages:
        timestamp = message.created_at.strftime("%H:%M")
        message_content = message.content
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                message_content += f"\n{attachment.url}"
        if message_content == "":
            message_content = "MESSAGE WAS AN EMBED"
        text_to_paste += f"[{timestamp}] {message.author.name} ({message.author.id}): {message_content}\n"
    return text_to_paste


def get_level_xp(level):
    return 5 * (level ** 2) + (50 * level) + 100


async def get_level_from_xp(xp) -> int:
    remaining_xp = int(xp)
    level = 0
    while remaining_xp >= get_level_xp(level):
        remaining_xp -= get_level_xp(level)
        level += 1
    return level
