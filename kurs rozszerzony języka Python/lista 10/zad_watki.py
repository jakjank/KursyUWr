import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random
import threading
import queue

def num_of_neighb(state, i, j):
    num = 0
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            num = num + state[(i+x)%state.shape[0], (j+y)%state.shape[1]]
    return num - state[i,j]

def step(shared_queue):
    while True:
        global state, new_state
        if(shared_queue.empty()):
            break

        row_index=shared_queue.get()
        new_row=np.zeros((state.shape[0]))
        for j in range(state.shape[1]):
            num = num_of_neighb(state,row_index,j)
            if state[row_index,j] == 1:
                if num == 2 or num == 3:
                    new_row[j] = 1
            else:
                if num == 3:
                    new_row[j] = 1

        new_state[row_index : new_state.shape[1]]=new_row
        shared_queue.task_done()

def init_state(state):
    for i in range(state.shape[0]):
        for j in  range(state.shape[1]):
            if random.randint(0,100)<15:
                state[i,j] = 1

state = np.zeros((150,150))
new_state = np.zeros_like(state)
init_state(state)
fig = plt.figure()
img = plt.imshow(state)
shared_queue = queue.Queue()


def update(*args):
    global state, shared_queue, new_state
    for i in range(state.shape[0]):
        shared_queue.put(i)

    watki = [threading.Thread(target=step,
                            args=(shared_queue,))
                for _ in range(15)]
                
    [w.start() for w in watki]
    if(threading.active_count()==1):
        state = new_state
        new_state = np.zeros_like(state)
        print(state, end="\n\n")
        img.set_array(state)
    return img,

ani = animation.FuncAnimation(fig=fig, func=update, interval=30, blit=True)
plt.show()
