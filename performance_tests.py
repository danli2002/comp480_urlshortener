from url_shortener import BloomURLShortener, NaiveURLShortener
import matplotlib.pyplot as plt
import pandas as pd
import random
import time

class PerformanceTester:
    def __init__(self):
        self.bloom_url_shortener = BloomURLShortener()
        self.naive_shortener = NaiveURLShortener()
        data = pd.read_csv('user-ct-test-collection-01.txt', sep="\t")
        self.urllist = list(data.ClickURL.dropna().unique())
        self.urlstoinsert = random.sample(self.urllist, 10000)
        self.false_negative_list = self.urlstoinsert[:len(self.urlstoinsert) // 2]
        self.false_positive_list = self.urlstoinsert[len(self.urlstoinsert) // 2:]
    
    def get_sample(self, sample_size):
        return random.choices(self.false_negative_list, k=sample_size)

    '''
    Want to test performance of shortening a very large number of urls:
    Bloom Filter implementation vs. Hashing every time

    1. Generate a sample of urls
    2. Time how long it takes to shorten all of them with the bloom filter
    3. Time how long it takes to shorten all of them with hashing

    Also consider the false positive rate of the bloom filter
    '''

    def test_bloom_filter(self, sample):
        query_times = []
        original_pairs = []
        for url in sample:
            shorten_start = time.time()
            original_pairs.append((url, self.bloom_url_shortener.shorten_url(url)))
            shorten_end = time.time()
            shorten_time = shorten_end - shorten_start
            query_times.append(shorten_time)
        return query_times, original_pairs
        # print("Bloom filter shorten time: " + str(shorten_time))
    
    def test_naive(self, sample):
        query_times = []
        original_pairs = []
        for url in sample:
            shorten_start = time.time()
            original_pairs.append((url, self.naive_shortener.shorten_url(url)))
            shorten_end = time.time()
            shorten_time = shorten_end - shorten_start
            query_times.append(shorten_time)
        return query_times, original_pairs
        # print("Naive shorten time: " + str(shorten_time))

    def collision_count(self, original_pairs, method="bloom"):
        count = 0
        if method == "bloom":
            for pair in original_pairs:
                if self.bloom_url_shortener.get_long_url(pair[1]) != pair[0]:
                    print(f"Expected: {pair[0]}, Actual: {self.bloom_url_shortener.get_long_url(pair[1])}")
                    count += 1
        elif method == "naive":
            for pair in original_pairs:
                if self.naive_shortener.get_long_url(pair[1]) != pair[0]:
                    count += 1
        return count

    # def false_negative_count(self, method="bloom"):
    #     count = 0
    #     if method == "bloom":
    #         for url in self.false_negative_list:
    #             if self.bloom_url_shortener.get_long_url(url) is None:
    #                 count += 1
    #     elif method == "naive":
    #         for url in self.false_negative_list:
    #             if self.naive_shortener.get_long_url(url) is None:
    #                 count += 1
    #     return count

    # def false_positive_count(self, method="bloom"):
    #     count = 0
    #     if method == "bloom":
    #         for url in self.false_positive_list:
    #             if self.bloom_url_shortener.get_long_url(url) is not None:
    #                 count += 1
    #     elif method == "naive":
    #         for url in self.false_positive_list:
    #             if self.naive_shortener.get_long_url(url) is not None:
    #                 count += 1
    #     return count

    def plot_query_times(self, bloom_query_times, naive_query_times):
        plt.figure(figsize=(14, 8))
        plt.plot(bloom_query_times, label='Bloom Filter')
        plt.plot(naive_query_times, label='Naive')
        plt.xlabel('URL Index')
        plt.ylabel('Query Time (seconds)')
        plt.title('Query Time Comparison')
        plt.legend()

        plt.savefig('plots/query_time_comparison.png')
        plt.clf()
    
    def plot_average_query_times(self, bloom_query_times, naive_query_times):
        # Calculate cumulative average
        bloom_cumulative_avg = [sum(bloom_query_times[:i+1]) / (i+1) for i in range(len(bloom_query_times))]
        naive_cumulative_avg = [sum(naive_query_times[:i+1]) / (i+1) for i in range(len(naive_query_times))]
        plt.figure(figsize=(14, 8))
        # Plot cumulative average query times for each
        plt.plot(bloom_cumulative_avg, label='Bloom Filter (Cumulative)')
        plt.plot(naive_cumulative_avg, label='Naive (Cumulative)')
        plt.xlabel('URL Index')
        plt.ylabel('Cumulative Average Query Time (seconds)')
        plt.title('Cumulative Average Query Time Comparison')
        plt.legend()

        plt.savefig('plots/cumulative_average_query_time_comparison.png')
        plt.clf()

    def run_test(self):
        sample = self.get_sample(100)
        # bloom_start = time.time()
        bloom_query_times, original_bloom_pairs = self.test_bloom_filter(sample)
        # bloom_end = time.time()
        # bloom_time = bloom_end - bloom_start

        # naive_start = time.time()
        naive_query_times, original_naive_pairs = self.test_naive(sample)
        # naive_end = time.time()
        # naive_time = naive_end - naive_start

        print("Bloom collision count: " + str(self.collision_count(original_bloom_pairs, method="bloom")))
        print("Naive collision count: " + str(self.collision_count(original_naive_pairs, method="naive")))

        self.plot_average_query_times(bloom_query_times, naive_query_times)
        self.plot_query_times(bloom_query_times, naive_query_times)
        print(original_naive_pairs[:10])

        # print("Bloom filter time: " + str(bloom_time))
        # print("Naive time: " + str(naive_time))

        # return bloom_time, naive_time

        

if __name__ == '__main__':
    tester = PerformanceTester()
    tester.run_test()
    