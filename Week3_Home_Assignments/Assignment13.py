import numpy as np
exe_time = np.random.randint(5, 51, size= (5,50))
print("All Test Cycyle Execution Time:\n",exe_time)
print("average execution time per cycle:")
for index,exe_cycle in enumerate(exe_time,start=1):
    print(f"Average Execution time of cycle {index} is {exe_cycle.mean()}")

print("Test case case with mx execution time is ",exe_time.max())

for index,exe_cycle in enumerate(exe_time,start=1):
    print(f"Std Deviation of cycle {index} is {exe_cycle.std()}")

print("First 10 execution time in cycle 1 is ",exe_time[0,:10])

print("Last 5 execution time in cycle 5 is ",exe_time[4,-5:])

print("Alternate execution time in cycyle 3 is: ",exe_time[2,::2]);

print("Element wise addition between Cycle 1 and Cycle 2 is ",exe_time[0,:]-exe_time[1,:]);
print("Element wise addition between Cycle 1 and Cycle 2 is ",exe_time[0,:]+exe_time[1,:]);
print("Element wise multiplication between Cycle 4 and Cycle 5 is ",exe_time[3,:]*exe_time[4,:]);
print("Element wise multiplication between Cycle 4 and Cycle 5 is ",exe_time[3,:]*exe_time[4,:]);

#Square and cube all execution times.
print("Square of all execution times is:\n", np.square(exe_time))
print("Cube of all execution times is:\n", np.power(exe_time,3))

#square root of all execution times
print("Square root of all execution times is:\n", np.sqrt(exe_time))

#logarithmic transformation of all execution times
print("Logarithmic transformation of all execution times is:\n", np.log(exe_time+1))    

#deep copy of array and change first element of original array to 999
exe_time_copy = exe_time.copy()
exe_time[0,0] = 999
print("Copy of array is:\n",exe_time_copy)

#shallow copy of array and change first element of original array to 888
exe_time_shallow = exe_time.view()
exe_time[0,0] = 888
print("Shallow copy of array is:\n",exe_time_shallow)

#Filtering with condition
#Extract all test cases in Cycle 2 that take more than 30 seconds
print("All execution times in cycle 2 greater than 30 are:\n",exe_time[1,exe_time[1,:]>30])
print("tests that consistently (in every cycle) take more than 25 seconds are:\n",exe_time[exe_time>25])
