from BloomFilter import BloomFilter

class URLShortener:
    def __init__(self):
        self.urls = {}  # Dictionary to store short URL -> long URL mapping
        self.bloom_filter = BloomFilter(1000000, 0.01)  # Bloom filter to check if a URL is already stored

    def shorten_url(self, long_url):
        # Check if the URL is already stored
        if self.bloom_filter.lookup(long_url):
            # If it is, return the existing short URL
            return self.urls[long_url]

        # If not, generate a new short URL
        short_url = self.generate_short_url(long_url)

        # Store the short URL -> long URL mapping
        self.urls[short_url] = long_url

        # Add the long URL to the Bloom filter
        self.bloom_filter.insert(long_url)

        return short_url

    def generate_short_url(self, long_url):
        # This is a very basic example of generating a short URL.
        # In a real-world application, you would want to use a more robust method.
        return 'http://short.url/' + str(hash(long_url))

    def get_long_url(self, short_url):
        # Return the long URL corresponding to the given short URL
        return self.urls.get(short_url, None)