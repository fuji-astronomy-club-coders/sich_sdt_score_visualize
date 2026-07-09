import numpy as np
height = 1104
width = 1680
n_frames = 10

dummy_date = np.random.uniform(
    low=1,
    high=100,
    size=(n_frames,height,width)
)
print(dummy_date)