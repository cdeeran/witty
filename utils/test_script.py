import time
for i in range(5, 0, -1):
    print(f"Seconds left running this task: {i}")
    time.sleep(1)
print("Ending task!")
