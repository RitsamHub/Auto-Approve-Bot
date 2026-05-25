import random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import *
from Script import text


async def is_subscribed(client, user_id):
    btn = []
    count = 0

    for channel in FORCE_SUB:
        try:
            user = await client.get_chat_member(channel, user_id)

            if user.status in [
                enums.ChatMemberStatus.BANNED,
                enums.ChatMemberStatus.LEFT
            ]:
                raise UserNotParticipant

        except UserNotParticipant:

            count += 1

            chat = await client.get_chat(channel)

            invite_link = chat.invite_link

            if not invite_link:
                invite = await client.create_chat_invite_link(channel)
                invite_link = invite.invite_link

            btn.append([
                InlineKeyboardButton(
                    text=f"📢 {chat.title}",
                    url=invite_link
                )
            ])

    if btn:

        btn.append([
            InlineKeyboardButton(
                text="🔄 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇",
                callback_data="try_again"
            )
        ])

        return False, InlineKeyboardMarkup(btn), count

    return True, None, 0


@Client.on_message(filters.private & filters.incoming)
async def force_sub(client, message):

    if not FORCE_SUB:
        return

    user_id = message.from_user.id

    subscribed, buttons, total_channels = await is_subscribed(
        client,
        user_id
    )

    if subscribed:
        return

    try:

        await message.reply_photo(
            photo=random.choice(PICS),

            caption=f"""
🔒 <b>𝖠𝖼𝖼𝖾𝗌𝗌 𝖱𝖾𝗌𝗍𝗋𝗂𝖼𝗍𝖾𝖽!</b>

{message.from_user.mention},

<b>𝖳𝗈 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖡𝗈𝗍, 𝖸𝗈𝗎 𝖭𝖾𝖾𝖽 𝖳𝗈 𝖩𝗈𝗂𝗇 𝖠𝖫𝖫 𝖱𝖾𝗊𝗎𝗂𝗋𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌.

𝖱𝖾𝗊𝗎𝗂𝗋𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌 ({total_channels})

𝖠𝖿𝗍𝖾𝗋 𝖩𝗈𝗂𝗇𝗂𝗇𝗀, 𝖢𝗅𝗂𝖼𝗄 “𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇” 𝖡𝖾𝗅𝗈𝗐.</b>
""",

            parse_mode=enums.ParseMode.HTML,
            reply_markup=buttons
        )

    except Exception as e:
        print(e)

    raise StopPropagation


@Client.on_callback_query(filters.regex("try_again"))
async def try_again(client, query):

    subscribed, buttons, total_channels = await is_subscribed(
        client,
        query.from_user.id
    )

    if subscribed:

        await query.message.delete()

        await query.message.reply_text(
            f"✅ {query.from_user.mention}, You Can Now Use The Bot.",
            parse_mode=enums.ParseMode.HTML
        )

        return

    await query.answer(
        "❌ You Still Haven't Joined All Channels",
        show_alert=True
    )