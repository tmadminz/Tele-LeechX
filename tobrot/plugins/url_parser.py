# 5MysterySD Coding . . .


from tobrot import LOGGER
from tobrot.helper_funcs.direct_link_generator import direct_link_generator
from tobrot.helper_funcs.exceptions import DirectDownloadLinkException

async def url_parser(client, message):
   
    op = await message.reply_text(
        text="`Fetching Data . . .`",
        quote=True,
    )
    user_id = message.from_user.id 
    u_men = message.from_user.mention
    url_parse = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(url_parse) > 1:
        url = url_parse[1]
    elif reply_to is not None:
        url = reply_to.text
    else:
        url = None
    if url is not None:
        oo = await op.edit_text(
            text=f"⚡️__URL Parsing Initiated__⚡️\n\n👤 **User** : {u_men} \n🆔 **User ID** : `{user_id}` \n🔗 **Link** : `{url}`\n\n`Fetching Data . . .`",
            disable_web_page_preview=True,
        )
        trigger, bypassed_url = await bypass_link(url)
        if trigger is True:
            ok = await oo.edit_text(
                text="⛔ __Url Parsing Stopped__ ⛔ \n\n `Check your Link First, if I can Parse it or Not !!` \n\n#UnParseable",
                disable_web_page_preview=True,
            )
            return 
        else:
            tell = await oo.edit_text(
                 text=f"⚡️__URL Parsing Initiated__⚡️\n\n👤 **User** : {u_men} \n🆔 **User ID** : `{user_id}` \n🔗 **Link** : `{url}`\n\n📇 **Bypass Info** 📇 : \n\n {bypassed_url}\n\n#Parsed",
                 disable_web_page_preview=True,
            )
    else:
        oo = await op.edit_text(
            text="`Send Link along with /parser`",
        )
        return


async def bypass_link(text_url: str):
    
    if "zippyshare.com" in text_url \
        or "osdn.net" in text_url \
        or "mediafire.com" in text_url \
        or "uptobox.com" in text_url \
        or "cloud.mail.ru" in text_url \
        or "github.com" in text_url \
        or "yadi.sk" in text_url  \
        or "hxfile.co" in text_url  \
        or "anonfiles.com" in text_url  \
        or "letsupload.io" in text_url  \
        or "fembed.net" in text_url  \
        or "fembed.com" in text_url  \
        or "femax20.com" in text_url  \
        or "fcdn.stream" in text_url  \
        or "feurl.com" in text_url  \
        or "naniplay.nanime.in" in text_url  \
        or "naniplay.nanime.biz" in text_url  \
        or "naniplay.com" in text_url  \
        or "layarkacaxxi.icu" in text_url  \
        or "sbembed.com" in text_url  \
        or "streamsb.net" in text_url  \
        or "sbplay.org" in text_url  \
        or "1drv.ms" in text_url  \
        or "pixeldrain.com" in text_url  \
        or "antfiles.com" in text_url  \
        or "streamtape.com" in text_url  \
        or "bayfiles.com" in text_url  \
        or "1fichier.com" in text_url  \
        or "solidfiles.com" in text_url  \
        or "krakenfiles.com" in text_url  \
        or "new.gdtot.nl" in text_url  \
        or "gplinks.co" in text_url  \
        or "appdrive.in" in text_url  \
        or "driveapp.in" in text_url  \
        or "linkvertise.com" in text_url  \
        or "droplink.co" in text_url  \
        or "gofile.io" in text_url  \
        or "ouo.io" in text_url  \
        or "ouo.press" in text_url  \
        or "upindia.mobi" in text_url  \
        or "uploadfile.cc" in text_url  \
        or "hubdrive.in" in text_url  \
        or "adf.ly" in text_url  \
        or "https://sourceforge.net" in text_url  \
        or "https://master.dl.sourceforge.net" in text_url  \
        or "androiddatahost.com" in text_url  \
        or "androidfilehost.com" in text_url  \
        or "sfile.mobi" in text_url  \
        or "wetransfer.com" in text_url  \
        or "we.tl" in text_url  \
        or "racaty.net" in text_url:
            try:
                url_string = direct_link_generator(text_url)
                return False, url_string
            except DirectDownloadLinkException as e:
                LOGGER.info(f'{text_url}: {e}')
    else:
        return True, None


