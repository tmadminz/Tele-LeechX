#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD 

import asyncio
import logging
import os
import time
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from sys import exit
import urllib.request
import dotenv
import telegram.ext as tg

from pyrogram import Client

if os.path.exists("TorrentLeech-Gdrive.txt"):
    with open("Torrentleech-Gdrive.txt", "r+") as f_d:
        f_d.truncate(0)

# the logging things
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "FuZionXLogs.txt", maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

user_specific_config=dict()

dotenv.load_dotenv("config.env")

# checking compulsory variable NOT NEEDED FOR OKTETO!! Just Use Your Brain
'''
for imp in ["TG_BOT_TOKEN", "APP_ID", "API_HASH", "OWNER_ID", "AUTH_CHANNEL"]:
    try:
        value = os.environ[imp]
        if not value:
            raise KeyError
    except KeyError:
        LOGGER.critical(f"Oh...{imp} is missing from config.env ... fill that")
        exit()
'''

# The Telegram API things
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "5139162631:AAHGWHHbnbu7k5jOjXW-axcNuJcSRpBktr4")
APP_ID = os.environ.get("APP_ID", "6878048")
API_HASH = os.environ.get("API_HASH", "3833ae3a7415af46df46a83a3ba2c432")
OWNER_ID = int(os.environ.get("OWNER_ID", "1242011540"))

# Get these values from my.telegram.org
# to store the channel ID who are authorized to use the bot
AUTH_CHANNEL = [int(x) for x in os.environ.get("AUTH_CHANNEL", "-1001270496331 -1001508663868").split()]

# Cuz most ppl dunno AUTH_CHANNEL also works as SUDO
SUDO_USERS = [int(sudos) if (' ' not in os.environ.get('SUDO_USERS', '')) else int(sudos) for sudos in os.environ.get('SUDO_USERS', '').split()]

