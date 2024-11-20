import matplotlib.pyplot as pl
from matplotlib import cm, ticker
from decimal import Decimal
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.ticker import FormatStrFormatter
from matplotlib import rcParams, use

use("agg")

rcParams.update({"figure.autolayout": True})


def sciFormat(num):
    num = "%.1E" % Decimal(str(num))
    return num


def plot_tri_contour(
    solutions,
    x,
    y,
    xlabel,
    ylabel,
    bar_label,
    title,
    filename=None,
    colormap="plasma",
    levels=None,
    limit_line=0.2,
    decimals=1,
):
    fig = pl.figure(figsize=(8, 6.4))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.tricontourf(x, y, solutions, levels=levels, cmap=colormap)
    l = ax.tricontour(x, y, solutions, colors="black", levels=[limit_line])
    ax.clabel(l, l.levels, inline=True, fontsize=10, fmt=sciFormat)
    fig.colorbar(
        c,
        ax=ax,
        label=bar_label,
        format=ticker.FormatStrFormatter(f"%.{decimals}f"),
    )
    if filename is not None:
        fig.savefig(filename)
    else:
        fig.savefig(title + ".png")
    pl.close()


def plot_tri_contour_log(
    solutions,
    x,
    y,
    xlabel,
    ylabel,
    bar_label,
    title,
    filename=None,
    limit_line=1e18,
    colormap="plasma",
    levels=None,
    decimals=1,
):
    print("beep")
    fig = pl.figure(figsize=(8, 6.4))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.tricontourf(
        x, y, solutions, levels=levels, norm=LogNorm(), cmap=colormap
    )
    l = ax.tricontour(x, y, solutions, colors="black", levels=[limit_line])
    ax.clabel(l, l.levels, inline=True, fontsize=10, fmt=sciFormat)
    fig.colorbar(
        c,
        ax=ax,
        label=bar_label,
        format=ticker.FormatStrFormatter(f"%.{decimals}f"),
    )
    if filename is not None:
        fig.savefig(filename)
    else:
        fig.savefig(title + ".png")
    pl.close()


def plotContour(
    solutions,
    x,
    y,
    barLabel,
    xlabel,
    ylabel,
    title,
    colormap="plasma",
    levels=10,
    filename=None,
    decimals=1,
):  # plot 2d solutions

    # plot it
    fig = pl.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    levels = np.linspace(np.min(solutions), np.max(solutions), levels)
    print(levels)
    c = ax.contourf(x, y, solutions, levels, cmap=colormap)
    cbar = fig.colorbar(c, ax=ax, label=barLabel)
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter(f"%.{decimals}f"))
    if filename is not None:
        fig.savefig(filename)
    else:
        fig.savefig(title + ".png")
    pl.close()


def plotContourLog(
    solutions,
    x,
    y,
    barLabel,
    xlabel,
    ylabel,
    title,
    levels=None,
    colormap="plasma",
    filename=None,
    decimals=1,
):  # plot 2d solutions

    # plot it
    fig = pl.figure(figsize=(5, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.contourf(
        x, y, solutions, norm=LogNorm(), levels=levels, cmap=colormap
    )
    fig.colorbar(
        c,
        ax=ax,
        label=barLabel,
        format=ticker.FormatStrFormatter(f"%.{decimals}f"),
    )
    if filename is not None:
        fig.savefig(filename + ".png")
    else:
        fig.savefig(title + ".png")
    pl.close()


def plotContourLinesLog(
    solutions, x, y, barLabel, xlabel, ylabel, title, decimals=1
):

    # plot it
    fig = pl.figure(figsize=(5, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.contourf(x, y, solutions, locator=ticker.LogLocator())
    l = ax.contour(
        x, y, solutions, colors="black", locator=ticker.LogLocator()
    )
    ax.clabel(l, l.levels, inline=True, fontsize=10, fmt=sciFormat)
    fig.colorbar(
        c,
        ax=ax,
        label=barLabel,
        format=ticker.FormatStrFormatter(f"%.{decimals}f"),
    )
    fig.savefig(title + ".png")
    pl.close()


def plotContourLines(
    solutions, x, y, barLabel, xlabel, ylabel, title, decimals
):

    # plot it
    fig = pl.figure(figsize=(5, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.title(title)
    c = ax.contourf(x, y, solutions)
    l = ax.contour(x, y, solutions, colors="black")
    ax.clabel(l, l.levels, inline=True, fontsize=10, fmt=sciFormat)
    fig.colorbar(
        c,
        ax=ax,
        label=barLabel,
        format=ticker.FormatStrFormatter(f"%.{decimals}f"),
    )
    fig.savefig(title + ".png")
    pl.close()
