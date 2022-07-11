#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


import asyncio
import logging
import os
import re
import shutil
import subprocess
import time
from functools import partial
from pathlib import Path

import pyrogram.types as pyrogram
import requests

from telegram import ParseMode
from pyrogram import enums
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hurry.filesize import size
from PIL import Image
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types import InputMediaAudio, InputMediaDocument, InputMediaVideo
from requests.utils import requote_uri
from tobrot import (
    DESTINATION_FOLDER,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    INDEX_LINK,
    LOGGER,
    RCLONE_CONFIG,
    TG_MAX_FILE_SIZE,
    UPLOAD_AS_DOC,
    CAP_STYLE,
    CUSTOM_CAPTION,
    gDict,
    user_specific_config,
    bot,
    LEECH_LOG,
    EXCEP_CHATS,
    EX_LEECH_LOG,
    BOT_PM,
    TG_PRM_FILE_SIZE,
    PRM_USERS,
    userBot,
    PRM_LOG,
    STRING_SESSION
)
from tobrot.helper_funcs.copy_similar_file import copy_file
from tobrot.helper_funcs.display_progress import humanbytes, Progress
from tobrot.helper_funcs.help_Nekmo_ffmpeg import take_screen_shot
from tobrot.helper_funcs.split_large_files import split_large_files
from tobrot.plugins.custom_utils import *

# stackoverflow🤐
def getFolderSize(p):
    prepend = partial(os.path.join, p)
    return sum(
        [
            (os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f))
            for f in map(prepend, os.listdir(p))
        ]
    )

async def upload_to_tg(
    message,
    local_file_name,
    from_user,
    dict_contatining_uploaded_files,
    client,
    edit_media=False,
    yt_thumb=None,
):
    base_file_name = os.path.basename(local_file_name)
    file_size = os.path.getsize(local_file_name)

    caption_str = ""
    DEF_CAPTION_MSG = f"<{CAP_STYLE}>"
    DEF_CAPTION_MSG += base_file_name
    DEF_CAPTION_MSG += f"</{CAP_STYLE}>"

    caption = CAP_DICT.get(from_user, "") 
    CUSTOM_CAPTION = caption 

    if CUSTOM_CAPTION != "":
        slit = CUSTOM_CAPTION.split("#")
        CAP_ = slit[0]
        caption_str = CAP_.format(
            filename = base_file_name,
            size = humanbytes(file_size)
        )
        if len(slit) > 1:
            for rep in range(1, len(slit)):
                args = slit[rep].split(":")
                if len(args) == 3:
                    caption_str = caption_str.replace(args[0], args[1], int(args[2]))
                else:
                    caption_str = caption_str.replace(args[0], args[1])
    else:
        caption_str = DEF_CAPTION_MSG

    if os.path.isdir(local_file_name):
        directory_contents = os.listdir(local_file_name)
        directory_contents.sort()
        LOGGER.info(directory_contents)
        new_m_esg = message
        if not message.photo:
            new_m_esg = await message.reply_text(
                f"<b><i>🛠 Extracting : </i></b> <code>{len(directory_contents)}</code> <b>File(s) <a href='tg://user?id={from_user}'></a></b>",
                quote=True
                # reply_to_message_id=message.id
            )
        for single_file in directory_contents:
            # recursion: will this FAIL somewhere?
            await upload_to_tg(
                new_m_esg,
                os.path.join(local_file_name, single_file),
                from_user,
                dict_contatining_uploaded_files,
                client,
                edit_media,
                yt_thumb,
            )
    else:
        sizze = os.path.getsize(local_file_name)
        if sizze < TG_PRM_FILE_SIZE and sizze > TG_MAX_FILE_SIZE and str(from_user) in str(PRM_USERS) and STRING_SESSION:
            LOGGER.info(f"User Type : Premium ({from_user})")
            prm_atv = True
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user,
                client,
                edit_media,
                yt_thumb,
                prm_atv
            )
            LOGGER.info(sent_message.message_id)
            if sent_message is not None:
                dict_contatining_uploaded_files[
                    os.path.basename(local_file_name)
                ] = sent_message.message_id
            else:
                return
        elif os.path.getsize(local_file_name) > TG_MAX_FILE_SIZE:
            LOGGER.info(f"User Type : Non Premium ({from_user})")
            i_m_s_g = await message.reply_text(
                "<b><i>📑Telegram doesn't Support Uploading this File.</i></b>\n"
                f"<b><i>🎯Detected File Size: {humanbytes(os.path.getsize(local_file_name))} </i></b>\n"
                "\n<code>🗃 Trying to split the files . . .</code>"
            )
            splitted_dir = await split_large_files(local_file_name)
            totlaa_sleif = os.listdir(splitted_dir)
            totlaa_sleif.sort()
            number_of_files = len(totlaa_sleif)
            LOGGER.info(totlaa_sleif)
            ba_se_file_name = os.path.basename(local_file_name)
            await i_m_s_g.edit_text(
                f"<b><i>📨 Detected File Size: {d_f_s}</i></b> \n"
                f"📬<code>{ba_se_file_name}</code><i><b> splitted into {number_of_files} Files🗃.</b></i>\n"
                "<i><b>📤Trying to upload to Telegram📤, Now...</b></i>"
            )
            for le_file in totlaa_sleif:
                # recursion: will this FAIL somewhere?
                await upload_to_tg(
                    message,
                    os.path.join(splitted_dir, le_file),
                    from_user,
                    dict_contatining_uploaded_files,
                    client,
                    edit_media,
                    yt_thumb,
                )
        else:
            sizze = os.path.getsize(local_file_name)
            LOGGER.info("Files Less Than 2 GB")
            prm_atv = False
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user,
                client,
                edit_media,
                yt_thumb,
                prm_atv
            )
            if sent_message is not None:
                dict_contatining_uploaded_files[
                    os.path.basename(local_file_name)
                ] = sent_message.id
            else:
                return
    # await message.delete()
    return dict_contatining_uploaded_files