# the download location, where the HTTP Server runs
DOWNLOAD_LOCATION = "./DOWNLOADS"
# Telegram maximum file upload size
MAX_FILE_SIZE = 50000000
TG_MAX_FILE_SIZE = 2097152000
FREE_USER_MAX_FILE_SIZE = 50000000
AUTH_CHANNEL.append(OWNER_ID)
AUTH_CHANNEL += SUDO_USERS
# chunk size that should be used with requests
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "128"))
# default thumbnail to be used in the videos
DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://telegra.ph/file/3a7f09b89943b51cdba38.jpg")
# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096
# set timeout for subprocess
PROCESS_MAX_TIMEOUT = 3600
#
SP_LIT_ALGO_RITH_M = os.environ.get("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = int(os.environ.get("ARIA_TWO_STARTED_PORT", "6800"))
EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", "10"))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 600))
MAX_TG_SPLIT_FILE_SIZE = int(os.environ.get("MAX_TG_SPLIT_FILE_SIZE", "1072864000"))
# add config vars for the display progress
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "■")
UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "□")
# add offensive API
TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)
CUSTOM_FILE_NAME = os.environ.get("CUSTOM_FILE_NAME", "")
LEECH_COMMAND = os.environ.get("LEECH_COMMAND", "leech")
LEECH_UNZIP_COMMAND = os.environ.get("LEECH_UNZIP_COMMAND", "extract")
LEECH_ZIP_COMMAND = os.environ.get("LEECH_ZIP_COMMAND", "archive")
GLEECH_COMMAND = os.environ.get("GLEECH_COMMAND", "gleech")
GLEECH_UNZIP_COMMAND = os.environ.get("GLEECH_UNZIP_COMMAND", "gleechunzip")
GLEECH_ZIP_COMMAND = os.environ.get("GLEECH_ZIP_COMMAND", "gleechzip")
YTDL_COMMAND = os.environ.get("YTDL_COMMAND", "ytdl")
GYTDL_COMMAND = os.environ.get("GYTDL_COMMAND", "gytdl")
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG", "")
DESTINATION_FOLDER = os.environ.get("DESTINATION_FOLDER", "Maxx-TD")
INDEX_LINK = os.environ.get("INDEX_LINK", "https://infyplexultra.mysterydemon.workers.dev/0:")
TELEGRAM_LEECH_COMMAND = os.environ.get("TELEGRAM_LEECH_COMMAND", "tleech")
TELEGRAM_LEECH_UNZIP_COMMAND = os.environ.get("TELEGRAM_LEECH_UNZIP_COMMAND", "tleechunzip")
CANCEL_COMMAND_G = os.environ.get("CANCEL_COMMAND_G", "cancel")
GET_SIZE_G = os.environ.get("GET_SIZE_G", "getsize")
STATUS_COMMAND = os.environ.get("STATUS_COMMAND", "status")
SAVE_THUMBNAIL = os.environ.get("SAVE_THUMBNAIL", "savethumb")
CLEAR_THUMBNAIL = os.environ.get("CLEAR_THUMBNAIL", "clearthumb")
UPLOAD_AS_DOC = os.environ.get("UPLOAD_AS_DOC", "False")
PYTDL_COMMAND = os.environ.get("PYTDL_COMMAND", "pytdl")
GPYTDL_COMMAND = os.environ.get("GPYTDL_COMMAND", "gpytdl")
LOG_COMMAND = os.environ.get("LOG_COMMAND", "log")
CLONE_COMMAND_G = os.environ.get("CLONE_COMMAND_G", "gclone")
UPLOAD_COMMAND = os.environ.get("UPLOAD_COMMAND", "upload")
RENEWME_COMMAND = os.environ.get("RENEWME_COMMAND", "renewme")
RENAME_COMMAND = os.environ.get("RENAME_COMMAND", "rename")
TOGGLE_VID = os.environ.get("TOGGLE_VID", "togglevid")
TOGGLE_DOC = os.environ.get("TOGGLE_DOC", "toggledoc")
RCLONE_COMMAND = os.environ.get("RCLONE_COMMAND", "rclone")
HELP_COMMAND = os.environ.get("HELP_COMMAND", "help")
SPEEDTEST = os.environ.get("SPEEDTEST", "speedtest")
TSEARCH_COMMAND = os.environ.get("TSEARCH_COMMAND", "tshelp")
MEDIAINFO_CMD = os.environ.get("MEDIAINFO_CMD", "mediainfo")
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "@FuZionX")
CAP_STYLE = os.environ.get("CAP_STYLE", "code")
UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN", "")
EMAIL = os.environ.get("EMAIL", "mysterysd.sd@gmail.com")
PWSSD = os.environ.get("PWSSD", "S#D#97531")
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "0AARBvkBdvULMUk9PVA")
CRYPT = os.environ.get("CRYPT", "S3htTzl3aDdHUWdJWDhLZVV2MlpSVGlkZ0RVYU0xc29oQlNKSENGakRaOD0%3D")
PHPSESSID = os.environ.get("PHPSESSID", "dslvec02r5mo3co40vsq6154eh")
HUB_CRYPT = os.environ.get("HUB_CRYPT", "dVAwSkpDU0FWVnNYV3hSZU40RkhrRU53RzVmdjVBbFd3RThPeFllMmhSND0%3D")
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "")
MAX_LIST_ELM = os.environ.get("MAX_LIST_ELM", None)
DEF_IMDB_TEMPLATE = os.environ.get("IMDB_TEMPLATE", """<i><b>⚡𝐓𝐢𝐭𝐥𝐞: </b> {title}
<b>⚡𝐈𝐌𝐃𝐁 𝐑𝐚𝐭𝐢𝐧𝐠 :</b> <code>{rating} </code>
<b>⚡𝐐𝐮𝐚𝐥𝐢𝐭𝐲:  </b>
<b>⚡𝐑𝐞𝐥𝐞𝐚𝐬𝐞 𝐃𝐚𝐭𝐞: </b> {release_date}
<b>⚡𝐆𝐞𝐧𝐫𝐞: </b>{genres}
<b>⚡️𝐈𝐌𝐃𝐁: </b>{url}
<b>⚡𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞:  </b>{languages}
<b>⚡𝐂𝐨𝐮𝐧𝐭𝐫𝐲: </b> {countries}
<b>⚡𝐒𝐮𝐛𝐭𝐢𝐭𝐥𝐞𝐬: </b>

<b>⚡𝐒𝐭𝐨𝐫𝐲 𝐋𝐢𝐧𝐞: </b><code>{plot}</code>

⚡️𝐉𝐨𝐢𝐧 𝐍𝐨𝐰 :  @FuZionX </i>

⚡️✅ 𝑪𝒍𝒊𝒄𝒌 𝑫𝒐𝒘𝒏 𝒂𝒏𝒅 𝑺𝒕𝒂𝒓𝒕 𝒕𝒉𝒆 𝑩𝒐𝒕 𝒕𝒐 𝑮𝒆𝒕 𝒕𝒉𝒆 𝑭𝒊𝒍𝒆 ✅ !! ⬇️ ⬇️""")
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "")
BOT_START_TIME = time.time()
# dict to control uploading and downloading
gDict = defaultdict(lambda: [])
# user settings dict #ToDo
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])
_lock = asyncio.Lock()

# Rclone Config Via any raw url
###########################################################################
try:                                                                      #
    RCLONE_CONF_URL = os.environ.get('RCLONE_CONF_URL', "")               #
    if len(RCLONE_CONF_URL) == 0:                                         #
        RCLONE_CONF_URL = None                                            #
    else:                                                                 #
        urllib.request.urlretrieve(RCLONE_CONF_URL, '/app/rclone.conf')   #
except KeyError:                                                          #
    RCLONE_CONF_URL = None                                                #
###########################################################################

def multi_rclone_init():
    if RCLONE_CONFIG:
        LOGGER.warning("Don't use this var now, put your rclone.conf in root directory")
    if not os.path.exists("rclone.conf"):
        LOGGER.warning("Sed, No rclone.conf found in root directory")
        return
    if not os.path.exists("rclone_bak.conf"):  # backup rclone.conf file
        with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
            with open("rclone.conf", "r") as f:
                fole.write(f.read())
        LOGGER.info("rclone.conf backuped to rclone_bak.conf!")


multi_rclone_init()

app = Client("LeechBot", bot_token=TG_BOT_TOKEN, api_id=APP_ID, api_hash=API_HASH, workers=343)

updater = tg.Updater(token=TG_BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher


