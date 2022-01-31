import matplotlib.pyplot as plt
import os


fig = plt.figure()
plt.cla()
plt.close(fig)

def make_plot(li, k):
    #regions = [24, 90, 76, 30, 45, 10, 37]
    colors = ['orange', 'green', 'blue', 'yellow', 'pink', 'purple', 'lightgreen']

    fig = plt.figure()
    fig.set_size_inches(4.6, 4)
    ax = fig.add_axes([0.12,0.12,0.8,0.8])
    plot = ax.bar([str(i+1) for i in range(7)], li, width=1.0, edgecolor='black')
    for i in range(7):
        plot[i].set_color(colors[i])

    plt.savefig(os.getcwd()+ "\DSS\pics\graph"+ str(k)+ ".png")
    plt.clf()
    plt.cla()
    plt.close(fig)

