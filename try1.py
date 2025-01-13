import time
import matplotlib.pyplot as plt
import numpy as np


def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        min_index = i
        for j in range(i+1,n):
            if arr[j]<arr[min_index]:
                min_index = j
        if min_index!=i:
            arr[i],arr[min_index] = arr[min_index],arr[i]



input_sizes = [10, 50, 100, 200, 500, 1000]
execution_times = []

for size in input_sizes:
    arr = np.random.randint(0, 10000, size)  
    start_time = time.time()                 
    selection_sort(arr)                     
    end_time = time.time()                   
    execution_times.append(end_time - start_time)  


plt.figure(figsize=(10, 6))
plt.plot(input_sizes, execution_times, marker='o', label='Selection Sort')
plt.title('Selection Sort Complexity Graph')
plt.xlabel('Input Size (n)')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.legend()
plt.show()
array = [10000,1000,100,10,0]
print("Before sorting:")
print(array)
selection_sort(array)
print(array)