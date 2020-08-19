import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def plotfit(x,y1,y2,y3,y4,y5,filename,title):
    plt.xlabel('Iterations')
    plt.ylabel('Fitness')
    plt.title(title)
    plt.plot(x, y1, label="best")
    plt.plot(x, y2, label="mean")
    plt.plot(x, y3, label="median")
    plt.plot(x, y4, label="min")
    plt.plot(x, y5, label="max")
    plt.legend(loc='best')
    #plt.show()
    plt.savefig(filename)
 