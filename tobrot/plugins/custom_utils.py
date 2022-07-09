#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import string
from pyrogram import enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# https://stackoverflow.com/questions/62173294/how-can-i-keep-save-the-user-input-in-dictionary

PRE_DICT = {}
CAP_DICT = {}
IMDB_TEMPLATE = {}

async def prefix_set(client, message):
    '''  /setpre command '''
    lm = await message.reply_text(
        text="`Setting Up ...`",
    )
    user_id_ = message.from_user.id 
    u_men = message.from_user.mention
    pre_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(pre_send) > 1:
        txt = pre_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    prefix_ = txt
    PRE_DICT[user_id_] = prefix_

    pre_text = await lm.edit_text(f"⚡️<i><b>Custom Prefix Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{user_id_}</code>\n🗃 <b>Prefix :</b> <spoiler><code>{txt}</code></spoiler>", parse_mode=enums.ParseMode.HTML)
    

async def caption_set(client, message):
    '''  /setcap command '''

    lk = await message.reply_text(
        text="`Setting Up ...`",
    )
    user_id_ = message.from_user.id 
    u_men = message.from_user.mention
    cap_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(cap_send) > 1:
        txt = cap_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    caption_ = txt
    CAP_DICT[user_id_] = caption_
    try:
        txx = txt.split("#", maxsplit=1)
        txt = txx[0]
    except:
        pass 
    cap_text = await lk.edit_text(f"⚡️<i><b>Custom Caption Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{user_id_}</code>\n🗃 <b>Caption :</b>\n<tg-spoiler><code>{txt}</code></tg-spoiler>", parse_mode=enums.ParseMode.HTML)


async def template_set(client, message):
    '''  /set_template command '''
    lm = await message.reply_text(
        text="`Checking Input ...`",
    )
    user_id_ = message.from_user.id 
    u_men = message.from_user.mention
    tem_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        txt = tem_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    if txt == "":
        await lm.edit_text("`Send Custom TEMPLATE for your Usage`")
        return
    else:
        template_ = txt
        IMDB_TEMPLATE[user_id_] = template_
    
        await lm.edit_text(f"⚡️<i><b>Custom Template Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{user_id_}</code>\n🗃 <b>IMDB Template :</b> \n<code>{txt}</code>", parse_mode=enums.ParseMode.HTML)


    '''
    await message.reply_text(
        text="**Send me New File Name Prefix!**",
        #reply_to_message_id=message.reply_to_message.message_id,
        parse_mode=enums.ParseMode.MARKDOWN,
    )
    try:
        ask_: Message = await bot.listen(message.from_user.id)
        if ask_.text and (ask_.text.startswith("/") is False):
            await ask_.delete(True)
            user_id_ = message.from_user.id
            prefix_ = ask_.text
            #await SetupPrefix(ask_.text, user_id=cb.from_user.id, editable=cb.message)
            set_pre[user_id_] = prefix_
            save_dict(set_pre)
            ascii_ = ''.join([i if (i in string.digits or i in string.ascii_letters or i == " ") else "" for i in text])
            #await db.set_prefix(user_id, prefix=text)
            await message.reply_text(
                text=f"File Name Prefix Successfully Added!\n\n**Prefix:** `{ascii_}`",
            )

        elif ask_.text and (ask_.text.startswith("/") is True):
            await message.reply_text(
                text="`Current Process Cancelled!`",
                #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go Back", callback_data="openSettings")]])
            )
    except TimeoutError:
        await message.send_message(
            message.reply_to_message.from_user.id,
            text="Sorry Unkil,\n5 Minutes Passed! I can't wait more. Send me Text Again to Set.",
        )
            #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go Back", callback_data="openSettings")]])
     '''
