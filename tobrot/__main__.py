#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


import io
import logging
import os
import sys
import traceback
import datetime 

from telegram import ParseMode
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters, idle
from pyrogram.raw import functions, types
from pyrogram.handlers import CallbackQueryHandler, MessageHandler

from tobrot import app, bot, dispatcher, userBot
from tobrot import (
    OWNER_ID,
    AUTH_CHANNEL,
    CANCEL_COMMAND_G,
    CLEAR_THUMBNAIL,
    CLONE_COMMAND_G,
    DOWNLOAD_LOCATION,
    GET_SIZE_G,
    GLEECH_COMMAND,
    GLEECH_UNZIP_COMMAND,
    GLEECH_ZIP_COMMAND,
    LEECH_COMMAND,
    LEECH_UNZIP_COMMAND,
    LEECH_ZIP_COMMAND,
    LOG_COMMAND,
    LOGGER,
    PYTDL_COMMAND,
    RENEWME_COMMAND,
    RENAME_COMMAND,
    SAVE_THUMBNAIL,
    STATUS_COMMAND,
    TELEGRAM_LEECH_UNZIP_COMMAND,
    TELEGRAM_LEECH_COMMAND,
    UPLOAD_COMMAND,
    YTDL_COMMAND,
    GYTDL_COMMAND,
    GPYTDL_COMMAND,
    TOGGLE_VID,
    RCLONE_COMMAND,
    TOGGLE_DOC,
    HELP_COMMAND,
    SPEEDTEST,
    TSEARCH_COMMAND,
    MEDIAINFO_CMD,
    UPDATES_CHANNEL,
    SERVER_HOST
)
from tobrot.helper_funcs.download import down_load_media_f
from tobrot.helper_funcs.direct_link_generator import url_link_generate
from tobrot.plugins import *
from tobrot.plugins.call_back_button_handler import button
# the logging things
from tobrot.plugins.imdb import imdb_search, imdb_callback 
from tobrot.plugins.torrent_search import searchhelp, sendMessage 
from tobrot.plugins.custom_utils import prefix_set, caption_set, template_set
from tobrot.plugins.url_parser import url_parser
from tobrot.helper_funcs.bot_commands import BotCommands
from tobrot.plugins.choose_rclone_config import rclone_command_f
from tobrot.plugins.custom_thumbnail import clear_thumb_nail, save_thumb_nail
from tobrot.plugins.incoming_message_fn import (g_clonee, g_yt_playlist,
                                                incoming_message_f,
                                                incoming_purge_message_f,
                                                incoming_youtube_dl_f,
                                                rename_tg_file)
from tobrot.plugins.new_join_fn import help_message_f, new_join_f
from tobrot.plugins.speedtest import get_speed
from tobrot.plugins.mediainfo import mediainfo
from tobrot.plugins.rclone_size import check_size_g, g_clearme
from tobrot.plugins.status_message_fn import (
    cancel_message_f,
    eval_message_f,
    exec_message_f,
    status_message_f,
    upload_document_f,
    upload_log_file,
    upload_as_doc,
    upload_as_video
)

