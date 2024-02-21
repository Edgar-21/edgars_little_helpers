import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors
import numpy as np
import math

#take 2 arrays of equal length name and dimension for each layer, make a nice picture

def plotRadialBuild(build, phi_index, theta_index, Title = "Radial Build", colors = None, height = 20, textSpace = 10, size = (8,4)):
    """
    build: dict formatted as for parastell
    phi_index, theta_index; angle pair for the index desired from the thickness matrix
    title: string, title for plot and filename to save to
    colors: list of matplotlib color strings. if specific colors are desired for each layer they can be added here
    height: height to make the rectangles, float
    textSpace: height avaliable for text, float
    size: figure size, inches, tuple
    """
    #extract info
    layers = list(build['radial_build'].keys())

    phi_list = build['phi_list']
    theta_list = build['theta_list']

    radial_build = build['radial_build']

    thicknesses = []

    for layer in layers:
        thicknesses.append(radial_build[layer]['thickness_matrix'][phi_index][theta_index])
    
    #make a list of colors if none provided
    if colors is None: 
        colors = list(matplotlib.colors.XKCD_COLORS.values())[0:len(layers)]

    #initialize list for lower left corner of each layer rectangle
    ll = [0,0]

    #embiggen layers too small for text
    graphicsThicknesses = []

    for i in range(len(thicknesses)):
        if thicknesses[i] < 6:
            graphicsThicknesses.append(6)
        elif thicknesses[i] > 15:
            graphicsThicknesses.append(thicknesses[i]/10+15)
        else:
            graphicsThicknesses.append(thicknesses[i]) 

    plt.figure(1, figsize=size)
    plt.tight_layout()
    ax = plt.gca()
    ax.set_xlim(-1, sum(graphicsThicknesses)+1)
    ax.set_ylim(-textSpace,height+1)
    ax.set_axis_off()

    for layer, thickness, graphicsThickness, color in zip(layers, thicknesses, graphicsThicknesses, colors):
        
        #put the rectangle
        ax.add_patch(Rectangle(ll,graphicsThickness, height, facecolor = color, edgecolor = "black"))
        
        #put the text in
        centerx = (ll[0]+ll[0]+graphicsThickness)/2+1
        centery = (height+1)/2
        plt.text(centerx, centery, layer + " " + str(thickness) + " cm", rotation = "vertical", ha = "center", va = "center")

        #update lower left corner
        ll[0] = ll[0]+float(graphicsThickness)


    plt.title(Title)
    plt.savefig(Title + '.png')

    plt.close()


def main():

    #examples
    layers = ["SOL", "Armor","FW","Breeder","BW","Manifolds","Hight Temp Shield","Gap 1","Vacuum Vessel","Low Temp Shield", "Gap 2", "Coil Case", "Winding Pack", "Coil Case"]
    thicknesses = [5, 0.2, 4, 30, 4, 15, 20, 2, 31, 18, 2, 5, 10, 5]
    build = {layers[i]: thicknesses[i] for i in range(len(layers))}

    #default settings
    radialBuild(build, Title="Radial Build (As Discussed)")



if __name__ == "__main__":
    main()
