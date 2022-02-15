
import string
import shelve
import dbm  # this import is necessary to handle the custom exception when shelve tries to load a missing file as "read"

#from helpers.database.access_db import db
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# https://stackoverflow.com/questions/62173294/how-can-i-keep-save-the-user-input-in-dictionary


def save_dict(dict_to_be_saved):  # your original function, parameter renamed to not shadow outer scope
    with shelve.open('shelve2.db', 'c') as s:  # Don't think you needed WriteBack, "c" flag used to create dictionary
        s['Dict'] = dict_to_be_saved # just as you had it


async def load_dict():  # loading dictionary
    try:  # file might not exist when we try to open it
        with shelve.open('shelve2.db', 'r') as s:  # the "r" flag used to only read the dictionary
            my_saved_dict = s['Dict']  # load and assign to a variable
            return my_saved_dict  # give the contents of the dictionary back to the program
    except dbm.error:  # if the file is not there to load, this error happens, so we suppress it...
        await message.reply_text("Not Found !!")
        return {} #... and return an empty dictionary instead

'''
ask = input('Do you want to add a new word?(y/n): ') 
if ask == 'y':
    new_word = input('what is the new word?: ')
    word_meaning = input('what does the word mean?: ')
    words[new_word] = word_meaning
    save_dict(words)
elif ask == 'n':
    print(words)  # You can see that the dictionary is preserved between runs
    print("Oh well, nothing else to do here then.")
'''


async def prefix_set(client, message):
    
    words = load_dict()  # first we attempt to load previous dictionary, or make a blank one
    await message.reply_text(
        text="**Send me New File Name Prefix!**"
        reply_to_message_id=message.reply_to_message.message_id,
        parse_mode="markdown"
    )
    try:
        ask_: Message = await bot.listen(message.from_user.id)
        if ask_.text and (ask_.text.startswith("/") is False):
            await ask_.delete(True)
            new_word = message.from_user.id
            word_meaning = ask_.text
            #await SetupPrefix(ask_.text, user_id=cb.from_user.id, editable=cb.message)
            words[new_word] = word_meaning
            save_dict(words)
            ascii_ = ''.join([i if (i in string.digits or i in string.ascii_letters or i == " ") else "" for i in text])
            #await db.set_prefix(user_id, prefix=text)
            await message.reply_text(
                text=f"File Name Prefix Successfully Added!\n\n**Prefix:** `{ascii_}`",
            )

        elif ask_.text and (ask_.text.startswith("/") is True):
            await message.reply_text(
                text="Current Process Cancelled!",
                #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go Back", callback_data="openSettings")]])
            )
    except TimeoutError:
        await message.send_message(
            message.reply_to_message.from_user.id
            text="Sorry Unkil,\n5 Minutes Passed! I can't wait more. Send me Text Again to Set.",
            #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go Back", callback_data="openSettings")]])
        )


