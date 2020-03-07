import requests
import parsel
from parsel import Selector

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


response = requests.get('https://www.azlyrics.com/a.html')
s = Selector(response.text)
data = get_artists(s)

print(data)

response = requests.get('https://www.azlyrics.com/a/amywinehouse.html')
s = Selector(response.text)
data = get_songs(s)

print(data)

response = requests.get('https://www.azlyrics.com/lyrics/sexpistols/godsavethequeen.html')
s = Selector(response.text)
data = get_song(s)

print(data)