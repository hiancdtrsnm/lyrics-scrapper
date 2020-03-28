import requests
from parsel import Selector
import enlighten
import json
import os
import logging
import time
import typer

app = typer.Typer()


logging.basicConfig(level=logging.DEBUG)
manager = enlighten.get_manager()


FOLDER = 'songs'

os.makedirs(FOLDER,exist_ok=True)

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
session = requests.Session()

session.headers.update({'User-Agent': user_agent})

BASE_URL = 'https://www.azlyrics.com/'

def parse_song(html: Selector):

    lyrics = ''.join(html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(8)::text').getall()).strip()
    title = html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > b ::text').get()
    band = html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div.lyricsh > h2 > b ::text').get()[:-len(' lyrics')]
    written_by = html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(17) > small ::text').get()
    album = html.css('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div.panel.songlist-panel.noprint > div.songinalbum_title > b ::text')

    if written_by:
        written_by = [author.strip() for author in written_by[len('Writer(s): '):].split(',') if author]

    return {
        'lyrics': lyrics,
        'title': title,
        'band': band,
        'written_by': written_by,
        'album': album
    }

def parse_songs(html: Selector):

    songs = [BASE_URL + link[3:] for link in html.css('#listAlbum a ::attr(href)').getall()]

    return songs

def parse_artists(html: Selector):

    artists = [BASE_URL + link for link in html.css('body > div.container.main-page > div a ::attr(href)').getall()]

    return artists

@app.command(help='Get a song info the link looks like this: "https://www.azlyrics.com/lyrics/viceganda/boompanes.html"')
def get_song(url: str)->dict:
    response = session.get(url)
    s_song = Selector(response.text)
    return parse_song(s_song)

def _get_artist(url: str):
    response = session.get(url)
    s_artist = Selector(response.text)
    songs = parse_songs(s_artist)

    sbar = manager.counter(total=len(songs), desc=f'Songs of ({url})', unit='songs')

    for song in songs:
        print(song)
        yield get_song(song)
        sbar.update()
        time.sleep(3)

    sbar.close()


def _get_page(url: str):
    response = session.get(url)
    s_page = Selector(response.text)
    artists = parse_artists(s_page)

    abar = manager.counter(total=len(artists), desc=f'Page({url})', unit='artists')

    for artist in artists:
        for song in _get_artist(artist):
            yield song

        abar.update()

    abar.close()

@app.command(help='Get the info of all site')
def get_all():

    letter_pages = ['https://www.azlyrics.com/a.html', 'https://www.azlyrics.com/b.html']


    pbar = manager.counter(total=len(letter_pages), desc='pages', unit='pages')


    for page in letter_pages:
        for song in _get_page(page):
            json.dump(song, open(os.path.join(FOLDER, f"({song['title']})-({song['band']}).json"), 'w'), indent=2)
            print(f"({song['title']})-({song['band']})")
        pbar.update()
    pbar.close()


@app.command(help='Get all song of an artist, link look like this: "https://www.azlyrics.com/v/viceganda.html"')
def get_artist(url:str):
    return list(_get_artist(url))

@app.command(help='Get all song of artists within a page, link look like this: "https://www.azlyrics.com/c.html"')
def get_page(url:str):
    return list(_get_page(url))


if __name__ == "__main__":
    app()

# response = requests.get('https://www.azlyrics.com/a.html')
# s = Selector(response.text)
# data = parse_artists(s)

# print(data)

# response = requests.get('https://www.azlyrics.com/a/amywinehouse.html')
# s = Selector(response.text)
# data = parse_songs(s)

# print(data)

# response = requests.get('https://www.azlyrics.com/lyrics/sexpistols/godsavethequeen.html')
# s = Selector(response.text)
# data = parse_song(s)

# print(data)