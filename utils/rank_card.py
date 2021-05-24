from database.users import get_xp
from utils.functions import get_level_from_xp
from utils.functions import get_level_xp


async def generate_rank_card(user):
    xp = await get_xp(user.id)
    current_level = await get_level_from_xp(xp)
    xp_required = await get_level_xp(current_level + 1)
    print(
        f"Current Level: {current_level}\n"
        f"Current XP: {xp}\n"
        f"XP Required: {xp_required}"
    )
