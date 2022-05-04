from Quanser.q_essential import LIDAR
import time
import struct
import numpy as np 
import matplotlib.pyplot as plt
import math

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
	return time.time() - startTime

sampleRate = 30
sampleTime = 1/sampleRate
simulationTime = 30.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Additional parameters and buffers
counter = 0

# LIDAR initialization and measurement buffers
myLidar = LIDAR(num_measurements=720)

# polar plot object for displaying LIDAR data later on
ax = plt.subplot(111, projection='polar')
plt.show(block=False)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Main Loop
try:
	while elapsed_time() < simulationTime:
		# Clear existing polar plot figure
		plt.cla()

		# Start timing this iteration
		start = time.time()

		# Capture LIDAR data
		myLidar.read()

		# print(myLidar.angles)
		

		# Plot the LIDAR data on the plot every 1 second
		if counter % 10 == 1:
			ax.scatter(myLidar.angles, myLidar.distances, marker='.')
			ax.set_theta_zero_location("W")
			# The set_theta_direction(-1) is set just for the plotting
			ax.set_theta_direction(-1)
			plt.pause(0.0001)
			
		
		
		
		# End timing this iteration
		end = time.time()

		# Calculate the computation time, and the time that the thread should pause/sleep for
		computationTime = end - start
		sleepTime = sampleTime - ( computationTime % sampleTime )
		
		# Pause/sleep and print out the current timestamp
		time.sleep(sleepTime)
		counter += 1
		print('Simulation Timestamp :', elapsed_time(), ' s.')

except KeyboardInterrupt:
	print("User interrupted!")

finally:
	# Close the plot figure
	plt.close()    

	# Terminate the LIDAR object
	myLidar.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 