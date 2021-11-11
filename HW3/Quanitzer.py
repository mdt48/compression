import math
import numpy as np
import utils
from tqdm import tqdm
class UniformQuantizer():
    def __init__(self, level, signal) -> None:
        self.level = level -1
        self.min_val = min(signal)
        self.max_val = max(signal)
        self.delta = (self.max_val-self.min_val) / self.level
        self.signal = np.array(signal)

    def quantize(self):
        return np.floor((self.signal - self.min_val) / self.delta)

    def dequantize(self, quantized_signal):
        return self.min_val + (quantized_signal + 0.5)*self.delta

class SemiUniformQuantizer(UniformQuantizer):
    def __init__(self, level, signal) -> None:
        super().__init__(level, signal)

    def dequantize(self, quantized_signal):
        r = self.gen_r_values(quantized_signal)
        dequantized_signal = np.zeros(len(quantized_signal))

        for i in range(len(quantized_signal)):
            dequantized_signal[i] = r[quantized_signal[i]]
        return dequantized_signal

    def gen_r_values(self, quantized_signal):
        r = {}

        for i in range(len(quantized_signal)):
            level = quantized_signal[i]
            if level in r:
                continue
            values_per_level = []

            for j in range(i, len(quantized_signal)):
                if quantized_signal[j] == level:
                    values_per_level.append(self.signal[j])

            r[level] = sum(values_per_level) / len(values_per_level)
        return r

class MaxLloydQuantizer(SemiUniformQuantizer):
    def __init__(self, level, signal) -> None:
        super().__init__(level, signal)
        self.D = []
        for i in range(level):
            if i == 0:
                self.D.append(self.min_val)
            else:
                self.D.append(self.min_val + i*self.delta)
        self.D = np.array(self.D)
        self.R = []
        for i in range(1, len(self.D)):
            if i == len(self.D)-1:
                self.R.append((self.D[i-1] + self.max_val) / 2)
            else:
                self.R.append((self.D[i-1]+self.D[i]) / 2)
        self.R = np.array(self.R)

    def quantize(self):
        quantized_signal = np.zeros(len(self.signal))

        for i in range(len(quantized_signal)):
            for j in range(1, len(self.D)-1):
                if self.signal[i] < self.D[0]:
                    quantized_signal[i] = 0
                    break
                elif float(self.signal[i]) >= float(self.D[j-1]) and float(self.signal[i]) < float(self.D[j]):
                    quantized_signal[i] = j
                    break
        return quantized_signal

    def dequantize(self, quantized_signal):
        dequantized_signal = np.zeros(len(quantized_signal))

        for i in range(len(quantized_signal)):
            dequantized_signal[i] = self.R[int(quantized_signal[i])]
        return dequantized_signal
    
    def fit(self,tolerance=0.1):
        prev = self.D.copy()
        while 1:
            self.R = self.gen_r_values()
            # self.D = np.array(len(self.R))
            self.D[0] = (self.R[0] + self.min_val) / 2
            for i in range(1, len(self.D)):
                if i == len(self.R):
                    self.D[i] = (self.max_val + self.R[i-1]) / 2
                else:
                    self.D[i] = (self.R[i] + self.R[i-1]) / 2

            mse = utils.MSE(prev, self.D)
            prev = self.D.copy()
            print('mse={}'.format(mse), end='\r')
            if mse < tolerance:
                break

    def gen_r_values(self):
        r = np.zeros(len(self.R))

        data = sorted(self.signal.copy())
        start = 0
        for i in range(len(self.D)-1):
            values = []
            for j in range(start, len(data)):
                if float(data[j]) >= float(self.D[i]) and float(data[j]) < float(self.D[i+1]):
                    values.append(data[j])
                else:
                    break
            if len(values) == 0:
                r[i] = self.D[i]
            else:
                r[i] = sum(values) / len(values)
            start = j+1
        return r