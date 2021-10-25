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
    BOT_NO
    )

class _BotCommands:
    def __init__(self):
        self.LeechCommand = f'{LEECH_COMMAND}'
        self.ExtractCommand = f'{LEECH_UNZIP_COMMAND}'
        self.ArchiveCommand = f'{LEECH_ZIP_COMMAND}'
        self.ToggleDocCommand = f'{TOGGLE_DOC}'
        self.ToggleVidCommand = f'{TOGGLE_VID}'
        self.SaveCommand = f'{SAVE_THUMBNAIL}'
        self.ClearCommand = f'{CLEAR_THUMBNAIL}'
        self.RenameCommand = f'{RENAME_COMMAND}'
        self.StatusCommand = f'{STATUS_COMMAND}'
        self.SpeedCommand = f'{SPEEDTEST}'
        self.YtdlCommand = f'{YTDL_COMMAND}'
        self.PytdlCommand = 'pytdl'
        self.HelpCommand = f'{HELP_COMMAND}'
        self.LogCommand = f'{LOG_COMMAND}'
        self.MediaInfoCommand = 'mediainfo'
        self.TsHelpCommand = f'{TSEARCH_COMMAND}'

BotCommands = _BotCommands()
