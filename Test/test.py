import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

# original time-value pairs
x = np.array([0, 5, 10, 15, 20, 30, 45, 50, 60])
y = np.array([0, 3, 1, 0, 2, 0, 2, 0, 0])

# define the interpolation function
f = interpolate.interp1d(x, y, kind='previous')

# generate high-resolution time values for interpolation
xnew = np.linspace(0, 60, num=60, endpoint=True)

# interpolate the values using the new time values
ynew = f(xnew)

# plot the original and interpolated curves
plt.plot(x, y, 'o', label='Original')
plt.plot(xnew, ynew, '.-', label='Interpolated')
plt.legend()
plt.show()
