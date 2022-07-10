from tobrot import (
    LEECH_COMMAND,
    LEECH_UNZIP_COMMAND,
    LEECH_ZIP_COMMAND,
    YTDL_COMMAND, 
    STATUS_COMMAND,
    SAVE_THUMBNAIL,
    CLEAR_THUMBNAIL,
    LOG_COMMAND,
    RENAME_COMMAND,
    TOGGLE_VID,
    TOGGLE_DOC,
    HELP_COMMAND,
    SPEEDTEST,
    TSEARCH_COMMAND,
    PYTDL_COMMAND,
    MEDIAINFO_CMD,
    BOT_NO
    )

class _BotCommands:
    def __init__(self):
        self.LeechCommand = f'{LEECH_COMMAND}{BOT_NO}'
        self.ExtractCommand = f'{LEECH_UNZIP_COMMAND}{BOT_NO}'
        self.ArchiveCommand = f'{LEECH_ZIP_COMMAND}{BOT_NO}'
        self.ToggleDocCommand = f'{TOGGLE_DOC}{BOT_NO}'
        self.ToggleVidCommand = f'{TOGGLE_VID}{BOT_NO}'
        self.SaveCommand = f'{SAVE_THUMBNAIL}{BOT_NO}'
        self.ClearCommand = f'{CLEAR_THUMBNAIL}{BOT_NO}'
        self.RenameCommand = f'{RENAME_COMMAND}{BOT_NO}'
        self.StatusCommand = f'{STATUS_COMMAND}{BOT_NO}'
        self.SpeedCommand = f'{SPEEDTEST}{BOT_NO}'
        self.YtdlCommand = f'{YTDL_COMMAND}{BOT_NO}'
        self.PytdlCommand = f'{PYTDL_COMMAND}{BOT_NO}'
        self.HelpCommand = f'{HELP_COMMAND}{BOT_NO}'
        self.LogCommand = f'{LOG_COMMAND}{BOT_NO}'
        self.MediaInfoCommand = f'{MEDIAINFO_CMD}{BOT_NO}'
        self.TsHelpCommand = f'{TSEARCH_COMMAND}{BOT_NO}'

BotCommands = _BotCommands()
