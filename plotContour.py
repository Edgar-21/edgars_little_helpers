import matplotlib.pyplot as pl
from matplotlib import cm, ticker

def plotContour(solutions, x, y, barLabel, xlabel, ylabel, title):#plot 2d solutions
    
    #plot it
    fig = pl.figure(figsize=(5,4))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.contourf(x,y,solutions)
    fig.colorbar(c, ax=ax, label= barLabel)
    pl.show
    fig.savefig(title + ".png")
    
def plotContourLog(solutions, x, y, barLabel, xlabel, ylabel, title):#plot 2d solutions
    
    #plot it
    fig = pl.figure(figsize=(5,4))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.contourf(x,y,solutions, locator = ticker.LogLocator())
    fig.colorbar(c, ax=ax, label= barLabel)
    pl.show
    fig.savefig(title + ".png")
