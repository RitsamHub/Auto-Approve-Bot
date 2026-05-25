import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import *
from Script import text
from .database import tb


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):

    if await tb.get_user(message.from_user.id) is None:

        await tb.add_user(
            message.from_user.id,
            message.from_user.first_name
        )

        bot = await client.get_me()

        await client.send_message(
            LOG_CHANNEL,
            text.LOG.format(
                message.from_user.id,
                getattr(message.from_user, "dc_id", "N/A"),
                message.from_user.first_name or "N/A",
                f"@{message.from_user.username}" if message.from_user.username else "N/A",
                bot.username
            )
        )

    await message.reply_photo(
        photo=random.choice(PICS),
        caption=text.START.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    '⇆ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ⇆',
                    url="https://telegram.me/{bot_info.username}?startgroup=true&admin=invite_users"
                )
            ],
            [
                InlineKeyboardButton('ℹ️ 𝖠𝖻𝗈𝗎𝗍', callback_data='about'),
                InlineKeyboardButton('📚 𝖧𝖾𝗅𝗉', callback_data='help')
            ],
            [
                InlineKeyboardButton(
                    '⇆ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 ⇆',
                    url="https://telegram.me/{bot_info.username}?startchannel=true&admin=invite_users"
                )
            ]
        ])
    )


@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):

    tb_msg = await message.reply(
        "❓ <b>Having Trouble?</b>\n"
        "If you're facing any problem using the bot, watch tutorial below.\n\n"
        "🎥 The video explains everything clearly.\n\n"
        "💖 Support: <b><a href='https://t.me/Vrubhi_x'>Support Us</a></b>",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎬 Watch Tutorial",
                    url="https://youtu.be/_n3V0gFZMh8"
                )
            ]
        ])
    )

    await asyncio.sleep(300)

    try:
        await tb_msg.delete()
        await message.delete()
    except:
        pass


@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):

    show = await message.reply("Please wait...")

    user_data = await tb.get_session(message.from_user.id)

    if user_data is None:
        return await show.edit("Use /login first.")

    try:
        acc = Client(
            "joinrequest",
            session_string=user_data,
            api_id=API_ID,
            api_hash=API_HASH
        )

        await acc.connect()

    except:
        return await show.edit(
            "Session expired. Use /logout then /login again."
        )

    await show.edit(
        "Forward a message from your channel/group."
    )

    fwd_msg = await client.listen(message.chat.id)

    if (
        fwd_msg.forward_from_chat
        and fwd_msg.forward_from_chat.type
        not in [enums.ChatType.PRIVATE, enums.ChatType.BOT]
    ):
        chat_id = fwd_msg.forward_from_chat.id

        try:
            await acc.get_chat(chat_id)
        except:
            return await show.edit(
                "Make sure your account is admin in that chat."
            )

    else:
        return await message.reply(
            "Invalid forwarded message."
        )

    try:
        await fwd_msg.delete()
    except:
        pass

    msg = await show.edit("Processing join requests...")

    try:
        while True:

            await acc.approve_all_chat_join_requests(chat_id)

            await asyncio.sleep(2)

            join_requests = [
                req async for req in acc.get_chat_join_requests(chat_id)
            ]

            if not join_requests:
                break

        await msg.edit("✅ All join requests approved.")

    except Exception as e:
        await msg.edit(f"Error: {e}")


@Client.on_chat_join_request()
async def approve_new(client, m):

    if not NEW_REQ_MODE:
        return

    try:
        await client.approve_chat_join_request(
            m.chat.id,
            m.from_user.id
        )

        await client.send_photo(
            chat_id=m.from_user.id,
            photo=random.choice(PICS),
            caption=f"""
<blockquote><b>{m.from_user.mention}</b></blockquote>
<b>
Contenido exclusivo 🔞🔒

https://cutt.ly/xtAOopXP
https://cutt.ly/xtAOopXP

✅ Acceso Completo ✅
</b>
""",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Sophie Raiin 🍑", url="https://t.me/+R41SiS0FJCkxNzIx"),
                    InlineKeyboardButton("Karely Ruiz 🍓", url="https://t.me/+RVxG8Au6CnEyZTUx")
                ],
                [
                    InlineKeyboardButton("Maria Julissa 🍑", url="https://t.me/+blQTEyDXu5c1ODk1"),
                    InlineKeyboardButton("Piper Rockelle 🔞", url="https://t.me/+JsJdB1qA2Dk3OTA1")
                ]
            ])
        )

    except Exception as e:
        print("Join request error:", e)