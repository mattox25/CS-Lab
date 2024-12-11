import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from epic1d import *
from main import *

# Save data from harmonics file and time data file
harmonic_data = np.loadtxt('harmonics.txt')
sim_times = np.loadtxt('sim_times.txt') # times for each simulationa as we change cell or number
time_steps = np.loadtxt('step_times.txt') # Still only 1D array as time steps are always the same

# lists of data to save as functions of cell/particle number
noise_levels = []
noise_errors = []
ang_frequencies = []
ang_frequency_errors = []
damping_rates = []
damping_errors = []

# Note find peaks returns a list [array[array we want], {}]
for i, cell in enumerate(cells):
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
            # If the above situation never happens
            noise_peak = peaks[j]

    # Calculate the index at which the signal turns into noise
    noise_co = np.where(firstharmonics == noise_peak)[0][0] # The index cutoff at which noise begins to dominate
    time_co = time_steps[noise_co] # The time cutoff value at which the noise starts to dominate

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
    freq_error = time_std/np.mean(time_diff)**2
    #print(f"Angular frequency = {2*np.pi*signal_freq} +/- {2*np.pi*freq_error}") # omega =2*pi*f

    # Fitting Functions
    params_sig, covariance_sig = curve_fit(exponential, time_signal_peaks, signal_peaks)
    sig_fit = exponential(time_signal_peaks, *params_sig)
    damping = -1*params_sig[1]
    damping_error = covariance_sig[1][1]
    #print(f'Damping rate = {-1*params_sig[1]} +/- {covariance_sig[1][1]}')

    # save data
    noise_levels.append(noise_level)
    noise_errors.append(noise_level_error)
    ang_frequencies.append(2*np.pi*signal_freq)
    ang_frequency_errors.append(2*np.pi*freq_error)
    damping_rates.append(damping)
    damping_errors.append(damping_error)

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
    # plt.savefig(f"firstharmonics{i+1}")
    # plt.close()

# print(f'noise = {noise_levels} \n')
# noise_errors_normalised = [k / len(noise_levels) for k in noise_levels]
# print(f'noise error = {noise_errors_normalised}')

# print(f'angular frequecies = {ang_frequencies} \n')
# print(f'angular frequency errors = {ang_frequency_errors} \n')
# print(f'damping = {damping_rates} \n')
# print(f'damping errors = {damping_errors} \n')
# params_noise, covariance_noise = curve_fit(linear, time_noise_peaks, noise_peaks)