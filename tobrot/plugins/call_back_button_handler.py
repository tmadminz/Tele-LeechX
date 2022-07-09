#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


import logging
import os
import shutil

from pyrogram import enums
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton 
from tobrot import *
#from tobrot import AUTH_CHANNEL, MAX_MESSAGE_LENGTH, LOGGER, gDict
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.helper_funcs.youtube_dl_button import youtube_dl_call_back
from tobrot.plugins.choose_rclone_config import rclone_button_callback
from tobrot.plugins.status_message_fn import cancel_message_f


async def button(bot, update: CallbackQuery):
    cb_data = update.data
    try:
        g = await AdminCheck(bot, update.message.chat.id, update.from_user.id)
    except Exception as ee:
        LOGGER.info(ee)
    if cb_data.startswith("gUPcancel"):
        cmf = cb_data.split("/")
        chat_id, mes_id, from_usr = cmf[1], cmf[2], cmf[3]
        if (int(update.from_user.id) == int(from_usr)) or g:
            await bot.answer_callback_query(
                update.id, text="Going to Cancel . . . 🛠", show_alert=False
            )
            gDict[int(chat_id)].append(int(mes_id))
        else:
            await bot.answer_callback_query(
                callback_query_id=update.id,
                text="⚠️ Opps ⚠️ \n I Got a False Visitor 🚸 !! \n\n 📛 Stay At Your Limits !!📛",
                show_alert=True,
                cache_time=0,
            )
        return
    if "|" in cb_data:
        await bot.answer_callback_query(
            update.id, text="Processing . . . 🛠", show_alert=False
        )
        await youtube_dl_call_back(bot, update)
        return
    if cb_data.startswith("rclone"):
        await bot.answer_callback_query(
            update.id, text="choose rclone config...", show_alert=False
        )
        await rclone_button_callback(bot, update)
        return
    # todo - remove this code if not needed in future
    if cb_data.startswith("cancel"):
        if (update.from_user.id == update.message.reply_to_message.from_user.id) or g:
            await bot.answer_callback_query(
                update.id, text="trying to cancel...", show_alert=False
            )
            if len(cb_data) > 1:
                i_m_s_e_g = await update.message.reply_to_message.reply_text(
                    "checking..?", quote=True
                )
                aria_i_p = await aria_start()
                g_id = cb_data.split()[-1]
                LOGGER.info(g_id)
                try:
                    downloads = aria_i_p.get_download(g_id)
                    file_name = downloads.name
                    LOGGER.info(
                        aria_i_p.remove(
                            downloads=[downloads], force=True, files=True, clean=True
                        )
                    )
                    if os.path.exists(file_name):
                        if os.path.isdir(file_name):
                            shutil.rmtree(file_name)
                        else:
                            os.remove(file_name)
                    await i_m_s_e_g.edit_text(
                        f"Leech Cancelled by <a href='tg://user?id={update.from_user.id}'>{update.from_user.first_name}</a>"
                    )
                except Exception as e:
                    await i_m_s_e_g.edit_text("<i>FAILED</i>\n\n" + str(e) + "\n#error")
        else:
            await bot.answer_callback_query(
                callback_query_id=update.id,
                text="who are you? 🤪🤔🤔🤔",
                show_alert=True,
                cache_time=0,
            )
    elif cb_data == "fuckingdo":
        if (update.from_user.id in AUTH_CHANNEL) or g:
            await bot.answer_callback_query(
                update.id, text="trying to delete...", show_alert=False
            )
            g_d_list = [
                "app.json",
                "venv",
                "rclone.conf",
                "rclone_bak.conf",
                ".gitignore",
                "_config.yml",
                "COPYING",
                "Dockerfile",
                "extract",
                "Procfile",
                ".heroku",
                ".profile.d",
                "rclone.jpg",
                "README.md",
                "requirements.txt",
                "runtime.txt",
                "start.sh",
                "tobrot",
                "gautam",
                "FuZionXLogs.txt",
                "vendor",
                "LeechBot.session",
                "LeechBot.session-journal",
                "config.env",
                "sample_config.env",
            ]
            g_list = os.listdir()
            LOGGER.info(g_list)
            g_del_list = list(set(g_list) - set(g_d_list))
            LOGGER.info(g_del_list)
            if len(g_del_list) != 0:
                for f in g_del_list:
                    if os.path.isfile(f):
                        os.remove(f)
                    else:
                        shutil.rmtree(f)
                await update.message.edit_text(f"<code>🔃 Deleted {len(g_del_list)} Objects 🚮</code>")
            else:
                await update.message.edit_text("<i>⛔ Nothing to clear ⛔ \nAs Per I Get to Know !! </i>")
        else:
            await update.message.edit_text("<i>I Got Info, \nYou Are Not Allowed to Do This 🤭</i>")
    elif cb_data == "fuckoff":
        await bot.answer_callback_query(
            update.id, text="Going to Cancel . . . 🔃", show_alert=False
        )
        await update.message.edit_text("<i>☢ Okay! ☢ \n\n ⌧ Don't Disturb Me !! </i>")
    elif cb_data == "openHelp_pg1":
        button_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"/{LEECH_COMMAND}", callback_data = "leech"),
                    InlineKeyboardButton(f"/{LEECH_UNZIP_COMMAND}", callback_data = "extract")
                ],
                [
                    InlineKeyboardButton(f"/{LEECH_ZIP_COMMAND}", callback_data = "archive"),
                    InlineKeyboardButton(f"/{TOGGLE_DOC}", callback_data = "toggledoc")
                ],
                [
                    InlineKeyboardButton(f"/{TOGGLE_VID}", callback_data = "togglevid"),
                    InlineKeyboardButton(f"/{SAVE_THUMBNAIL}", callback_data = "savethumb")
                ],
                [
                    InlineKeyboardButton("⏪••", callback_data = "pre_1"),
                    InlineKeyboardButton("••⏩", callback_data = "nex_1")
                ],
                [
                    InlineKeyboardButton("Close 🔐", callback_data = "close")
                ]
            ]
        )
        await update.message.edit_text(
            text = "<b>Choose the Desired Command Help :</b>",
            reply_markup = button_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif cb_data == "nex_1":
        button_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"/{CLEAR_THUMBNAIL}", callback_data = "clearthumb"),
                    InlineKeyboardButton(f"/{RENAME_COMMAND}", callback_data = "rename")
                ],
                [
                    InlineKeyboardButton(f"/{STATUS_COMMAND}", callback_data = "status"),
                    InlineKeyboardButton(f"/{SPEEDTEST}", callback_data = "speedtest")
                ],
                [
                    InlineKeyboardButton(f"/{YTDL_COMMAND}", callback_data = "ytdl"),
                    InlineKeyboardButton(f"/{PYTDL_COMMAND}", callback_data = "pytdl")
                ],
                [
                    InlineKeyboardButton("⏪••", callback_data = "openHelp_pg1"),
                    InlineKeyboardButton("••⏩", callback_data = "nex_2")
                ],
                [
                    InlineKeyboardButton("Close 🔐", callback_data = "close")
                ]
            ]
        )
        await update.message.edit_text(
            text = "<b>Choose the Desired Command Help :</b>",
            reply_markup = button_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif cb_data == "nex_2":
        button_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"/{MEDIAINFO_CMD}", callback_data = "mediainfo"),
                    InlineKeyboardButton(f"/{TSEARCH_COMMAND}", callback_data = "tshelp")
                ],
                [
                    InlineKeyboardButton(f"/setpre", callback_data = "setpre"),
                    InlineKeyboardButton(f"/setcap", callback_data = "setcap")
                ],
                [
                    InlineKeyboardButton(f"/parser", callback_data = "parser")
                ],
                [
                    InlineKeyboardButton(f"More Features", callback_data = "fea")
                ],
                [
                    InlineKeyboardButton("⏪••", callback_data = "nex_1"),
                    InlineKeyboardButton("••⏩", callback_data = "openHelp_pg1")
                ],
                [
                    InlineKeyboardButton("Close 🔐", callback_data = "close")
                ]
            ]
        )
        await update.message.edit_text(
            text = "<b>Choose the Desired Command Help :</b>",
            reply_markup = button_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif cb_data == "leech":
        button_call = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Back", callback_data = "openHelp_pg1"),
                    InlineKeyboardButton("Close 🔐", callback_data = "close")
                ],
            ]
        )
        stringg = """<u>Cᴏᴍᴍᴀɴᴅ Aʟᴍᴀɴɪᴄ :</u>

• 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 : /leech
• 𝐓𝐲𝐩𝐞 : Magnet Link / Direct Link / Torrent File 
• 𝐔𝐩𝐥𝐨𝐚𝐝 𝐓𝐲𝐩𝐞 : Media ( Default )
• 𝐀𝐫𝐠𝐮𝐦𝐞𝐧𝐭 : <code>( Optional )</code>

□ <b><u>Custom Name while Leech</u></b>
<i>&gt; Use | for Custom Name
&gt; Like </i><i>www.download.me/fx.txt</i> <i>| sample.txt
&gt; Extension is Must</i>

□ <b><u>Direct Links Supported : </u></b>
<i>&gt; </i><i>zippyshare.com</i><i>, </i><i>letsupload.io</i><i>, </i><i>hxfile.co</i><i>, </i><i>anonfiles.com</i><i>, </i><i>bayfiles.com</i><i>, antfiles, </i><i>fembed.com</i><i>, </i><i>fembed.net</i><i>, </i><i>femax20.com</i><i>, </i><i>layarkacaxxi.icu</i><i>, </i><i>fcdn.stream</i><i>, </i><i>sbplay.org</i><i>, </i><i>naniplay.com</i><i>, </i><i>naniplay.nanime.in</i><i>, </i><i>naniplay.nanime.biz</i><i>, </i><i>sbembed.com</i><i>, </i><i>streamtape.com</i><i>, </i><i>streamsb.net</i><i>, </i><i>feurl.com</i><i>, </i><i>pixeldrain.com</i><i>, </i><i>racaty.net</i><i>, </i><i>1fichier.com</i><i>, </i><i>solidfiles.com</i><i>, </i><i>gplinks.co</i><i>, </i><i>appdrive.in</i> <b><i>( Other Available in </i></b><b><i>/parser</i></b> <b><i>)</i>
</b>
• 𝐔𝐬𝐚𝐠𝐞:
□ <b>Send Direct Link Along with Command :</b>
/leech(BotName) <code>{link}</code>

□ <b><u>Reply to a Direct Download Link / Torrent File / Magnet Link :</u></b>
<code>{type} | &lt;Custom Name&gt;</code>
/leech(BotName) <i>[Reply]</i>"""

        await update.message.edit_text(
            text = stringg,
            reply_markup = button_call,
            disable_web_page_preview = True, 
            parse_mode=enums.ParseMode.HTML
        )
    elif cb_data == "close":
        await update.message.delete()
        try:
            await update.message.reply_to_message.delete()
        except:
            pass

    '''
    elif cb_data == "":
        button_call = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Back", callback_data = ""),
                    InlineKeyboardButton("Close 🔐", callback_data = "close")
                ],
            ]
        )
        await bot.edit_text(
            text = "",
            reply_markup = button_call,
            disable_web_page_preview = True, 
            parse_mode=enums.ParseMode.HTML
        )
    '''
