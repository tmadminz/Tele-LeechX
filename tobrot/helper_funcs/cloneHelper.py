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
import subprocess

import pyrogram.types as pyrogram
import requests
from tobrot import (
    DESTINATION_FOLDER,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    INDEX_LINK,
    LOGGER,
    RCLONE_CONFIG,
    TG_MAX_FILE_SIZE,
    UPLOAD_AS_DOC,
)
from tobrot.plugins import is_appdrive_link, is_gdtot_link
from tobrot.helper_funcs.direct_link_generator import gdtot, appdrive_dl, url_link_generate
from re import search
from urllib.parse import parse_qs, urlparse

class CloneHelper:
    def __init__(self, mess):
        self.g_id = ""
        self.mess = mess
        self.name = ""
        self.out = b""
        self.err = b""
        self.lsg = ""
        self.filee = ""
        self.u_id = self.mess.from_user.id
        self.u_men = self.mess.from_user.mention
        self.dname = ""

    def config(self):
        if not os.path.exists("rclone.conf"):
            with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
                fole.write(f"{RCLONE_CONFIG}")
        if os.path.exists("rclone.conf"):
            with open("rclone.conf", "r+") as file:
                con = file.read()
                self.dname = re.findall("\[(.*)\]", con)[0]

    async def get_id(self):
        mes = self.mess
        reply_to = mes.reply_to_message
        mystery = mes.text.split(" ", maxsplit=1)
        if len(mystery) > 1:
            txt = mystery[1]
        else:
            txt = reply_to.text 
        mess = txt.split("|", maxsplit=1)
        LOGGER.info(txt)
        def_text = f"__⚡️Clone Initiated⚡️__\n\n👤 **User** : {self.u_men} ( #ID{self.u_id} )\n"
        if is_gdtot_link(mess[0]):
            process = await mes.reply_text(f"{def_text}**📎 GDToT Link** : `{mess[0]}`\n\n `Generating . . .`")
            info_parsed = gdtot(mess[0])
            message = info_parsed['gdrive_link']
            await process.edit_text(f"{def_text}**📎GDToT Link** : `{mess[0]}`\n**☁️ GDrive Link** : `{message}`")
        elif is_appdrive_link(mess[0]):
            process = await mes.reply_text(f"{def_text}**📎 AppDrive Link** : `{mess[0]}`\n\n `Generating . . .`")
            info_parsed = appdrive_dl(mess[0], is_direct=False)
            message = info_parsed['gdrive_link']
            await process.edit_text(f"{def_text}**📎 AppDrive Link** : `{mess[0]}`\n**☁️ GDrive Link** : `{message}`")
        elif "kolop.icu" in mess[0]:
            process = await mes.reply_text(f"{def_text}**📎 Kolop Link** : `{mess[0]}`\n\n `Generating . . .`")
            info_parsed = url_link_generate(mess[0])
            message = info_parsed['gdrive_url']
            await process.edit_text(f"{def_text}**📎 Kolop Link** : `{mess[0]}`\n**☁️ GDrive Link** : `{message}`")
        elif "hubdrive.cc" in mess[0]:
            process = await mes.reply_text(f"{def_text}**📎 HubDrive Link** : `{mess[0]}`\n\n `Generating . . .`")
            info_parsed = url_link_generate(mess[0])
            message = info_parsed['gdrive_url']
            await process.edit_text(f"{def_text}**📎 HubDrive Link** : `{mess[0]}`\n**☁️ GDrive Link** : `{message}`")
        elif "drivelinks.in" in mess[0]:
            process = await mes.reply_text(f"{def_text}**📎 DriveLinks Link** : `{mess[0]}`\n\n `Generating . . .`")
            info_parsed = appdrive_dl(mess[0], is_direct=False)
            message = info_parsed['gdrive_link']
            await process.edit_text(f"{def_text}**📎 DriveLinks Link** : `{mess[0]}`\n**☁️ GDrive Link** : `{message}`")
        elif "drive.google.com" in mess[0]:
            await mes.reply_text(f"{def_text}**☁️ GDrive Link** : `{mess[0]}`")
            message = mess[0]
        else:
            await mes.reply_text(f"**Unsupported Link** : `{mess[0]}`")
            return
        if len(mess) == 2:
            self.g_id = self.getIdFromUrl(message)
            LOGGER.info(self.g_id)
            self.name = mess[1]
            LOGGER.info(self.name)
        else:
            self.g_id = self.getIdFromUrl(message)
            LOGGER.info(self.g_id)
            self.name = ""
        return self.g_id, self.name

    @staticmethod
    def getIdFromUrl(link: str):
        if "folders" in link or "file" in link:
            regex = r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)"
            res = search(regex,link)
            if res is None:
                LOGGER.info("G-Drive ID not found.")
            return res.group(3)
        parsed = urlparse(link)
        return parse_qs(parsed.query)['id'][0]

    async def link_gen_size(self):
        if self.name is not None:
            _drive = ""
            if self.name == self.filee:
                _flag = "--files-only"
                _up = "File"
                _ui = ""
            else:
                _flag = "--dirs-only"
                _up = "Folder"
                _drive = "folderba"
                _ui = "/"
            g_name = re.escape(self.name)
            LOGGER.info(g_name)
            destination = f"{DESTINATION_FOLDER}"

            with open("filter1.txt", "w+", encoding="utf-8") as filter1:
                print(f"+ {g_name}{_ui}\n- *", file=filter1)

            g_a_u = [
                "rclone",
                "lsf",
                "--config=./rclone.conf",
                "-F",
                "i",
                "--filter-from=./filter1.txt",
                f"{_flag}",
                f"{self.dname}:{destination}",
            ]
            LOGGER.info(g_a_u)
            gau_tam = await asyncio.create_subprocess_exec(
                *g_a_u, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            gau, tam = await gau_tam.communicate()
            LOGGER.info(gau)
            gautam = gau.decode("utf-8")
            LOGGER.info(gautam)
            LOGGER.info(tam.decode("utf-8"))

            if _drive == "folderba":
                gautii = f"https://drive.google.com/folderview?id={gautam}"
            else:
                gautii = f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"

            LOGGER.info(gautii)
            gau_link = re.search("(?P<url>https?://[^\s]+)", gautii).group("url")
            LOGGER.info(gau_link)
            button = []
            button.append(
                [
                    pyrogram.InlineKeyboardButton(
                        text="☁️ GDrive Link ☁️", url=f"{gau_link}"
                    )
                ]
            )
            if INDEX_LINK:
                _idno = 1
                INDEXS = INDEX_LINK.split(" ")
                for indexes in INDEXS:
                    if _flag == "--files-only":
                        indexurl = f"{indexes}/{self.name}"
                    else:
                        indexurl = f"{indexes}/{self.name}/"
                    tam_link = requests.utils.requote_uri(indexurl)
                    LOGGER.info(tam_link)
                    button.append(
                        [
                            pyrogram.InlineKeyboardButton(
                                text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}"
                            )
                        ]
                    )
                    _idno = _idno + 1
            button_markup = pyrogram.InlineKeyboardMarkup(button)
            msg = await self.lsg.edit_text(
                f"📨 **Name** : `{self.name}`\n\n📚 **Type** : __{_up}__\n\n🗃 **Total Files** : `Calculating ..` 🛃\n📊 **Total Size** : `Calculating ..` 🛃\n\n👤 Req By: {self.u_men} ( #ID{self.u_id} )",
                reply_markup=button_markup,
            )
            g_cmd = [
                "rclone",
                "size",
                "--config=rclone.conf",
                f"{self.dname}:{destination}/{self.name}",
            ]
            LOGGER.info(g_cmd)
            gaut_am = await asyncio.create_subprocess_exec(
                *g_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            gaut, am = await gaut_am.communicate()
            g_autam = gaut.decode("utf-8")
            LOGGER.info(g_autam)
            LOGGER.info(am.decode("utf-8"))
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            g_autam = g_autam.replace("Total objects:", "🗃 **Total Files** :").replace("Total size:", "📊 **Total Size** :")
            await msg.edit_text(
                f"📨 **Name** : `{self.name}`\n\n📚 **Type** : __{_up}__\n\n{g_autam}\n👤 Req By: {self.u_men} ( #ID{self.u_id} )",
                reply_markup=button_markup,
            )

    async def gcl(self):
        self.lsg = await self.mess.reply_text(f"`♻️ Cloning GDrive Link`")
        destination = f"{DESTINATION_FOLDER}"
        idd = "{" f"{self.g_id}" "}"
        cmd = [
            "/app/gautam/gclone",
            "copy",
            "--config=rclone.conf",
            f"{self.dname}:{idd}",
            f"{self.dname}:{destination}/{self.name}",
            "-v",
            "--drive-server-side-across-configs",
            "--transfers=16",
            "--checkers=20",
        ]
        LOGGER.info(cmd)
        pro = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        p, e = await pro.communicate()
        self.out = p
        LOGGER.info(self.out)
        err = e.decode()
        LOGGER.info(err)
        LOGGER.info(self.out.decode())

        try:
            if self.name == "":
                reg_f = "INFO(.*)(:)(.*)(:) (Copied)"
                file_n = re.findall(reg_f, err)
                self.name = file_n[0][2].strip()
                LOGGER.info(file_n[0][2].strip())
                self.filee = self.name
        except IndexError:
            await asyncio.sleep(3)
            await self.lsg.delete()
            await gcl(self)
        except Exception as err:
            LOGGER.info(err)
            await self.lsg.edit_text(f"‼️ **ERROR** ‼️\n\n`{err}`")
            
