# General
TOKEN: str = ""  # discord bot token
PREFIX: str = "!"
MEMBER_ROLE: str = "member"
MUTE_ROLE: str = "muted"

# Paste
PASTE_API_KEY: str = ""  # paste.gg | register & create API key

# LOGGING
LOGS_CHANNEL_ID: int = 000000  # discord ID of logs channel
MOD_LOGS_CHANNEL_ID: int = 000000  # discord ID of mod logs channel

# Other
LOGO: str = "https://i.imgur.com/8mKjoAA.png"  # Logo URL
MOD_LOGS_CHANNEL_ID: int = 000000  # discord ID of verify-here

# DB (postgresql)

DATABASE = "MCsniperBOT"  # DB name
HOST = "localhost:5432"
USER = ""
PASSWORD = ""


RULES = {
    "aa": "✅ Be kind to other users in the discord server, toxicity is not tolerated.",
    "ab": "✅ Follow Discord terms of service. This includes being 13 or over to join.",
    "ac": "✅ Keep the server SFW. We want to keep this server a welcoming community for people all ages",
    "ad": "🛑 Doxxing / Dox threats are NOT tolerated and will result in an instant and permanent ban! "
    "This could include leaking details of someone that may not be considered private, but that they do not want public such as an email address.",
    "ae": "🛑 Do NOT post any content that could be considered NSFW, gore, or something else that people of all ages would not want to see. "
    " This includes graphic or suggestive memes.",
    "af": "🛑 No discussion of politics, religion, or other heavy topics! "
    "This allows us to focus on Minecraft, name sniping, or whatever else i happening at the time and not become divided by political opinions.",
    "ag": "🛑 Do NOT abuse any systems related to this server (custom announcements, discord bots, etc...) ",
    "ah": "🛑 Do NOT self promote, especially without context. It's okay to send your something that could be considered self "
    " promotion in chat if it's a part of a conversation, but spamming dms or randomly sending it in chat is not allowed.",
    "ba": "✅ Only ask for help in a channel specifically for support. Preferably, use a channel that is not currently active.",
    "bb": "✅ Ask the most specific question you can about a topic. This allows the support process to move much faster!",
    "bc": "✅ Check pinned messages or search for a term before asking for help about it."
    " This allows you to get answers faster and people helping to not repeat answers!",
    "bd": "⚠️ If you are not contributing answers to people's questions, by trolling or giving false information intentionally, then you risk being muted.",
    "ca": "🛑 No discussion of hacked / illegally obtained accounts",
    "cb": "🛑 No discussion of buying / selling / trading accounts"
}
