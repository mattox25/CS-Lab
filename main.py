
from epic1d import *
import time
import numpy as np

cells = arange(20, 150, 10)
npart = 5000                                           # Keep fixed for now
ntimes = 100
ncells = len(cells)  

if __name__ == "__main__":                  
    
    # Data lists of interest (simulation time, noise level, frequency and damping rate)
    # noise level, frequency and damping rateis calculated in noise_assess.py
    harmonic_data = np.zeros((ncells, ntimes))     
    time_step_data = np.zeros(ntimes)
    sim_time_data = np.zeros(ncells) # Time data for each run at different cell number

    for i, cell in enumerate(cells):
        start_time = time.time()
        if False:
            # 2-stream instability
            L = 100
            ncells = 20
            pos, vel = twostream(npart, L, 3.) # Might require more npart than Landau!
        else:
            # Landau damping
            L = 4. * pi
            pos, vel = landau(npart, L) # Randomises the position and velocity
        
        # Create some output classes
        # Summary stores an array of the first-harmonic amplitude
        s = Summary()                   # Calculates, stores and prints summary info

        diagnostics_to_run = [s]        # Remove p to get much faster code!
        
        # Run the simulation
        pos, vel = run(pos, vel, L, cell, 
                    out = diagnostics_to_run,           # These are called each output step
                    output_times=linspace(0., 20, ntimes))  # The times to output
        
        # i = where(cells == cell)[0][0]
        harmonic_data[i] += s.firstharmonic
        
        end_time = time.time()
        sim_time_data[i] += end_time-start_time
        print(f'Simulation {i+1} (cells = {cell}) finished in {end_time-start_time}')

    # The time steps are the same for each value of cells, so just keep times to one list!
    time_step_data += s.t
    print(f'Total time: {sum(sim_time_data)}')
    directory = '/Users/jvf522/Documents/CS Lab/Lab1'
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist

    # Now save the file
    savetxt(os.path.join(directory, 'harmonics.txt'), harmonic_data, fmt='%f')
    savetxt(os.path.join(directory, 'step_times.txt'), time_step_data, fmt='%f')
    savetxt(os.path.join(directory, 'sim_times.txt'), sim_time_data, fmt='%f')
