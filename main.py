
from epic1d import *

if __name__ == "__main__":
    # Generate initial condition
    # 
    npart = 20000   
    
    if False:
        # 2-stream instability
        L = 100
        ncells = 20
        pos, vel = twostream(npart, L, 3.) # Might require more npart than Landau!
    else:
        # Landau damping
        L = 4.*pi
        ncells = 20
        pos, vel = landau(npart, L)
    
    # Create some output classes
    # p = Plot(pos, vel, ncells, L) # This displays an animated figure - Slow!
    s = Summary()                 # Calculates, stores and prints summary info

    diagnostics_to_run = [s]   # Remove p to get much faster code!

    
    # Run the simulation
    pos, vel = run(pos, vel, L, ncells, 
                   out = diagnostics_to_run,        # These are called each output step
                   output_times=linspace(0.,20,50)) # The times to output
    
    # Summary stores an array of the first-harmonic amplitude


    harmonic_data = column_stack((s.t, s.firstharmonic))
    
    directory = '/Users/jvf522/Documents/CS Lab/Lab1'
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist

    # Now save the file
    savetxt(os.path.join(directory, 'harmonics.txt'), harmonic_data, fmt='%f')
