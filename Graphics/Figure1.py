import PyChest
import numpy as np
np.random.seed(1)
import matplotlib.pyplot as plt

sequence=[]
sequence = []
sequence.append(np.random.binomial(1, p=0.2, size=2000))
sequence.append(np.random.binomial(1, p=0.7, size=4500))
sequence.append(np.random.binomial(1, p=0.2, size=1500))

sequence = np.concatenate(sequence)

lambd = 1000/len(sequence)

estimates = PyChest.list_estimator(sequence,lambd)

print(estimates)

estimates = PyChest.find_changepoints(sequence, lambd,2)

print(estimates)

N=25

seq=np.convolve(sequence, np.ones(N)/N, mode='valid')

estimates = PyChest.list_estimator(seq, lambd)

print(estimates)

estimates = PyChest.find_changepoints(seq, lambd,2)

print(estimates)

fig, ax = plt.subplots(figsize=(8,5))
ax.set_title(f'Example Data and Estimated Changepoints')
#ax.set(xlabel='Time', ylabel='Moving Average over 25 Elements')
ax.plot(seq)
for estimate in estimates:
	ax.axvline(float(estimate) - N/2, color="red", ls="--")

plt.savefig('python_example.png')
