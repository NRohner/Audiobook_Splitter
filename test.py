import numpy as np
import matplotlib.pyplot as plt

a = []
b = [1, 4]
c = [8, 12]

a.append(b)
a.append(c)

a = np.array(a)

print(a)