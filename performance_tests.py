from url_shortener import BloomURLShortener, NaiveURLShortener
import matplotlib.pyplot as plt
import pandas as pd
import random
import time
import sys
import math 

class PerformanceTester:
    def __init__(self, n, desired_fp):
        self.n = n
        self.desired_fp = desired_fp        
        self.naive_shortener = NaiveURLShortener()
        data = pd.read_csv('user-ct-test-collection-01.txt', sep="\t")
        self.urllist = list(data.ClickURL.dropna().unique())
        self.bloom_url_shortener = BloomURLShortener(n=n, fp=desired_fp)
        ninety_split = math.floor(len(self.urllist) * 0.9)
        self.urlstoinsert = self.urllist[:ninety_split]
        
        self.urlstotest = self.urllist[ninety_split:]
        self.false_negative_list = self.urlstotest[:len(self.urlstotest) // 2]
        self.false_positive_list = self.urlstotest[len(self.urlstotest) // 2:]
    
    def get_sample(self, sample_size):
        return random.choices(self.false_negative_list, k=sample_size)
    '''
    Initializing our shorteners
    '''
    def insert(self):
        bloom_start = time.time()
        for url in self.urlstoinsert:      
            self.bloom_url_shortener.shorten_url(url)
        bloom_end = time.time()

        naive_start = time.time()
        for url in self.urlstoinsert:
            self.naive_shortener.shorten_url(url)
        naive_end = time.time()

        bloom_total = bloom_end-bloom_start
        naive_total = naive_end-naive_start
        print("Insertion times for n = ", self.n, " and fp = ", self.desired_fp, ":")
        print("Bloom took :", bloom_total)
        print("Naive took :", naive_total)
    '''
    Want to assert that bloom filter takes less space
    '''
    def test_size(self):
        print(f'Memory footprint for n = {self.n} and fp = {self.desired_fp}:')
        print("Bloom size in memory:", sys.getsizeof(self.bloom_url_shortener.bloom_filter))
        print("Naive size in memory:", sys.getsizeof(self.naive_shortener.seen_urls))
    
    def test_query(self):
        print(f"Query time test for Bloom filter of n = {self.n} and fp = {self.desired_fp}:")
        # stuff we know is in the set
        samples = random.choices(self.urlstoinsert, k=1000)
        query_times_bloom = []
        start_bloom = time.time()
        for sample in samples:
            shorten_start = time.time()
            # assert(self.bloom_url_shortener.bloom_filter.test(sample))
            shorten_end = time.time()
            shorten_time = shorten_end - shorten_start
            query_times_bloom.append(shorten_time)
        end_bloom = time.time()

        query_times_naive = []
        start_naive = time.time()
        for sample in samples:
            shorten_start = time.time()
            # assert(sample in self.naive_shortener.urls.values())
            shorten_end = time.time()
            shorten_time = shorten_end - shorten_start
            query_times_naive.append(shorten_time)
        end_naive = time.time()
        naive_time = end_naive-start_naive
        bloom_time = end_bloom-start_bloom
        print("Naive took: ", naive_time)
        print("Bloom took: ", bloom_time)
        speedup = naive_time/bloom_time
        print("Bloom was " + str(speedup) + " times faster")
        return query_times_bloom, query_times_naive

    def generate_query_time_plots(self, bloom_query_times, naive_query_times):
        plt.figure(figsize=(14, 8))
        # log_bloom = [math.log(x) for x in bloom_query_times]
        # log_naive = [math.log(x) for x in naive_query_times]
        plt.plot(bloom_query_times, label='Bloom Filter')
        plt.plot(naive_query_times, label='Naive')
        plt.xlabel('URL Index')
        plt.ylabel('Query Time (seconds)')
        plt.title('Query Time Comparison')
        plt.legend()

        plt.savefig('plots/query_time_comparison.png')
        plt.show()
        plt.clf()

    def generate_average_query_time_plots(self, bloom_query_times, naive_query_times):
        # Calculate cumulative average
        bloom_cumulative_avg = [sum(bloom_query_times[:i+1]) / (i+1) for i in range(len(bloom_query_times))]
        naive_cumulative_avg = [sum(naive_query_times[:i+1]) / (i+1) for i in range(len(naive_query_times))]
        plt.figure(figsize=(14, 8))
        # Plot cumulative average query times for each
        plt.plot(bloom_cumulative_avg, label='Bloom Filter (Cumulative)')
        plt.plot(naive_cumulative_avg, label='Naive (Cumulative)')
        plt.xlabel('URL Index')
        plt.ylabel('Cumulative Average Query Times  (seconds)')
        plt.title(f'Cumulative Average Query Time Comparison for Naive vs. Bloom Filter w/ n={self.n}, fp={self.desired_fp}')
        plt.legend()
        plt.savefig(f'plots/cumulative_avg_query_comparison_n{self.n}_fp{self.desired_fp}.png')
        plt.clf()
    
    def generate_fp_plots(self, fp_rates):
        plt.figure(figsize=(14, 8))
        plt.plot(fp_rates, label='Bloom Filter')
        plt.xlabel('URL Index')
        plt.ylabel('False Positive Rate')
        plt.title(f'False Positive Rate for Bloom Filter w/ n={self.n}, fp={self.desired_fp}')
        plt.legend()

        plt.savefig(f'plots/fp_rate_comparison_n{self.n}_fp{self.desired_fp}.png')
        plt.clf()

    def test_fp(self):
        fp_rates = []
        fp = 0
        print("Length of test set", len(self.urlstotest))
        for total, false in enumerate(self.urlstotest):
            if self.bloom_url_shortener.bloom_filter.test(false) == True:
                fp += 1
            fp_rates.append(fp/(total + 1))
        fp_obs = fp / len(self.urlstotest)
        print("Observed fp rate = ", fp_obs)
        print("Num fp = ", fp)
        return fp_obs, fp_rates
        
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

    # def plot_query_times(self, bloom_query_times, naive_query_times):
    #     plt.figure(figsize=(14, 8))
    #     # log_bloom = [math.log(x) for x in bloom_query_times]
    #     # log_naive = [math.log(x) for x in naive_query_times]
    #     plt.plot(naive_query_times, label='Bloom Filter')
    #     plt.plot(naive_query_times, label='Naive')
    #     plt.xlabel('URL Index')
    #     plt.ylabel('Query Time (seconds)')
    #     plt.title('Query Time Comparison')
    #     plt.legend()

    #     plt.savefig('plots/query_time_comparison.png')
    #     plt.show()
    #     plt.clf()
    
    # def plot_average_query_times(self, bloom_query_times, naive_query_times):
    #     # Calculate cumulative average
    #     bloom_cumulative_avg = [sum(bloom_query_times[:i+1]) / (i+1) for i in range(len(bloom_query_times))]
    #     naive_cumulative_avg = [sum(naive_query_times[:i+1]) / (i+1) for i in range(len(naive_query_times))]
    #     plt.figure(figsize=(14, 8))
    #     # Plot cumulative average query times for each
    #     plt.plot(bloom_cumulative_avg, label='Bloom Filter (Cumulative)')
    #     plt.plot(naive_cumulative_avg, label='Naive (Cumulative)')
    #     plt.xlabel('URL Index')
    #     plt.ylabel('Cumulative Average Query Time (seconds)')
    #     plt.title('Cumulative Average Query Time Comparison')
    #     plt.legend()

    #     plt.savefig('plots/cumulative_average_query_time_comparison.png')
    #     plt.clf()

    def run_test(self):
        self.insert()
        self.test_size()
        query_times_bloom, query_times_naive = self.test_query()
        fp_obs, fp_rates = self.test_fp()
        self.generate_fp_plots(fp_rates)
        # self.generate_query_time_plots(query_times_bloom, query_times_naive)
        self.generate_average_query_time_plots(query_times_bloom, query_times_naive)

if __name__ == '__main__':
    # tester = PerformanceTester()
    n_vals = [380000, 500000, 1000000]
    fp_rates = [0.001, 0.01]
    for n in n_vals:
        for fp in fp_rates:
            tester = PerformanceTester(n, fp)
            tester.run_test()
            tester.insert()
            tester.test_size()
            tester.test_query()
            tester.test_fp()
    