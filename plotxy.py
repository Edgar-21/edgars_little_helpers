import matplotlib.pyplot as pl

def plotxy(x, y, xlabel, ylabel, title):#helper for plotting
    fig = pl.figure(figsize=(5,4))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    ax.plot(x, y)
      
    fig.savefig(title + ".png")