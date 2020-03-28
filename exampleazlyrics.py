import requests
import parsel
from parsel import Selector


def song_info(html: Selector):

    author_css = 'body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div.lyricsh > h2 > b ::text'
    lyrics = 'body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(8) ::text'
    album_css = 'body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div.panel.songlist-panel.noprint > div.songinalbum_title > b ::text'
    author = html.css(author_css).get()
    text = html.css(lyrics).getall()
     album = html.css(album_css).get()
    
    return {'author': author, 'lyrics': ''.join(text)}


response =  requests.get('https://www.azlyrics.com/lyrics/dabrat/funkdafied.html')

data = song_info(Selector(response.text))


print(data)

print(data['lyrics'])