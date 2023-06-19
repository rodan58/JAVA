import matplotlib.pyplot as plt
import numpy as np


class Data:
    def __init__(self, file):
        with open(file, 'r') as f:
            self.arr = list(map(int, f.read().split()))

    def calc_sma(self, sma_period):
        j = next(i for i, x in enumerate(self.arr) if x is not None)
        our_range = range(len(self.arr))[j + sma_period - 1:]
        empty_list = [None] * (j + sma_period - 1)
        sub_result = [sum(self.arr[i - sma_period + 1:i + 1]) / len(self.arr[i - sma_period + 1:i + 1]) for i in our_range]

        return empty_list + sub_result

    def med_filter(self, window_size):
        assert window_size % 2 == 1
        k2 = (window_size - 1) // 2
        y = np.zeros((len(self.arr), window_size), dtype=int)
        y[:, k2] = self.arr
        for i in range(k2):
            j = k2 - i
            y[j:, i] = self.arr[:-j]
            y[:j, i] = self.arr[0]
            y[:-j, -(i + 1)] = self.arr[j:]
            y[-j:, -(i + 1)] = self.arr[-1]
        return np.median(y, axis=1)


all_here = Data('data2.txt')
plt.plot(all_here.arr)
plt.plot(all_here.med_filter(3))
plt.plot(all_here.med_filter(5))
plt.title('Median Filter')
plt.legend(['Data', 'Period: 3', 'Period: 5'])
plt.show()

sma = all_here.calc_sma(2)
sma1 = all_here.calc_sma(5)
plt.title('SMA')
plt.plot(all_here.arr)
plt.plot(sma)
plt.plot(sma1)
plt.legend(['Data', 'Period: 2', 'Period: 5'])
plt.show()
