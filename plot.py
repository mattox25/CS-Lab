import numpy as np
import matplotlib.pyplot as plt 
from noise_assess import *

# Make a semilog plot to see exponential damping
plt.plot(time, firstharmonics)
plt.scatter(peak_times, peaks, marker = 'x', color = 'red')
plt.axvline(time_co, color='g', linestyle='--', label='Noise dominates')
plt.axhline(noise_peak_average, color='r', linestyle='--', label='Average Noise')
plt.plot(time_signal_peaks, sig_fit, color='c', linestyle='--', label='Exponential fit')
plt.xlabel("Time [Normalised]")
plt.ylabel("First harmonic amplitude [Normalised]")
plt.yscale('log')
plt.legend()
plt.savefig("firstharmonics")
plt.close()

# plt.plot(time_signal, signal)
# plt.xlabel("Time [Normalised]")
# plt.ylabel("First harmonic amplitude [Normalised]")
# plt.yscale('log')
# plt.savefig("firstharmonics_signal")
# plt.close()
