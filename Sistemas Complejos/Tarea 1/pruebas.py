import numpy as np

c = complex(0,1)

x = np.array([0,0,0], dtype=complex)
x[0] = x[0] + c
print(x)