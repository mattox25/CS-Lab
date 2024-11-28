import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from epic1d import *

# Open, read and save the data from the file 
with open('harmonics.txt', 'r') as file:
    time = []
    firstharmonics = []
    for line in file:
        # Split each line into columns
        columns = line.split()
        # Add the first column to the time list and the second column to the firstharmonics list
        time.append(float(columns[0]))
        firstharmonics.append(float(columns[1]))

time = np.array(time)
firstharmonics = np.array(firstharmonics)

# Note find peaks returns a list [array[aray we want], {}]
peak_indices = find_peaks(firstharmonics)[0]

# Retrieve the peaks and their respective times
peaks = firstharmonics[peak_indices]
peak_times = time[peak_indices]

# find the first peak which is largest than the previous one
noise_peak = 0
for i in range(1, len(peaks)):
    if peaks[i] > peaks[i-1]:
        noise_peak = peaks[i-1]
        break
    else:
        # If the above situation never happens
        noise_peak = peaks[i]

# Calculate the index at which the signal turns into noise
noise_co = np.where(firstharmonics == noise_peak)[0][0] # The index cutoff at which noise begins to dominate
time_co = time[noise_co] # The time cutoff value at which the noise starts to dominate

# Generate arrays of data for signal and noise
signal = firstharmonics[:noise_co]
noise = firstharmonics[noise_co:]
time_signal = time[:noise_co]
time_noise = time[noise_co:]

# Average peaks of noise
noise_peaks_indexes = find_peaks(noise)[0]
noise_peaks = noise[noise_peaks_indexes]
noise_peak_average = np.mean(noise_peaks)
time_noise_peaks = time_noise[noise_peaks_indexes]

# Find signal peaks annd time signal peaks
signal_peaks_indexes = find_peaks(signal)[0]
signal_peaks = signal[find_peaks(signal)[0]]
time_signal_peaks = time_signal[signal_peaks_indexes]

# Spacing between signal peaks. 
# Need to take difference between every other peak, as we have a amplitude graph
odd_time_signal_peaks = time_signal_peaks[::2] # get the even indexed values (i=0, 2, ...)
time_signal_spacing = abs(np.diff(odd_time_signal_peaks))
signal_freq = np.mean(1/time_signal_spacing)

# Frequency error
time_diff = np.diff(time_signal_peaks)
time_std = np.std(time_diff)
freq_error = time_std/np.mean(time_diff)**2
print(f"Angular frequency = {2*np.pi*signal_freq} +/- {2*np.pi*freq_error}") # omega =2*pi*f

# Fitting Functions
params_sig, covariance_sig = curve_fit(exponential, time_signal_peaks, signal_peaks)
sig_fit = exponential(time_signal_peaks, *params_sig)
print(f'Damping rate = {-1*params_sig[1]} +/- {covariance_sig[1][1]}')

# params_noise, covariance_noise = curve_fit(linear, time_noise_peaks, noise_peaks)