# © gautamajay52 thanks to Rclone team for this wonderful tool.🧘

async def upload_to_gdrive(file_upload, message, messa_ge, g_id):
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    del_it = await message.edit_text(
        f"<a href='tg://user?id={g_id}'>🔊</a> Now Uploading to ☁️ Cloud!!!"
    )
    if not os.path.exists("rclone.conf"):
        with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
            fole.write(f"{RCLONE_CONFIG}")
    if os.path.exists("rclone.conf"):
        with open("rclone.conf", "r+") as file:
            con = file.read()
            gUP = re.findall("\[(.*)\]", con)[0]
            LOGGER.info(gUP)
    destination = f"{DESTINATION_FOLDER}"
    file_upload = str(Path(file_upload).resolve())
    LOGGER.info(file_upload)
    if os.path.isfile(file_upload):
        g_au = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{file_upload}",
            f"{gUP}:{destination}",
            "-v",
        ]
        LOGGER.info(g_au)
        tmp = await asyncio.create_subprocess_exec(
            *g_au, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        gk_file = re.escape(os.path.basename(file_upload))
        LOGGER.info(gk_file)
        with open("filter.txt", "w+", encoding="utf-8") as filter:
            print(f"+ {gk_file}\n- *", file=filter)

        t_a_m = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter.txt",
            "--files-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await asyncio.create_subprocess_exec(
            *t_a_m, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # os.remove("filter.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode().strip()
        LOGGER.info(gau.decode())
        LOGGER.info(tam.decode())
        # os.remove("filter.txt")
        gauti = f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"
        gjay = size(os.path.getsize(file_upload))
        button = []
        button.append(
            [pyrogram.InlineKeyboardButton(text="☁️ CloudUrl ☁️", url=f"{gauti}")]
        )
        if INDEX_LINK:
            indexurl = f"{INDEX_LINK}/{os.path.basename(file_upload)}"
            tam_link = requests.utils.requote_uri(indexurl)
            LOGGER.info(tam_link)
            button.append(
                [
                    pyrogram.InlineKeyboardButton(
                        text="ℹ️ IndexUrl ℹ️", url=f"{tam_link}"
                    )
                ]
            )
        button_markup = pyrogram.InlineKeyboardMarkup(button)
        await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"🤖: Uploaded successfully `{os.path.basename(file_upload)}` <a href='tg://user?id={g_id}'>🤒</a>\n📀 Size: {gjay}",
            reply_markup=button_markup,
        )
        os.remove(file_upload)
        await del_it.delete()
    else:
        tt = os.path.join(destination, os.path.basename(file_upload))
        LOGGER.info(tt)
        t_am = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{file_upload}",
            f"{gUP}:{tt}",
            "-v",
        ]
        LOGGER.info(t_am)
        tmp = await asyncio.create_subprocess_exec(
            *t_am, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        g_file = re.escape(os.path.basename(file_upload))
        LOGGER.info(g_file)
        with open("filter1.txt", "w+", encoding="utf-8") as filter1:
            print(f"+ {g_file}/\n- *", file=filter1)

        g_a_u = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter1.txt",
            "--dirs-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await asyncio.create_subprocess_exec(
            *g_a_u, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # os.remove("filter1.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode("utf-8")
        LOGGER.info(gautam)
        LOGGER.info(tam.decode("utf-8"))
        # os.remove("filter1.txt")
        gautii = f"https://drive.google.com/folderview?id={gautam}"
        gjay = size(getFolderSize(file_upload))
        LOGGER.info(gjay)
        button = []
        button.append(
            [pyrogram.InlineKeyboardButton(text="☁️ CloudUrl ☁️", url=f"{gautii}")]
        )
        if INDEX_LINK:
            indexurl = f"{INDEX_LINK}/{os.path.basename(file_upload)}/"
            tam_link = requests.utils.requote_uri(indexurl)
            LOGGER.info(tam_link)
            button.append(
                [
                    pyrogram.InlineKeyboardButton(
                        text="ℹ️ IndexUrl ℹ️", url=f"{tam_link}"
                    )
                ]
            )
        button_markup = pyrogram.InlineKeyboardMarkup(button)
        await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"🤖: Uploaded successfully `{os.path.basename(file_upload)}` <a href='tg://user?id={g_id}'>🤒</a>\n📀 Size: {gjay}",
            reply_markup=button_markup,
        )
        shutil.rmtree(file_upload)
        await del_it.delete()


VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF")
AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
IMAGE_SUFFIXES = ("JPG", "JPX", "PNG", "WEBP", "CR2", "TIF", "BMP", "JXR", "PSD", "ICO", "HEIC", "JPEG")

async def upload_single_file(
    message, local_file_name, caption_str, from_user, client, edit_media, yt_thumb, prm_atv: bool
):
    base_file_name = os.path.basename(local_file_name)
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    local_file_name = str(Path(local_file_name).resolve())
    sent_message = None
    start_time = time.time()
    #
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION, "thumbnails", str(from_user) + ".jpg"
    )
    # LOGGER.info(thumbnail_location)
    dyna_user_config_upload_as_doc = False
    for key in iter(user_specific_config):
        if key == from_user:
            dyna_user_config_upload_as_doc=user_specific_config[key].upload_as_doc
            LOGGER.info(f'Found dyanamic config for user {from_user}')
    #
    if UPLOAD_AS_DOC.upper() == "TRUE" or dyna_user_config_upload_as_doc: 
    # todo
        thumb = None
        thumb_image_path = None
        if os.path.exists(thumbnail_location):
            thumb_image_path = await copy_file(
                thumbnail_location, os.path.dirname(os.path.abspath(local_file_name))
            )
            thumb = thumb_image_path
        message_for_progress_display = message
        if not edit_media:
            message_for_progress_display = await message.reply_text(
                "<b>🔰Status : <i>Starting Uploading...📤</i></b>\n\n🗃<b> File Name</b>: <code>{}</code>".format(os.path.basename(local_file_name))
            )
            prog = Progress(from_user, client, message_for_progress_display)
        LOGGER.info(f"Premium Active : {prm_atv}")
        if str(message.chat.id) in str(EXCEP_CHATS) and not prm_atv:
            sent_message = await message.reply_document(
                document=local_file_name,
                thumb=thumb,
                caption=caption_str,
                parse_mode=enums.ParseMode.HTML,
                disable_notification=True,
                progress=prog.progress_for_pyrogram,
                progress_args=(
                    f"◆━━━━━━◆ ❃ ◆━━━━━━◆\n\n┏━━━━━━━━━━━━━━━━╻\n┣⚡️ 𝐅𝐢𝐥𝐞𝐧𝐚𝐦𝐞 : `{os.path.basename(local_file_name)}`",
                    start_time,
                ),
            )
        elif str(message.chat.id) in str(EXCEP_CHATS) and prm_atv:
            with userBot:
                LOGGER.info("UserBot Upload : Started")
                sent_msg = await userBot.send_document(
                    chat_id=int(PRM_LOG),
                    document=local_file_name,
                    thumb=thumb,
                    caption=f"<code>{os.path.basename(local_file_name)}</code>",
                    parse_mode=enums.ParseMode.HTML,
                    disable_notification=True,
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"◆━━━━━━◆ ❃ ◆━━━━━━◆\n\n┏━━━━━━━━━━━━━━━━╻\n┣⚡️ 𝐅𝐢𝐥𝐞𝐧𝐚𝐦𝐞 : `{os.path.basename(local_file_name)}`",
                        start_time,
                    ),
                )
                LOGGER.info("UserBot Upload : Completed")
            prm_id = sent_msg.id
            sent_message = bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=int(PRM_LOG),
                message_id=prm_id,
                caption=caption_str,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.id
            )
            
        else:
            sent_message = await bot.send_document(
                chat_id=int(LEECH_LOG),
                document=local_file_name,
                thumb=thumb,
                caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 @FXTorrentz ♨️",
                parse_mode=enums.ParseMode.HTML,
                disable_notification=True,
            )
            if BOT_PM:
                try:
                  bot.send_document(
                      chat_id=from_user, 
                      document=sent_message.document.file_id,
                      thumb=thumb,
                      caption=caption_str,
                      parse_mode=enums.ParseMode.HTML
                  )
                except Exception as err:
                   LOGGER.error(f"Failed To Send Document in User PM:\n{err}")
            if EX_LEECH_LOG:
                try:
                    for i in EX_LEECH_LOG:
                        bot.send_document(
                            chat_id=i, 
                            document=sent_message.document.file_id,
                            thumb=thumb,
                            caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 @FXTorrentz ♨️",
                            parse_mode=enums.ParseMode.HTML
                        )
                except Exception as err:
                    LOGGER.error(f"Failed To Send Document in Channel:\n{err}")
        if message.id != message_for_progress_display.id:
            try:
                await message_for_progress_display.delete()
            except FloodWait as gf:
                time.sleep(gf.value)
            except Exception as rr:
                LOGGER.warning(str(rr))
        os.remove(local_file_name)
        if thumb is not None:
            os.remove(thumb)
    else:
        try:
            message_for_progress_display = message
            if not edit_media:
                message_for_progress_display = await message.reply_text(
                    "<b>🔰Status : <i>Starting Uploading...📤</i></b>\n\n🗃<b> File Name</b>: <code>{}</code>".format(os.path.basename(local_file_name))
                )
                prog = Progress(from_user, client, message_for_progress_display)
            if local_file_name.upper().endswith(VIDEO_SUFFIXES):
                duration = 0
                try:
                    metadata = extractMetadata(createParser(local_file_name))
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                except Exception as g_e:
                    LOGGER.info(g_e)
                width = 0
                height = 0
                thumb_image_path = None
                if os.path.exists(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        os.path.dirname(os.path.abspath(local_file_name)),
                    )
                else:
                    if not yt_thumb:
                        LOGGER.info("📸 Taking Screenshot..")
                        thumb_image_path = await take_screen_shot(
                            local_file_name,
                            os.path.dirname(os.path.abspath(local_file_name)),
                            (duration / 2),
                        )
                    else:
                        req = requests.get(yt_thumb)
                        thumb_image_path = os.path.join(
                            os.path.dirname(os.path.abspath(local_file_name)),
                            str(time.time()) + ".jpg",
                        )
                        with open(thumb_image_path, "wb") as thum:
                            thum.write(req.content)
                        img = Image.open(thumb_image_path).convert("RGB")
                        img.save(thumb_image_path, format="jpeg")
                    # get the correct width, height, and duration for videos greater than 10MB
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                        # ref: https://t.me/PyrogramChat/44663
                        # https://stackoverflow.com/a/21669827/4723940
                        Image.open(thumb_image_path).convert("RGB").save(
                            thumb_image_path
                        )
                        img = Image.open(thumb_image_path)
                        # https://stackoverflow.com/a/37631799/4723940
                        img.resize((320, height))
                        img.save(thumb_image_path, "JPEG")
                        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
                #
                thumb = None
                if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                    thumb = thumb_image_path
                # send video
                if edit_media and message.photo:
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                    sent_message = await message.edit_media(
                        media=InputMediaVideo(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            width=width,
                            height=height,
                            duration=duration,
                            supports_streaming=True,
                        )
                        # quote=True,
                    )
                else:
                    if str(message.chat.id) in str(EXCEP_CHATS):
                        sent_message = await message.reply_video(
                            video=local_file_name,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            duration=duration,
                            width=width,
                            height=height,
                            thumb=thumb,
                            supports_streaming=True,
                            disable_notification=True,
                            progress=prog.progress_for_pyrogram,
                            progress_args=(
                                f"<b>🔰Status : <i>Starting Uploading...📤</i></b>\n\n🗃<b> File Name</b>: `{os.path.basename(local_file_name)}`",
                                start_time,
                            ),
                         )
                    else:
                        sent_message = await message.sent_video(
                            chat_id=LEECH_LOG,
                            video=local_file_name,
                            caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 @FXTorrentz ♨️",
                            parse_mode=enums.ParseMode.HTML,
                            duration=duration,
                            width=width,
                            height=height,
                            thumb=thumb,
                            supports_streaming=True,
                            disable_notification=True,
                            progress=prog.progress_for_pyrogram,
                            progress_args=(
                                f"<b>🔰Status : <i>Starting Uploading...📤</i></b>\n\n🗃<b> File Name</b>: `{os.path.basename(local_file_name)}`",
                                start_time,
                            ),
                         )
                        if BOT_PM:
                            try:
                                bot.send_video(
                                    chat_id=from_user, 
                                    video=sent_message.video.file_id,
                                    thumb=thumb,
                                    supports_streaming=True,
                                    caption=caption_str,
                                    parse_mode=enums.ParseMode.HTML
                                )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Video in User PM:\n{err}")
                        if EX_LEECH_LOG:
                            try:
                                for i in EX_LEECH_LOG:
                                    bot.send_video(
                                        chat_id=i, 
                                        video=sent_message.video.file_id,
                                        thumb=thumb,
                                        supports_streaming=True,
                                        caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 @FXTorrentz ♨️",
                                        parse_mode=enums.ParseMode.HTML
                                    )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Video in Channel:\n{err}")
                if thumb is not None:
                    os.remove(thumb)
            elif local_file_name.upper().endswith(AUDIO_SUFFIXES):
                metadata = extractMetadata(createParser(local_file_name))
                duration = 0
                title = ""
                artist = ""
                if metadata.has("duration"):
                    duration = metadata.get("duration").seconds
                if metadata.has("title"):
                    title = metadata.get("title")
                if metadata.has("artist"):
                    artist = metadata.get("artist")
                thumb_image_path = None
                if os.path.isfile(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        os.path.dirname(os.path.abspath(local_file_name)),
                    )
                thumb = None
                if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                    thumb = thumb_image_path
                # send audio
                if edit_media and message.photo:
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                    sent_message = await message.edit_media(
                        media=InputMediaAudio(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            duration=duration,
                            performer=artist,
                            title=title,
                        )
                    )
                else:
                    sent_message = await message.reply_audio(
                        audio=local_file_name,
                        caption=caption_str,
                        parse_mode=enums.ParseMode.HTML,
                        duration=duration,
                        performer=artist,
                        title=title,
                        thumb=thumb,
                        disable_notification=True,
                        progress=prog.progress_for_pyrogram,
                        progress_args=(
                            f"<b>🔰Status : <i>Starting Uploading...📤</i></b>\n\n🗃<b> File Name</b>: `{os.path.basename(local_file_name)}`",
                            start_time,
                        ),
                    )
                    if BOT_PM:
                        try:
                            bot.send_audio(
                                chat_id=from_user, 
                                audio=sent_message.audio.file_id,
                                thumb=thumb,
                                caption=caption_str,
                            )
                        except Exception as err:
                            LOGGER.error(f"Failed To Send Audio in User PM:\n{err}")
                    if LEECH_LOG:
                        try:
                            for i in LEECH_LOG:
                                bot.send_audio(
                                    chat_id=i, 
                                    document=sent_message.audio.file_id,
                                    thumb=thumb,
                                    caption=f"<code>{base_file_name}</code>",
                                )
                        except Exception as err:
                            LOGGER.error(f"Failed To Send Audio in User PM:\n{err}")
                if thumb is not None:
                    os.remove(thumb)
            else:
                thumb_image_path = None
                if os.path.isfile(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        os.path.dirname(os.path.abspath(local_file_name)),
                    )
                # if a file, don't upload "thumb"
                # this "diff" is a major derp -_- 😔😭😭
                thumb = None
                if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                    thumb = thumb_image_path
                #
                # send document
                if edit_media and message.photo:
                    sent_message = await message.edit_media(
                        media=InputMediaDocument(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML
                        )
                    )
                else:
                    if str(message.chat.id) in str(EXCEP_CHATS):
                        sent_message = await message.reply_document(
                            document=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            disable_notification=True,
                            progress=prog.progress_for_pyrogram,
                            progress_args=(
                                f"<b>🔰Status : <i>Starting Uploading...📤</i></b>\n\n🗃<b> File Name</b>: `{os.path.basename(local_file_name)}`",
                                start_time,
                            ),
                        )
                    else:
                        sent_message = await bot.send_document(
                            chat_id=LEECH_LOG,
                            document=local_file_name,
                            thumb=thumb,
                            caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 @FXTorrentz ♨️",
                            parse_mode=enums.ParseMode.HTML,
                            disable_notification=True,
                            progress=prog.progress_for_pyrogram,
                            progress_args=(
                                f"<b>🔰Status : <i>Starting Uploading...📤</i></b>\n\n🗃<b> File Name</b>: `{os.path.basename(local_file_name)}`",
                                start_time,
                            ),
                        )
                        if BOT_PM:
                            try:
                                bot.send_document(
                                    chat_id=from_user, 
                                    document=sent_message.document.file_id,
                                    thumb=thumb,
                                    caption=caption_str,
                                    parse_mode=enums.ParseMode.HTML
                                )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Document in User PM:\n{err}")
                        if EX_LEECH_LOG:
                            try:
                                for i in EX_LEECH_LOG:
                                    bot.send_document(
                                        chat_id=i, 
                                        document=sent_message.document.file_id,
                                        thumb=thumb,
                                        caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 @FXTorrentz ♨️",
                                        parse_mode=enums.ParseMode.HTML
                                    )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Document in Channel:\n{err}")
                if thumb is not None:
                    os.remove(thumb)

        except MessageNotModified as oY:
            LOGGER.info(oY)
        except FloodWait as g:
            LOGGER.info(g)
            time.sleep(g.value)
        except Exception as e:
            LOGGER.info(e)
            await message_for_progress_display.edit_text("**FAILED**\n" + str(e))
        else:
            if message.id != message_for_progress_display.id:
                try:
                    if sent_message is not None:
                        await message_for_progress_display.delete()
                except FloodWait as gf:
                    time.sleep(gf.value)
                except Exception as rr:
                    LOGGER.warning(str(rr))
                    await asyncio.sleep(5)
        os.remove(local_file_name)
    return sent_message
