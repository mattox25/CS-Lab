from epic1d import *
import time
import numpy as np
import sys

cells = 20
particles = 10000
boxL = arange(1, 15, 0.5) * pi
nbox = len(boxL)                              
ntimes = 100 

if __name__ == "__main__":                  
    
    # Data lists of interest (simulation time, noise level, frequency and damping rate)
    # noise level, frequency and damping rateis calculated in noise_assess.py

    box_harmonic_data = np.zeros((nbox, ntimes))
    time_step_data = linspace(0., 20, ntimes)
    box_sim_time_data = np.zeros(nbox) # Time data for each run at different cell number
    for i, box in enumerate(boxL):
        start_time = time.time()
        if False:
            # 2-stream instability
            L = 100
            ncells = 20
            pos, vel = twostream(npart, L, 3.) # Might require more npart than Landau!
        else:
            # Landau damping
            pos, vel = landau(particles, L=box) # Randomises the position and velocity
        
        # Create some output classes
        # Summary stores an array of the first-harmonic amplitude
        s = Summary()                   # Calculates, stores and prints summary info

        diagnostics_to_run = [s]        # Remove p to get much faster code!
        
        # Run the simulation
        pos, vel = run(pos, vel, box, cells, 
                    out = diagnostics_to_run,               # These are called each output step
                    output_times=time_step_data)  # The times to output
        
        box_harmonic_data[i] += s.firstharmonic
        
        end_time = time.time()

        box_sim_time_data[i] += end_time - start_time
        print(f'Simulation {i+1} (box = {box}) finished')

    # The time steps are the same for each value of cells, so just keep times to one list!
    # time_step_data += s.t
    # print(f'Total time: {sum(sim_time_data)}')
    directory = '/Users/jvf522/Documents/CS Lab/Lab1/Box'
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist

    # Now save the file
    savetxt(os.path.join(directory, 'box_harmonics.txt'), box_harmonic_data, fmt='%f')
    savetxt(os.path.join(directory, 'box_sim_times.txt'), box_sim_time_data, fmt='%f')