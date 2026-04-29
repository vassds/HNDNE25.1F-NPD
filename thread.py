from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time

start_time = datetime.now()
print("Start Time:", start_time)

# Define a function that simulates a time-consuming task
def task(name):
    print(f"Task {name} started...")
    time.sleep(2)  # Simulate work by pausing for 2 seconds
    return f"Task {name} finished!"

# Using ThreadPoolExecutor as a context manager
# max_workers=3 means up to 3 threads can run concurrently
with ThreadPoolExecutor(max_workers=80) as executor:

    # Submit multiple tasks to the executor
    # submit() returns a 'Future' object for each task
    results = [executor.submit(task, i) for i in range(1000)]

    # Iterate through the list of Future objects
    for f in results:
        # result() blocks the program until the specific task is complete
        # then it returns the value returned by the task function
        print(f.result())

end_time = datetime.now()
print("End Time:", end_time)

# Duration
print("Execution Time:", end_time - start_time)