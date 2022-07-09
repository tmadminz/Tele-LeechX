#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import logging
import pyrogram
from tobrot import *

from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def new_join_f(client, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        await message.reply_text(
            f"""<b>🙋🏻‍♂️ Hello dear!\n\n This Is A Leech Bot .This Chat Is Not Supposed To Use Me</b>\n\n<b>Current CHAT ID: <code>{message.chat.id}</code>""",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Channel', url='https://t.me/FuZionXTorrentQuater')
                    ]
                ]
               )
            )
        # leave chat
        await client.leave_chat(chat_id=message.chat.id, delete=True)
    # delete all other messages, except for AUTH_CHANNEL
    #await message.delete(revoke=True)


async def help_message_f(client, message):

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🆘️ Open Help 🆘️", callback_data = "openHelp_pg1")
            ]
        ]
    )
    await message.reply_text(
        text = f"""┏━ 🆘 <b>HELP MODULE</b> 🆘 ━━━╻
┃
┃• <i>Open Help to Get Tips and Help</i>
┃• <i>Use the Bot Like a Pro User</i>
┃• <i>Access Every Feature That Bot Offers in Better Way </i>
┃• <i>Go through Commands to Get Help</i>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹""",
        reply_markup = reply_markup,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

