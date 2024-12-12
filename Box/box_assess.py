import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from epic1d import *
from boxL import *
import os

directory = '/Users/jvf522/Documents/CS Lab/Lab1/Box'
if not os.path.exists(directory):
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Save data from harmonics file and time data file

harmonic_data = np.loadtxt('Box/box_harmonics.txt')
sim_times_data = np.loadtxt('Box/box_sim_times.txt') # times for each simulation as we change cell or number
time_steps = np.loadtxt('Box/step_times.txt') # Still only 1D array as time steps are always the same

# lists of data to save as functions of cell/particle number
noise_levels = []
noise_errors = []
ang_frequencies = []
ang_frequency_errors = []
damping_rates = []
damping_errors = []

time_cutoffs = []

# Note find peaks returns a list [array[array we want], {}]
for i, box in enumerate(boxL):
    
    firstharmonics = np.array(harmonic_data[i])
    peak_indices = find_peaks(firstharmonics)[0]

    # Retrieve the peaks and their respective times
    peaks = firstharmonics[peak_indices]
    peak_times = time_steps[peak_indices]

    # find the first peak which is largest than the previous one
    noise_peak = 0
    for j in range(1, len(peaks)):
        if peaks[j] > peaks[j-1]:
            noise_peak = peaks[j-1]
            break
        else:
            # If the above situation never happens, the noise peak is the last peak
            noise_peak = peaks[-1]
    
    # Calculate the index at which the signal turns into noise
    noise_co = np.where(firstharmonics == noise_peak)[0][0] # The index cutoff at which noise begins to dominate
    time_co = time_steps[noise_co] # The time cutoff value at which the noise starts to dominate
    time_cutoffs.append(time_co)
    # Generate arrays of data for signal and noise
    signal = firstharmonics[:noise_co]
    noise = firstharmonics[noise_co:]
    time_signal = time_steps[:noise_co]
    time_noise = time_steps[noise_co:]

    # Average peaks of noise
    noise_peaks_indexes = find_peaks(noise)[0]
    noise_peaks = noise[noise_peaks_indexes]
    noise_peak_average = np.mean(noise_peaks)
    time_noise_peaks = time_noise[noise_peaks_indexes]
    
    # noise quantification, just using the average noise level
    noise_level = noise_peak_average
    noise_level_error = np.std(noise_peaks)

    # Find signal peaks and time signal peaks
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
    if len(time_signal_peaks) == 1:
        freq_error = 0
        # Just take the gradient of the line connecting the first data point and the first (and only) signal peak)
        damping = -1 * (signal_peaks[0] - signal[0])/ (time_signal_peaks[0] - time_signal[0])
        damping_error = 0
    elif len(time_signal_peaks) == 0:
        freq_error = 0
        # Just take the gradient of the line connecting the first data point and the first (and only) signal peak)
        damping = 0
        damping_error = 0
    else:
        freq_error = time_std/np.mean(time_diff)**2

        # Fitting Functions
        params_sig, covariance_sig = curve_fit(exponential, time_signal_peaks, signal_peaks)
        sig_fit = exponential(time_signal_peaks, *params_sig)
        damping = -1*params_sig[1]
        damping_error = covariance_sig[1][1]

    # save data
    noise_levels.append(noise_level)
    noise_errors.append(noise_level_error)
    ang_frequencies.append(2*np.pi*signal_freq)
    ang_frequency_errors.append(2*np.pi*freq_error)
    damping_rates.append(damping)
    damping_errors.append(damping_error)