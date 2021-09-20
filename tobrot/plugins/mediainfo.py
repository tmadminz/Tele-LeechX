# Suggested by - @MysterySD (https://github.com/code-rgb/USERGE-X/issues/9)
# Copyright (C) 2020 BY - GitHub.com/code-rgb [TG - @deleteduser420]
# Taken From Slam-mirrorbot, I thereby Take No Extra Credit on Code !!
# All rights reserved.

import asyncio
import os
import shlex

from typing import Tuple
from html_telegraph_poster import TelegraphPoster
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tobrot import app, bot
from tobrot.helper_funcs.bot_commands import BotCommands

def post_to_telegraph(a_title: str, content: str) -> str:
    """ Create a Telegram Post using HTML Content """
    post_client = TelegraphPoster(use_api=True)
    auth_name = "FuZionX-Leech"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=a_title,
        author=auth_name,
        author_url="https://github.com/5MysterySD/Tele-LeechX",
        text=content,
    )
    return post_page["url"]

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

def safe_filename(path_):
    if path_ is None:
        return
    safename = path_.replace("'", "").replace('"', "")
    if safename != path_:
        os.rename(path_, safename)
    return safename

@app.on_message(filters.command([BotCommands.MediaInfoCommand, f'{BotCommands.MediaInfoCommand}@{bot.username}']))
async def mediainfo(client, message):
    reply = message.reply_to_message
    if not reply:
        await message.reply_text("Reply to Media first")
        return
    process = await message.reply_text("`Processing...`")
    x_media = None
    available_media = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
        "new_chat_photo",
    )
    for kind in available_media:
        x_media = getattr(reply, kind, None)
        if x_media is not None:
            break
    if x_media is None:
       await process.edit_text("Reply To a Valid Media Format")
       return
    media_type = str(type(x_media)).split("'")[1]
    file_path = safe_filename(await reply.download())
    output_ = await runcmd(f'mediainfo "{file_path}"')
    out = None
    if len(output_) != 0:
         out = output_[0]
    body_text = f"""
<h2>JSON</h2>
<pre>{x_media}</pre>
<br>
<h2>DETAILS</h2>
<pre>{out or 'Not Supported'}</pre>
"""
    title = f"Slam Mirror Bot Mediainfo"
    text_ = media_type.split(".")[-1].upper()
    link = post_to_telegraph(title, body_text)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=text_, url=link)]])
    await process.edit_text("ℹ️ <b>MEDIA INFO</b>", reply_markup=markup)


