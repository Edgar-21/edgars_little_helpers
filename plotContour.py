import matplotlib.pyplot as pl
from matplotlib import cm, ticker
from decimal import Decimal
import numpy as np

def sciFormat(num):
    num = '%.1E' % Decimal(str(num))
    return num
    

def plotContour(solutions, x, y, barLabel, xlabel, ylabel, title, colormap = 'viridis', levels=10):#plot 2d solutions
    
    #plot it
    fig = pl.figure(figsize=(5,4))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    levels = np.linspace(np.min(solutions),np.max(solutions),levels)
    c = ax.contourf(x,y,solutions,levels,cmap=colormap)
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
    
def plotContourLinesLog(solutions, x, y, barLabel, xlabel, ylabel, title):
    
    #plot it
    fig = pl.figure(figsize=(5,4))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.contourf(x,y,solutions, locator = ticker.LogLocator())
    l = ax.contour(x,y,solutions, colors='black', locator = ticker.LogLocator())
    ax.clabel(l,l.levels,inline=True,fontsize=10,fmt=sciFormat)
    fig.colorbar(c, ax=ax, label= barLabel)
    pl.show
    fig.savefig(title + ".png")

def plotContourLines(solutions, x, y, barLabel, xlabel, ylabel, title):
    
    #plot it
    fig = pl.figure(figsize=(5,4))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.contourf(x,y,solutions)
    l = ax.contour(x,y,solutions, colors='black')
    ax.clabel(l,l.levels,inline=True,fontsize=10,fmt=sciFormat)
    fig.colorbar(c, ax=ax, label= barLabel)
    pl.show
    fig.savefig(title + ".png")

