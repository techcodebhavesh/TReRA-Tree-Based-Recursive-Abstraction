import matplotlib.pyplot as plt

import time
import numpy as np

def insertion(arr):
    n = len(arr)
    for i in range(1,n):
        key = arr[i]
        j = i-1
        while j>=0 and arr[j]>key:
            arr[j+1] = arr[j]
            j-=1
        arr[j+1] = key
        
nums = [99999,9999,999,99,9]
print("Before sort......")
print(nums)

insertion(nums)
print("After sort......")
print(nums)


input_sizes = [10, 50, 100, 200, 500, 1000]
execution_times = []

for size in input_sizes:
    arr = np.random.randint(0, 10000, size)  
    start_time = time.time()                 
    insertion(arr)                     
    end_time = time.time()                   
    execution_times.append(end_time - start_time)  


plt.figure(figsize=(10, 6))
plt.plot(input_sizes, execution_times, marker='o', label='Insertion Sort')
plt.title('Insertion Sort Complexity Graph')
plt.xlabel('Input Size (n)')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.legend()
plt.show()