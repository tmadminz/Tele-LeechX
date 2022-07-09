#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


import asyncio
import io
import logging
import os
import shutil
import sys
import time
import traceback
import psutil
import math

from pyrogram.errors import FloodWait, MessageIdInvalid, MessageNotModified
from pyrogram import enums
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot import (
    AUTH_CHANNEL,
    BOT_START_TIME,
    LOGGER,
    MAX_MESSAGE_LENGTH, 
    user_specific_config,
    gid_dict,
    _lock,
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    UPDATES_CHANNEL,
    CANCEL_COMMAND_G
    )
# the logging things
from tobrot.helper_funcs.display_progress import TimeFormatter, humanbytes
from tobrot.helper_funcs.download_aria_p_n import aria_start, call_apropriate_function
from tobrot.helper_funcs.upload_to_tg import upload_to_tg
from tobrot.UserDynaConfig import UserDynaConfig

async def upload_as_doc(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,True)
    u_men = message.from_user.mention
    await message.reply_text(f"┏━━ 🛠  𝗧𝗼𝗴𝗴𝗹𝗲 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 :\n┣👤 𝐔𝐬𝐞𝐫 : {u_men} \n┣🆔️ 𝐈𝐃 : #ID{message.from_user.id}\n┃\n┣🏷 𝐓𝐨𝐠𝐠𝐥𝐞 : 📁<code>Document 📂</code>\n┃\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹")


async def upload_as_video(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,False)
    u_men = message.from_user.mention
    await message.reply_text(f"┏━━ 🛠  𝗧𝗼𝗴𝗴𝗹𝗲 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 :\n┣👤 𝐔𝐬𝐞𝐫 : {u_men} \n┣🆔️ 𝐈𝐃 : #ID{message.from_user.id}\n┃\n┣🏷𝐓𝐨𝐠𝐠𝐥𝐞 : <code>🎞 Video 🎞</code>\n┃\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹")
 

async def status_message_f(
    client, message
):  # weird code but 'This is the way' @gautamajay52
    aria_i_p = await aria_start()
    # Show All Downloads
    to_edit = await message.reply("🧭 𝐆𝐞𝐭𝐭𝐢𝐧𝐠 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐒𝐭𝐚𝐭𝐮𝐬 . .")
    chat_id = int(message.chat.id)
    mess_id = int(to_edit.id)
    async with _lock:
        if len(gid_dict[chat_id]) == 0:
            gid_dict[chat_id].append(mess_id)
        else:
            if not mess_id in gid_dict[chat_id]:
                await client.delete_messages(chat_id, gid_dict[chat_id])
                gid_dict[chat_id].pop()
                gid_dict[chat_id].append(mess_id)

    prev_mess = "By gautamajay52"
    await message.delete()
    while True:
        downloads = aria_i_p.get_downloads()
        msg = ""
        for file in downloads:
            downloading_dir_name = "N/A"
            try:
                downloading_dir_name = str(file.name)
            except:
                pass
            if file.status == "active":
                is_file = file.seeder
                if is_file is None:
                    msgg = f"┣🔰𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧𝐬: <code>{file.connections}</code>"
                else:
                    msgg = f"┣🔰𝐒𝐞𝐞𝐝𝐬: <code>{file.num_seeders}</code> ┃ 🔰𝐏𝐞𝐞𝐫𝐬: <code>{file.connections}</code>"

                percentage = int(file.progress_string(0).split('%')[0])
                prog = "[{0}{1}]".format("".join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 5))]),"".join([UN_FINISHED_PROGRESS_STR for i in range(20 - math.floor(percentage / 5))]))
                msg += f"\n┏━━━━━━━━━━━━━━━━╻"
                msg += f"\n┣🔰𝐍𝐚𝐦𝐞: <code>{downloading_dir_name}</code>"
                msg += f"\n┣🔰𝐒𝐭𝐚𝐭𝐮𝐬: <i>Downloading...📥</i>"
                msg += f"\n┃<code>{prog}</code>"
                msg += f"\n┣🔰𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝: <code>{file.progress_string()}</code> <b>of</b> <code>{file.total_length_string()}</code>"
                msg += f"\n┣🔰𝐒𝐩𝐞𝐞𝐝: <code>{file.download_speed_string()}</code>,"
                msg += f"🔰𝐄𝐓𝐀: <code>{file.eta_string()}</code>"  
                #umen = f'<a href="tg://user?id={file.message.from_user.id}">{file.message.from_user.first_name}</a>'
                #msg += f"\n<b>👤User:</b> {umen} (<code>{file.message.from_user.id}</code>)"
                #msg += f"\n<b>⚠️Warn:</b> <code>/warn {file.message.from_user.id}</code>"
                msg += f"\n{msgg}"
                msg += f"\n┣🔰𝐂𝐚𝐧𝐜𝐞𝐥: <code>/{CANCEL_COMMAND_G} {file.gid}</code>"
                msg += f"\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹\n"

        hr, mi, se = up_time(time.time() - BOT_START_TIME)
        total, used, free = shutil.disk_usage(".")
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)

        ms_g = (
            f"◆━━━━━━◆ ❃ ◆━━━━━━◆\n"
            f"┏━━━━━━━━━━━━━━┓\n"
            f"┃ᑕᑭᑌ: <code>{cpu}%</code> ┃ ᖇᗩᗰ: <code>{ram}%</code>  ┃\n"
            f"┃ᖴ: <code>{free}</code> ┃ᑌᑭ: <code>{hr}h{mi}m{se}s</code>┃\n"
            f"┃T: <code>{total}</code> ┃ᑌ: <code>{used}</code>┃\n"
            f"┗━━━━━━━━━━━━━━┛"
        )

        umen = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
        mssg = f"\n❣𝙎𝙩𝙖𝙩𝙪𝙨 𝙍𝙚𝙦𝙪𝙚𝙨𝙩𝙚𝙙 𝘽𝙮 : {umen} (<code>{message.from_user.id}</code>)\n◆━━━━━━◆ ❃ ◆━━━━━━◆"
        if msg == "":
            msg = f"\n┏━━━━━━━━━━━━━━━╻\n┃\n┃ ⚠️ <b>No Active, Queued or Paused \n┃ Torrents / Direct Links ⚠️</b>\n┃\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹\n"
            msg = mssg + "\n" + msg + "\n" + ms_g
            await to_edit.edit(msg)
            break
        msg = mssg + "\n" + msg + "\n" + ms_g
        if len(msg) > MAX_MESSAGE_LENGTH:  # todo - will catch later
            with io.BytesIO(str.encode(msg)) as out_file:
                out_file.name = "status.text"
                await client.send_document(
                    chat_id=message.chat.id,
                    document=out_file,
                )
            break
        else:
            if msg != prev_mess:
                try:
                    await to_edit.edit(msg, parse_mode=enums.ParseMode.HTML)
                except MessageIdInvalid as df:
                    break
                except MessageNotModified as ep:
                    LOGGER.info(ep)
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                except FloodWait as e:
                    LOGGER.info(e)
                    time.sleep(e.value)
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                prev_mess = msg


