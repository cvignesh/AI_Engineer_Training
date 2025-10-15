import numpy as np
n=5
arr = np.random.randint(10,100, size=n)
max_val = np.max(arr)
min_val = np.min(arr)
mean_val = np.mean(arr)
mean_val_round=round(mean_val,2)
print(max_val,min_val,mean_val_round)