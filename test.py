import numpy as np
import matplotlib.pyplot as plt


x = np.zeros(5)
y = np.zeros(5)

for i in range (0, 5):
    y[i] = i + 1

print(x)
print(y)

plt.plot(x, y)
plt.show()
