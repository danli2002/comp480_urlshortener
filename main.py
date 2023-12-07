from url_shortener import URLShortener
import pandas as pd
import random


if __name__ == '__main__':
    url_shortener = URLShortener()
    # long_url = 'https://verylongurlwebsite.com/very_long_link_to_a_webpage/very_verylong'
    # short_url = url_shortener.shorten_url(long_url)
    # print(short_url)
    # print(url_shortener.get_long_url(short_url))
    data = pd.read_csv('user-ct-test-collection-01.txt', sep="\t")
    urllist = data.ClickURL.dropna().unique()
    url_sample = random.sample(list(urllist), 20)
    for url in url_sample:
        short_url = url_shortener.shorten_url(url)
        print(short_url)
        print(url_shortener.get_long_url(short_url))