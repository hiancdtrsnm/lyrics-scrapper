import requests
from parsel import Selector
import enlighten
import json
import os
import logging
import time


logging.basicConfig(level=logging.DEBUG)

FOLDER = 'songs'

os.makedirs(FOLDER,exist_ok=True)

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
session = requests.Session()

session.headers.update({'User-Agent': user_agent})

BASE_URL = 'https://www.azlyrics.com/'

def get_song(html: Selector):

    lyrics = ''.join(html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(8)::text').getall()).strip()
    title = html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > b ::text').get()
    band = html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div.lyricsh > h2 > b ::text').get()[:-len(' lyrics')]
    written_by = [author.strip() for author in html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(17) > small ::text').get()[len('Writer(s): '):].split(',')]

    return {
        'lyrics': lyrics,
        'title': title,
        'band': band,
        'written_by': written_by,
        'album': None
    }

def get_songs(html: Selector):

    songs = [BASE_URL + link[3:] for link in html.css('#listAlbum a ::attr(href)').getall()]

    return songs

def get_artists(html: Selector):

    artists = [BASE_URL + link for link in html.css('body > div.container.main-page > div a ::attr(href)').getall()]

    return artists


manager = enlighten.get_manager()


letter_pages = ['https://www.azlyrics.com/a.html', 'https://www.azlyrics.com/b.html']
pbar = manager.counter(total=len(letter_pages), desc='pages', unit='pages')

for page in letter_pages:
    pbar.update()
    response = session.get(page)
    s_page = Selector(response.text)
    artists = get_artists(s_page)
    abar = manager.counter(total=len(artists), desc=f'Page({page})', unit='artists')

    for artist in artists:
        abar.update()
        response = session.get(artist)
        s_artist = Selector(response.text)
        songs = get_songs(s_artist)
        sbar = manager.counter(total=len(songs), desc=f'Songs of ({artist})', unit='songs')

        for song in songs:
            sbar.update()
            response = session.get(song)
            time.sleep(3)
            s_song = Selector(response.text)
            song = get_song(s_song)
            json.dump(song, open(os.path.join(FOLDER, f"({song['title']})-({song['band']}).json"), 'w'), indent=2)
            print(f"({song['title']})-({song['band']})")

        sbar.close()
    abar.close()


# response = requests.get('https://www.azlyrics.com/a.html')
# s = Selector(response.text)
# data = get_artists(s)

# print(data)

# response = requests.get('https://www.azlyrics.com/a/amywinehouse.html')
# s = Selector(response.text)
# data = get_songs(s)

# print(data)

# response = requests.get('https://www.azlyrics.com/lyrics/sexpistols/godsavethequeen.html')
# s = Selector(response.text)
# data = get_song(s)

# print(data)