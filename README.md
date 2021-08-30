![FUZION LEECH](https://telegra.ph/file/213b587eee775e34ca221.jpg)
## FuZionX Leech Bot 
![GitHub Repo stars](https://img.shields.io/github/stars/5MysterySD/Tele-LeechX?color=blue&style=flat)
![GitHub forks](https://img.shields.io/github/forks/5MysterySD/Tele-LeechX?color=green&style=flat)
![GitHub contributors](https://img.shields.io/github/contributors/5MysterySD/Tele-LeechX?style=flat)
![GitHub watchers](https://img.shields.io/github/watchers/5MysterySD/Tele-LeechX)

**A Powerful Leech Bot .**

## Features Supported :-
<details>
    <summary><b>Click Here For Description</b></summary>

### From Original Repo :
- Google Drive link cloning using gclone.(wip)
- Telegram File mirrorring to cloud along with its unzipping, unrar and untar
- Drive/Teamdrive support/All other cloud services rclone.org supports
- Unzip, Unrar, Untar while Leeching to Telegram .
- Custom file name (Used in Prefix on Every Item Leeched)
- Custom commands for Using in Telegram .
- Get total size of your working cloud directory
- You can also upload files downloaded from `/ytdl` command to gdrive using `/ytdl gdrive` command.
- You can also deploy this on your VPS .
- Option to select either video will be uploaded as document or streamable
- Added `/renewme` command to clear the downloads which are not deleted automatically.
- Added support for YouTube Playlist .
- Renaming of Telegram files support added. 😐
- Changing rclone destination config on fly (By using `/rlcone` in private mode)

### From Different Repos :
- Aria2 configs In Root
- Small FIX for Gclone
- Unzip Error Fixed
- Added Dynamic Config 
- Added Custom ToggleDoc and ToggleVid Commands
- Added Custom Rename Command via vars
- Added direct rclone.conf url in vars

### New In Repo :
- UI Added for Improved User Experience with Easy to Use.
- Added New Status Bar using `/status` command. 
- Direct links Supported:
```
letsupload.io, hxfile.co, anonfiles.com, bayfiles.com, antfiles,
fembed.com, fembed.net, femax20.com, layarkacaxxi.icu, fcdn.stream,
sbplay.org, naniplay.com, naniplay.nanime.in, naniplay.nanime.biz, sbembed.com,
streamtape.com, streamsb.net, feurl.com, pixeldrain.com, racaty.net,
1fichier.com, 1drv.ms (Only works for file not folder or business account), solidfiles.com 
```

</details>

## Mandatory Variables :-
<details>
    <summary><b>Click Here For Description</b></summary>

* `TG_BOT_TOKEN`: Create a Bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API Token.

* `APP_ID`: Get this Value from [my.telegram.org/apps](https://my.telegram.org/apps).

* `API_HASH`: Get this Value from [my.telegram.org/apps](https://my.telegram.org/apps).
  * NOTE: If Telegram is blocked by your ISP, try Telegram to get the IDs.

* `AUTH_CHANNEL`: Create a Super(Means Changing it to `Visible` for `Chat History for New Members`) in Telegram, forward a Message from the Group to `@ShowJsonBot` to get this value.

* `OWNER_ID`: ID of the Bot Owner, He/She can be abled to access bot in bot only mode too(`Private mode`).

</details>

## Optional Configuration Variables :-

<details>
    <summary><b>Click Here For Description</b></summary>

* `DOWNLOAD_LOCATION`

* `MAX_FILE_SIZE`

* `TG_MAX_FILE_SIZE`

* `FREE_USER_MAX_FILE_SIZE`

* `MAX_TG_SPLIT_FILE_SIZE`

* `CHUNK_SIZE`

* `MAX_MESSAGE_LENGTH`

* `PROCESS_MAX_TIMEOUT`

* `ARIA_TWO_STARTED_PORT`

* `EDIT_SLEEP_TIME_OUT`

* `MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START`

* `FINISHED_PROGRESS_STR`

* `UN_FINISHED_PROGRESS_STR`

* `TG_OFFENSIVE_API`

* `CUSTOM_FILE_NAME`

* `LEECH_COMMAND`

* `YTDL_COMMAND`

* `GYTDL_COMMAND`

* `GLEECH_COMMAND`

* `TELEGRAM_LEECH_COMMAND`

* `TELEGRAM_LEECH_UNZIP_COMMAND`

* `PYTDL_COMMAND`

* `CLONE_COMMAND_G`

* `UPLOAD_COMMAND`

* `RENEWME_COMMAND`

* `SAVE_THUMBNAIL`

* `CLEAR_THUMBNAIL`

* `GET_SIZE_G`

* `UPLOAD_AS_DOC`: Takes two option True or False. If True file will be uploaded as document. This is for people who wants video files as document instead of streamable.

* `INDEX_LINK`: (Without `/` at last of the link, otherwise u will get error) During creating index, plz fill `Default Root ID` with the id of your `DESTINATION_FOLDER` after creating. Otherwise index will not work properly.

* `DESTINATION_FOLDER`: Name of your folder in ur respective drive where you want to upload the files using the bot.

</details>

## ARE YOU NEW ??? Then READ Full 👉 [Instructions](https://github.com/5MysterySD/Tele-LeechX/blob/master/About-Leech.md)

## Deploying on Heroku
- Deploying on Heroku Directly, Please Don't Abuse it. 

<p><a href="https://heroku.com/deploy?template=https://github.com/5MysterySD/Tele-LeechX/tree/master)"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200""/></a></p>

## Credits Goes To : 
* [`MysterySD`](https://github.com/5MysterySD) (Meh !!) For Direct Link Support. 
* [`KGK06`](https://github.com/KGK06) Adding Features from Different Repos.
* [`XcodersHub`](https://github.com/XcodersHub) for Modding 🙄 
* [`GautamKumar`](https://github.com/gautamajay52/TorrentLeech-Gdrive) 😬
* [`SpEcHiDe`](https://github.com/SpEcHiDe/PublicLeech) for his wonderful code😚
* [`Rclone Team`](https://rclone.org) for theirs awesome tool☁️
* [`Dan Tès`](https://telegram.dog/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
* [`Robots`](https://telegram.dog/Robots) for their [@UploadBot](https://telegram.dog/UploadBot)
* [`@AjeeshNair`](https://telegram.dog/AjeeshNait) for his [torrent.ajee.sh](https://torrent.ajee.sh)
* [`@gotstc`](https://telegram.dog/gotstc), @aryanvikash, [@HasibulKabir](https://telegram.dog/HasibulKabir) for their TORRENT groups
  [![CopyLeft](https://telegra.ph/file/b514ed14d994557a724cb.jpg)](https://telegra.ph/file/fab1017e21c42a5c1e613.mp4 "CopyLeft Credit Video")