botcmds = [
        (f'{BotCommands.LeechCommand}','📨 [Reply] Leech any Torrent/ Magnet/ Direct Link '),
        (f'{BotCommands.ExtractCommand}', '🔐 Unarchive items . .'),
        (f'{BotCommands.ArchiveCommand}','🗜 Archive as .tar.gz acrhive... '),
        (f'{BotCommands.ToggleDocCommand}','📂 Toggle to Document Upload '),
        (f'{BotCommands.ToggleVidCommand}','🎞 Toggle to Streamable Upload '),
        (f'{BotCommands.SaveCommand}','🖼 Save Thumbnail For Uploads'),
        (f'{BotCommands.ClearCommand}','🕹 Clear Thumbnail '),
        (f'{BotCommands.RenameCommand}','📧 [Reply] Rename Telegram File '),
        (f'{BotCommands.StatusCommand}','🖲 Show Bot stats and concurrent Downloads'),
        (f'{BotCommands.SpeedCommand}','📡 Get Current Server Speed of Your Bot'),
        (f'{BotCommands.YtdlCommand}','🧲 [Reply] YT-DL Links for Uploading...'),
        (f'{BotCommands.PytdlCommand}','🧧 [Reply] YT-DL Playlists Links for Uploading...'),
        (f'gclone','♻️ [G-Drive] Clone Different Supported Sites !!'),
        (f'{BotCommands.MediaInfoCommand}','🆔️ [Reply] Get Telegram Files Media Info'),
        (f'setpre','🔠 <Text> Save Custom Prefix for Uploads'),
        (f'setcap','🔣 <Text> Save Custom Caption for Uploads'),
        (f'parser','🧮 <URL> Get Bypassed Link After Parsing !!'),
        (f'imdb','🎬 [Title] Get IMDb Details About It !!'),
        (f'set_template','📋 [HTML] Set IMDb Custom Template for Usage!!'),
        (f'{BotCommands.HelpCommand}','🆘 Get Help, How to Use and What to Do. . .'),
        (f'{BotCommands.LogCommand}','🔀 Get the Bot Log [Owner Only]'),
        (f'{BotCommands.TsHelpCommand}','🌐 Get help for Torrent Search Module'),
    ]

async def start(client, message):
    """/start command"""
    buttons = [
            [
                InlineKeyboardButton('🚦 Bot Stats 🚦', url='https://t.me/FXTorrentz/28'),
                InlineKeyboardButton('🛃 FX Group 🛃', url='https://t.me/+BgIhdNizM61jOGNl'),
            ]
            ]
    reply_markup=InlineKeyboardMarkup(buttons)
    u_men = message.from_user.mention 
    start_string = f'''
┏ <i>Dear {u_men}</i>,
┃
┃ <i>If You Want To Use Me, You Have To Join @FXTorrentz</i>
┃
┣ <b>NOTE:</b> <code>All The Uploaded Leeched Contents By You Will Be Sent Here In Your Private Chat From Now.</code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️
'''
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text(
           start_string,
           reply_markup=reply_markup,
           parse_mode=enums.ParseMode.HTML,
           quote=True
        )
    else:
        await message.reply_text(f"**I Am Alive and Working, Send /help to Know How to Use Me !** ✨", parse_mode=enums.ParseMode.MARKDOWN)


def restart(client, message): 
    restart_message = sendMessage("Restarting, Please wait!", message.tobrot, client)
    with open(".restartmsg", "w") as f: 
        f.truncate(0)       
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n") 
    clean_all()
    os.execl(executable, executable, "-m", "bot")


if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)

    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
    ist = ist_now.strftime("<b>📆 𝘿𝙖𝙩𝙚 :</b> <code>%d/%m/%Y</code> \n<b>⏰ 𝙏𝙞𝙢𝙚 :</b> <code>%H:%M:%S (GMT+05:30)</code>")

    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("Restarted successfully!", chat_id, msg_id)
        os.remove(".restartmsg")
    elif OWNER_ID:
        try:
            text = f"<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !!</b>\n\n<b>📊 𝙃𝙤𝙨𝙩 :</b> <code>{SERVER_HOST}</code>\n{ist}\n\n<b>ℹ️ 𝙑𝙚𝙧𝙨𝙞𝙤𝙣 :</b> <code>3.2.15</code>"
            #bot.sendMessage(chat_id=OWNER_ID, text=text, parse_mode=enums.ParseMode.HTML)
            if AUTH_CHANNEL:
                for i in AUTH_CHANNEL:
                    bot.sendMessage(chat_id=i, text=text, parse_mode=ParseMode.HTML)
        except Exception as e:
            LOGGER.warning(e)

    bot.set_my_commands(botcmds)

    # Starting The Bot
    userBot.start()
    app.start()
    
    ##############################################################################
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=filters.command(
            [
                LEECH_COMMAND, f"{LEECH_COMMAND}@{bot.username}",
                LEECH_ZIP_COMMAND, f"{LEECH_ZIP_COMMAND}@{bot.username}",
                LEECH_UNZIP_COMMAND, f"{LEECH_UNZIP_COMMAND}@{bot.username}",
                GLEECH_COMMAND,
                GLEECH_UNZIP_COMMAND,
                GLEECH_ZIP_COMMAND,
            ]
        )
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_message_handler)
    ##############################################################################
    incoming_telegram_download_handler = MessageHandler(
        down_load_media_f,
        filters=filters.command([TELEGRAM_LEECH_COMMAND, TELEGRAM_LEECH_UNZIP_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_telegram_download_handler)
    ##############################################################################
    incoming_purge_message_handler = MessageHandler(
        incoming_purge_message_f,
        filters=filters.command(["purge"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_purge_message_handler)
    ##############################################################################
    incoming_clone_handler = MessageHandler(
        g_clonee,
        filters=filters.command([f"{CLONE_COMMAND_G}", f"{CLONE_COMMAND_G}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_clone_handler)
    ##############################################################################
    incoming_size_checker_handler = MessageHandler(
        check_size_g,
        filters=filters.command([f"{GET_SIZE_G}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_size_checker_handler)
    ##############################################################################
    incoming_g_clear_handler = MessageHandler(
        g_clearme,
        filters=filters.command([f"{RENEWME_COMMAND}", f"{RENEWME_COMMAND}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_g_clear_handler)
    ##############################################################################
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=filters.command([f"{YTDL_COMMAND}", f"{YTDL_COMMAND}@{bot.username}", f"{GYTDL_COMMAND}", f"{GYTDL_COMMAND}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_dl_handler)
    ##############################################################################
    incoming_youtube_playlist_dl_handler = MessageHandler(
        g_yt_playlist,
        filters=filters.command([f"{PYTDL_COMMAND}", f"{PYTDL_COMMAND}@{bot.username}", GPYTDL_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_playlist_dl_handler)
    ##############################################################################
    status_message_handler = MessageHandler(
        status_message_f,
        filters=filters.command([f"{STATUS_COMMAND}", f"{STATUS_COMMAND}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(status_message_handler)
    ##############################################################################
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=filters.command([f"{CANCEL_COMMAND_G}", f"{CANCEL_COMMAND_G}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(cancel_message_handler)
    ##############################################################################
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=filters.command(["exec", "gdtot", "gdtot@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(exec_message_handler)
    ##############################################################################
    eval_message_handler = MessageHandler(
        eval_message_f,
        filters=filters.command(["eval"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(eval_message_handler)
    ##############################################################################
    rename_message_handler = MessageHandler(
        rename_tg_file,
        filters=filters.command([f"{RENAME_COMMAND}", f"{RENAME_COMMAND}@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(rename_message_handler)
    ##############################################################################
    upload_document_handler = MessageHandler(
        upload_document_f,
        filters=filters.command([f"{UPLOAD_COMMAND}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_document_handler)
    ##############################################################################
    upload_log_handler = MessageHandler(
        upload_log_file,
        filters=filters.command([f"{LOG_COMMAND}", f"{LOG_COMMAND}@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_log_handler)
    ##############################################################################
    help_text_handler = MessageHandler(
        help_message_f,
        filters=filters.command([f"{HELP_COMMAND}", f"{HELP_COMMAND}@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(help_text_handler)
    ##############################################################################
    '''
    new_join_handler = MessageHandler(
        new_join_f, filters=~filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)
    ##############################################################################
    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=filters.chat(chats=AUTH_CHANNEL) & filters.new_chat_members,
    )
    app.add_handler(group_new_join_handler)
    '''
    ##############################################################################
    call_back_button_handler = CallbackQueryHandler(button)
    app.add_handler(call_back_button_handler)
    ##############################################################################
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=filters.command([f"{SAVE_THUMBNAIL}", f"{SAVE_THUMBNAIL}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(save_thumb_nail_handler)
    ##############################################################################
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=filters.command([f"{CLEAR_THUMBNAIL}", f"{CLEAR_THUMBNAIL}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(clear_thumb_nail_handler)
    ##############################################################################
    rclone_config_handler = MessageHandler(
        rclone_command_f, filters=filters.command([f"{RCLONE_COMMAND}"])
    )
    app.add_handler(rclone_config_handler)
    ##############################################################################
    upload_as_doc_handler = MessageHandler(
        upload_as_doc,
        filters=filters.command([f"{TOGGLE_DOC}", f"{TOGGLE_DOC}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_as_doc_handler)
    ##############################################################################
    upload_as_video_handler = MessageHandler(
        upload_as_video,
        filters=filters.command([f"{TOGGLE_VID}", f"{TOGGLE_VID}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_as_video_handler)
    ##############################################################################
    get_speed_handler = MessageHandler(
        get_speed,
        filters=filters.command([f"{SPEEDTEST}", f"{SPEEDTEST}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(get_speed_handler)
    ##############################################################################
    searchhelp_handler = MessageHandler(
        searchhelp,
        filters=filters.command([f"{TSEARCH_COMMAND}", f"{TSEARCH_COMMAND}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(searchhelp_handler)
    ##############################################################################
    mediainfo_handler = MessageHandler(
        mediainfo,
        filters=filters.command([f"{MEDIAINFO_CMD}", f"{MEDIAINFO_CMD}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(mediainfo_handler)
    ##############################################################################
    restart_handler = MessageHandler(
        restart,
        filters=filters.command(["restart", f"restart@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(restart_handler)
    ##############################################################################
    start_handler = MessageHandler(
        start,
        filters=filters.command(["start", f"start@{bot.username}"])
    )
    app.add_handler(start_handler)
    ##############################################################################
    prefixx_handler = MessageHandler(
        prefix_set,
        filters=filters.command(["setpre", f"setpre@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(prefixx_handler)
    ##############################################################################
    captionn_handler = MessageHandler(
        caption_set,
        filters=filters.command(["setcap", f"setcap@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(captionn_handler)
    ##############################################################################
    url_parse_handler = MessageHandler(
        url_parser,
        filters=filters.command(["parser", f"parser@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(url_parse_handler)
    ##############################################################################
    imdb_handler = MessageHandler(
        imdb_search,
        filters=filters.command(["imdb", f"imdb@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(imdb_handler)
    ##############################################################################
    template_handler = MessageHandler(
        template_set,
        filters=filters.command(["set_template", f"set_template@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(template_handler)
    ##############################################################################

        #$$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\   
        #\______|\______|\______|\______|\______|\______|\______|\______|\______|\______|\______|\______|  
        #
        #$$$$$$$$\        $$\                   $$\                                    $$\       $$\   $$\ 
        #\__$$  __|       $$ |                  $$ |                                   $$ |      $$ |  $$ |
        #   $$ | $$$$$$\  $$ | $$$$$$\          $$ |      $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$$\  \$$\ $$  |
        #   $$ |$$  __$$\ $$ |$$  __$$\ $$$$$$\ $$ |     $$  __$$\ $$  __$$\ $$  _____|$$  __$$\  \$$$$  / 
        #   $$ |$$$$$$$$ |$$ |$$$$$$$$ |\______|$$ |     $$$$$$$$ |$$$$$$$$ |$$ /      $$ |  $$ | $$  $$<  
        #   $$ |$$   ____|$$ |$$   ____|        $$ |     $$   ____|$$   ____|$$ |      $$ |  $$ |$$  /\$$\ 
        #   $$ |\$$$$$$$\ $$ |\$$$$$$$\         $$$$$$$$\\$$$$$$$\ \$$$$$$$\ \$$$$$$$\ $$ |  $$ |$$ /  $$ |
        #   \__| \_______|\__| \_______|        \________|\_______| \_______| \_______|\__|  \__|\__|  \__|
        #
        #$$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\ $$$$$$\   
        #\______|\______|\______|\______|\______|\______|\______|\______|\______|\______|\______|\______|

    logging.info('''
______                 ______ ____  __
___  / ___________________  /___  |/ /
__  /  _  _ \  _ \  ___/_  __ \_    / 
_  /___/  __/  __/ /__ _  / / /    |  
/_____/\___/\___/\___/ /_/ /_//_/|_|  

    ''')
    logging.info(f"{(app.get_me()).first_name} [@{(app.get_me()).username}] Has Started Running...🏃💨💨")
    logging.info(f"User : {(userBot.get_me()).first_name} Has Started Revolving...♾️⚡️")

    idle()
    
    app.stop()
    userBot.stop()