async def cancel_message_f(client, message):
    if len(message.command) > 1:
        # /cancel command
        i_m_s_e_g = await message.reply_text("<code>Checking..⁉️</code>", quote=True)
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        try:
            downloads = aria_i_p.get_download(g_id)
            name = downloads.name
            size = downloads.total_length_string()
            gid_list = downloads.followed_by_ids
            downloads = [downloads]
            if len(gid_list) != 0:
                downloads = aria_i_p.get_downloads(gid_list)
            aria_i_p.remove(downloads=downloads, force=True, files=True, clean=True)
            await i_m_s_e_g.edit_text(
                f"⛔<b> Download Cancelled </b>⛔ :\n<code>{name} ({size})</code> By <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
            )
        except Exception as e:
            await i_m_s_e_g.edit_text("<i>⚠️ FAILED ⚠️</i>\n\n" + str(e) + "\n#Error")
    else:
        await message.delete()


async def exec_message_f(client, message):
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]
    link = message.text.split(' ', maxsplit=1)[1]
    work_in = await message.reply_text("`Generating ...`")

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "No Output"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"<b>QUERY:\n\nLink: {link} \n\nPID: {process.pid}</b>\n\n<b>Stderr: \n{e}\nOutput:\n\n {o}</b> "
    await work_in.delete()

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "shell.txt"
            await client.send_document(
                chat_id=message.chat.id,
                document=out_file,
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id,
            )
        await message.delete()
    else:
        await message.reply_text(OUTPUT, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, quote=True)


async def upload_document_f(client, message):
    imsegd = await message.reply_text("processing ...")
    if message.from_user.id in AUTH_CHANNEL:
        if " " in message.text:
            recvd_command, local_file_name = message.text.split(" ", 1)
            recvd_response = await upload_to_tg(
                imsegd, local_file_name, message.from_user.id, {}, client
            )
            LOGGER.info(recvd_response)
    await imsegd.delete()


async def eval_message_f(client, message):
    if message.from_user.id in AUTH_CHANNEL:
        status_message = await message.reply_text("Processing ...")
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.id

        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None

        try:
            await aexec(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"

        final_output = (
            "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code> \n".format(
                cmd, evaluation.strip()
            )
        )

        if len(final_output) > MAX_MESSAGE_LENGTH:
            with open("eval.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(final_output))
            await message.reply_document(
                document="eval.text",
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id,
            )
            os.remove("eval.text")
            await status_message.delete()
        else:
            await status_message.edit(final_output)


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


def up_time(time_taken):
    hours, _hour = divmod(time_taken, 3600)
    minutes, seconds = divmod(_hour, 60)
    return round(hours), round(minutes), round(seconds)


async def upload_log_file(client, message):
    g = await AdminCheck(client, message.chat.id, message.from_user.id)
    if g:
        await message.reply_document("FuZionXLogs.txt")
