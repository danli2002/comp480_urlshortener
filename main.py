from url_shortener import URLShortener

if __name__ == '__main__':
    url_shortener = URLShortener()
    long_url = 'https://verylongurlwebsite.com/very_long_link_to_a_webpage/very_verylong'
    short_url = url_shortener.shorten_url(long_url)
    print(short_url)
    print(url_shortener.get_long_url(short_url))