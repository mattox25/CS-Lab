import numpy as np
import matplotlib.pyplot as plt 
from noise_assess import *
from main import cells

# Make a semilog plot to see exponential damping

# plt.plot(time_steps, firstharmonics)
# plt.scatter(peak_times, peaks, marker = 'x', color = 'red')
# plt.axvline(time_co, color='g', linestyle='--', label='Noise dominates')
# plt.axhline(noise_peak_average, color='r', linestyle='--', label='Average Noise')
# plt.plot(time_signal_peaks, sig_fit, color='c', linestyle='--', label='Exponential fit')
# # plt.plot(time_noise_peaks, noise_peaks, color='m', linestyle='--', label='Exponential fit')
# plt.xlabel("Time [Normalised]")
# plt.ylabel("First harmonic amplitude [Normalised]")
# plt.yscale('log')
# plt.legend()
# plt.savefig("firstharmonics")
# plt.close()

# Sim time vs cell number
plt.scatter(cells, sim_times, marker='x')
plt.xlabel("Number of Cells")
plt.ylabel("Simlation Times")
plt.savefig("sim_times_vs_cells")
plt.close()

# Angular freqs vs cell number
plt.errorbar(cells, ang_frequencies, ang_frequency_errors, fmt='x', 
             label='Frequency with errors', ecolor='red', capsize=5)
plt.xlabel("Number of Cells")
plt.ylabel("Angular Frequency")
plt.savefig("ang_freq_vs_cells")
plt.close()

# damping rates vs cell number
plt.errorbar(cells, damping_rates, damping_errors, fmt='x', 
             label='Frequency with errors', ecolor='red', capsize=5)
plt.xlabel("Number of Cells")
plt.ylabel("Damping Rate")
plt.savefig("damping_rate_vs_cells")
plt.close()

plt.plot(cells, damping_rates)
plt.show()

# noise vs cell number
plt.errorbar(cells, noise_levels, noise_errors, fmt='x', 
             label='Frequency with errors', ecolor='red', capsize=5)
plt.xlabel("Number of Cells")
plt.ylabel("Noise Level")
plt.savefig("noise_vs_cells")
plt.close()

