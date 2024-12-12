
from epic1d import *
import time
import numpy as np
import sys

cells = [20]
particles = [10000]
boxL = 100
npart = len(particles)
ncells = len(cells)                                    
ntimes = 200 

if ncells != npart:
    print(f'cell and particle number must be the same (ncell = {ncells}, npart = {npart})')
    sys.exit()

if __name__ == "__main__":                  
    
    # Data lists of interest (simulation time, noise level, frequency and damping rate)
    # noise level, frequency and damping rateis calculated in noise_assess.py
    harmonic_data = np.zeros((ncells, npart, ntimes))     
    time_step_data = linspace(0.,80, ntimes)
    sim_time_data = np.zeros((ncells, npart)) # Time data for each run at different cell number
    test_time_start = time.time()

    for i, cell in enumerate(cells):
        sim_time_lst = []
        for j, part in enumerate(particles):
            start_time = time.time()
            if True:
                # 2-stream instability
                L = boxL
                pos, vel = twostream(part, boxL, 3.) # Might require more npart than Landau!
            else:
                # Landau damping
                L = 4. * pi
                pos, vel = landau(box, L) # Randomises the position and velocity
            
            # Create some output classes
            # Summary stores an array of the first-harmonic amplitude
            p = Plot(pos, vel, cell, boxL) # This displays an animated figure - Slow!
            s = Summary()                   # Calculates, stores and prints summary info

            diagnostics_to_run = [p, s]        # Remove p to get much faster code!
            
            # Run the simulation
            pos, vel = run(pos, vel, boxL, cell, 
                        out = diagnostics_to_run,               # These are called each output step
                        output_times=time_step_data)  # The times to output
            
            harmonic_data[i][j] += s.firstharmonic
            
            end_time = time.time()
            sim_time_lst.append(end_time-start_time)

        sim_time_data[i] += np.array(sim_time_lst)
        print(f'Simulation {i+1} (cells = {cell}) finished')

        # The time steps are the same for each value of cells, so just keep times to one list!
        # time_step_data += s.t
        # print(f'Total time: {sum(sim_time_data)}')
        directory = '/Users/jvf522/Documents/CS Lab/Lab1'
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory if it doesn't exist

        # Now save the file
        np.save(os.path.join(directory, 'harmonics.txt'), harmonic_data, fmt='%f')
        savetxt(os.path.join(directory, 'step_times.txt'), time_step_data, fmt='%f')
        savetxt(os.path.join(directory, 'sim_times.txt'), sim_time_data, fmt='%f')

    test_time_end = time.time()
    print(f'run time = {test_time_end - test_time_start}')