import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random

def num_of_neighb(state, i, j):
    num = 0
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            num = num + state[(i+x)%state.shape[0], (j+y)%state.shape[1]]
    return num - state[i,j]

def step(state):
    new_state=np.zeros((state.shape[0],state.shape[1]))
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            num = num_of_neighb(state,i,j)
            if state[i,j] == 1:
                if num == 2 or num == 3:
                    new_state[i,j] = 1
            else:
                if num == 3:
                    new_state[i,j] = 1
    return new_state

def init_state(state):
    for i in range(state.shape[0]):
        for j in  range(state.shape[1]):
            if random.randint(0,100)<15:
                state[i,j] = 1

state = np.zeros((64,64))
init_state(state)
fig = plt.figure()
img = plt.imshow(state)

def update(*args):
    global state
    state = step(state)
    img.set_array(state)
    return img,

ani = animation.FuncAnimation(fig=fig, func=update, interval=50, blit=True)
plt.show()
