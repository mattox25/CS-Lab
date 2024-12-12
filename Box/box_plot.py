import numpy as np
import matplotlib.pyplot as plt 
from box_assess import *
from boxL import boxL

directory = '/Users/jvf522/Documents/CS Lab/Lab1/Box'
if not os.path.exists(directory):
    os.makedirs(directory)  # Create the directory if it doesn't exist
    
# Sim time vs cell number
plt.scatter(boxL, sim_times_data, )
plt.xlabel("Box Length")
plt.ylabel("Simlation Times")
plt.savefig("Box/sim_times_vs_boxes")
plt.close()

# Angular freqs vs cell number
plt.errorbar(boxL, ang_frequencies, ang_frequency_errors, fmt='.', 
             label='Frequency with errors', ecolor='red', capsize=5)
plt.xlabel("Box Length")
plt.ylabel("Angular Frequency")
plt.savefig("Box/ang_freq_vs_boxes")
plt.close()

# damping rates vs cell number
plt.errorbar(boxL, damping_rates, damping_errors, fmt='.', 
             label='Frequency with errors', ecolor='red', capsize=5)
plt.xlabel("Box Length")
plt.ylabel("Damping Rate")
plt.savefig("Box/damping_rate_vs_boxes")
plt.close()

# noise vs cell number
plt.errorbar(boxL, noise_levels, noise_errors, fmt='.', 
             label='Frequency with errors', ecolor='red', capsize=5)
plt.xlabel("Box Length")
plt.ylabel("Noise Level")
plt.savefig("Box/noise_vs_boxes")
plt.close()

for i in range(0, len(boxL)):
    plt.plot(time_steps, harmonic_data[i], label=f'Box length ={np.round(boxL[i], 2)}')
    # plt.scatter(peak_times, peaks, marker = 'x', color = 'red')
    plt.axvline(time_cutoffs[i], color='g', linestyle='--', label='Noise dominates')
    # plt.axhline(noise_peak_average, color='r', linestyle='--', label='Average Noise')
    # plt.plot(time_signal_peaks, sig_fit, color='c', linestyle='--', label='Exponential fit')
    # plt.plot(time_noise_peaks, noise_peaks, color='m', linestyle='--', label='Exponential fit')
    plt.xlabel("Time [Normalised]")
    plt.ylabel("First harmonic amplitude [Normalised]")
    plt.yscale('log')
    plt.legend()
    plt.savefig(f"Box/box_firstharmonics{i+1}")
    plt.close()


