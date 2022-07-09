#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import re
from imdb import IMDb

from tobrot import app, MAX_LIST_ELM, DEF_IMDB_TEMPLATE,  LOGGER
from tobrot.plugins.custom_utils import *
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery 
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
# Callback Data

imdb = IMDb() 

async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('<code>Searching IMDB ...</code>', parse_mode=enums.ParseMode.HTML)
        r, title = message.text.split(None, 1)
        user_id_ = message.from_user.id
        if title.lower().startswith("tt"):
            movieid = title.replace("tt", "")
            movie = imdb.get_movie(movieid)
            if not movie:
                await k.delete()
                return await message.reply("`No Results Found`")
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{movie.get('title')} ({movie.get('year')}) - tt{movieid}",
                        callback_data=f"imdb#{movieid}#{user_id_}",
                    )
                ]
            ]
            await k.edit('**Here What I found on IMDb.com**', reply_markup=InlineKeyboardMarkup(btn))
            return
        else:
            movies = await get_poster(title, bulk=True)
            LOGGER.info(movies)
            if not movies:
                await k.delete()
                return await message.reply("`No results Found`")
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{movie.get('title')} ({movie.get('year')})",
                        callback_data=f"imdb#{movie.movieID}#{user_id_}",
                    )
                ]
                for movie in movies
            ]
            await k.edit('**Here What I found on IMDb.com**', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('`Send Movie / Series Name along with /imdb`')


async def get_poster(query, bulk=False, id=False, file=None):
    if not id:
        # https://t.me/GetTGLink/4183
        query = (query.strip()).lower()
        title = query
        year = re.findall(r'[1-2]\d{3}$', query, re.IGNORECASE)
        if year:
            year = list_to_str(year[:1])
            title = (query.replace(year, "")).strip()
        elif file is not None:
            year = re.findall(r'[1-2]\d{3}', file, re.IGNORECASE)
            if year:
                year = list_to_str(year[:1]) 
        else:
            year = None
        movieid = imdb.search_movie(title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered=list(filter(lambda k: str(k.get('year')) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid=list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = query
    movie = imdb.get_movie(movieid)
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    LONG_IMDB_DESCRIPTION = False
    plot = ""
    if not LONG_IMDB_DESCRIPTION:
        plot = movie.get('plot')
        if plot and len(plot) > 0:
            plot = plot[0]
    else:
        plot = movie.get('plot outline')
    if plot and len(plot) > 800:
        plot = plot[0:800] + "..."

    return {
        'title': movie.get('title'),
        'votes': movie.get('votes'),
        "aka": list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        "box_office": movie.get('box office'),
        'localized_title': movie.get('localized title'),
        'kind': movie.get("kind"),
        "imdb_id": f"tt{movie.get('imdbID')}",
        "cast": list_to_str(movie.get("cast")),
        "runtime": list_to_str(movie.get("runtimes")),
        "countries": list_to_hash(movie.get("countries")),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_hash(movie.get("languages")),
        "director": list_to_str(movie.get("director")),
        "writer":list_to_str(movie.get("writer")),
        "producer":list_to_str(movie.get("producer")),
        "composer":list_to_str(movie.get("composer")) ,
        "cinematographer":list_to_str(movie.get("cinematographer")),
        "music_team": list_to_str(movie.get("music department")),
        "distributors": list_to_str(movie.get("distributors")),
        'release_date': date,
        'year': movie.get('year'),
        'genres': list_to_hash(movie.get("genres")),
        'poster': movie.get('full-size cover url'),
        'plot': plot,
        'rating': str(movie.get("rating")),
        'url':f'https://www.imdb.com/title/tt{movieid}'
    }

def list_to_str(k):
    if not k:
        return ""
    elif len(k) == 1:
        return str(k[0])
    elif MAX_LIST_ELM:
        k = k[:int(MAX_LIST_ELM)]
        return ' '.join(f'{elem},' for elem in k)[:-1]
    else:
        return ' '.join(f'{elem},' for elem in k)[:-1]

def list_to_hash(k):
    listing = ""
    if not k:
        return ""
    elif len(k) == 1:
        return str("#"+k[0].replace(" ", "_"))
    elif MAX_LIST_ELM:
        k = k[:int(MAX_LIST_ELM)]
        for elem in k:
            elem = elem.replace(" ", "_")
            listing += f'#{elem}, '
        return listing[:-1]
    else:
        for elem in k:
            elem = elem.replace(" ", "_")
            listing += f'#{elem}, '
        return listing[:-1]

@app.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot, quer_y: CallbackQuery):
    i, movie, from_user = quer_y.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"⚡ 𝘊𝘭𝘪𝘤𝘬 𝘏𝘦𝘳𝘦 ⚡",
                    url=imdb['url'],
                )
            ]
        ]
    message = quer_y.message.reply_to_message or quer_y.message
    template = IMDB_TEMPLATE.get(from_user, "")
    LOGGER.info(IMDB_TEMPLATE)
    LOGGER.info(from_user)
    LOGGER.info(template)
    if template == "":
        template = DEF_IMDB_TEMPLATE
    if imdb and template != "":
        caption = template.format(
            query = imdb['title'],
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        caption = "No Results"
    if imdb.get('poster'):
        try:
            await quer_y.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await quer_y.message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            LOGGER.exception(e)
            await quer_y.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        await quer_y.message.delete()
    else:
        await quer_y.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
    await quer_y.answer()


