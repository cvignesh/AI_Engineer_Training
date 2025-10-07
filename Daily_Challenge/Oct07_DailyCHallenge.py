#calculate mean,. median and std dev
import numpy as np
inp = np.array([10,20,30,40,50])
out_mean = float(np.mean(inp))
out_median = float(np.median(inp))
out_std = round(float(np.std(inp)),2)
out = (out_mean, out_median, out_std)
print(out)