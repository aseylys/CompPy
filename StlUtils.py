from stl import mesh
import numpy as np
from BladeCalc import * 


################################
#Function: drawCylinder
#Inputs:
#dia: diameter of cylinder
#height: height of cylinder
#res: resoltution of shape (num of sides really)
#Returns:
#cylinder: cylinder mesh object
################################
def drawCylinder(dia, height, res = 25):
    botOrigin = [0, 0, 0]
    topOrigin = [0, 0, height]
    nspan = 1

    #Draw Lower Verts 
    vertices = [[botOrigin[0] + dia / 2 * np.cos(np.deg2rad((360 / res) * i)), botOrigin[1] + dia / 2 * np.sin(np.deg2rad((360 / res) * i)), botOrigin[2]] for i in range(1, res + 1)]
    #Draw Upper Verts
    vertices += [[topOrigin[0] + dia / 2 * np.cos(np.deg2rad((360 / res) * i)), topOrigin[1] + dia / 2 * np.sin(np.deg2rad((360 / res) * i)), topOrigin[2]] for i in range(1, res + 1)]
    #Add Origins to Top and Bottom Faces
    vertices.insert(int(len(vertices) / 2), topOrigin)
    vertices.insert(0, botOrigin)

    vertices = np.array([np.array(x) for x in vertices])

    faces = []
    
    #Generate Bottom and Bottom-to-Top Faces
    for vert in range(1, res + 1):
        nextVert = vert + 1
        if nextVert == res + 1:
            nextVert = 1
        faces.append([vert, nextVert, 0])
        faces.append([vert, nextVert, vert + res + 1])

    #Generate Top and Top-to-Bottom Faces
    for vert in range(res + 2, len(vertices)):
        nextVert = vert + 1
        conVert = vert - res
        if nextVert == len(vertices):
            nextVert = res + 2
            conVert  = 1
        faces.append([vert, nextVert, res + 1])
        faces.append([vert, nextVert, conVert])

    #Delete Any Duplicates IF Any Were Created
    faces = np.array([list(x) for x in  set(tuple(x) for x in faces)])

    # Create the mesh
    cylinder = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        for j in range(3):
            cylinder.vectors[i][j] = vertices[f[j],:]
            
    return cylinder
    

################################
#Function: drawDuct
#Inputs:
#innerDia: inner diameter
#thickness: thickness of duct
#height: height of cylinder
#res: resoltution of shape (num of sides really)
#Returns:
#duct: duct mesh object
################################
def drawDuct(innerDia, thickness, height, res = 25):
    botOrigin = [0, 0, 0]
    topOrigin = [0, 0, height]
    nspan = 1    

    #Draw Lower Outer Verts 
    outer = [[botOrigin[0] + ((innerDia / 2) + thickness) * np.cos(np.deg2rad((360 / res) * i)), botOrigin[1] + ((innerDia / 2) + thickness) * np.sin(np.deg2rad((360 / res) * i)), botOrigin[2]] for i in range(1, res + 1)]
    #Draw Upper Outer Verts
    outer += [[topOrigin[0] + ((innerDia / 2) + thickness) * np.cos(np.deg2rad((360 / res) * i)), topOrigin[1] + ((innerDia / 2) + thickness) * np.sin(np.deg2rad((360 / res) * i)), topOrigin[2]] for i in range(1, res + 1)]
    
    #Draw Lower Outer Verts 
    inner = [[botOrigin[0] + (innerDia / 2) * np.cos(np.deg2rad((360 / res) * i)), botOrigin[1] + (innerDia / 2) * np.sin(np.deg2rad((360 / res) * i)), botOrigin[2]] for i in range(1, res + 1)]
    #Draw Upper Outer Verts
    inner += [[topOrigin[0] + (innerDia / 2) * np.cos(np.deg2rad((360 / res) * i)), topOrigin[1] + (innerDia / 2) * np.sin(np.deg2rad((360 / res) * i)), topOrigin[2]] for i in range(1, res + 1)]
    
    vertices = np.array([np.array(x) for x in outer + inner])
    
    faces = []
    
    #Generate Bottom and Bottom-to-Top Faces
    for vert in range(0,  res):
        nextVert = vert + 1
        if nextVert == res:
            nextVert = 0
        faces.append([vert, nextVert, vert + 2 * res])
        faces.append([vert + 2 * res, nextVert + 2 * res, nextVert])
        faces.append([vert, nextVert, vert + res])
        faces.append([vert + 2 * res, nextVert + 2 * res, vert + res + 2 * res])
        
    #Generate Top and Top-to-Bottom Faces
    for vert in range(res,  2 * res):
        nextVert = vert + 1
        conVert = vert - res + 1
        if nextVert == 2 * res:
            nextVert = res 
            conVert = 0
        faces.append([vert, nextVert, vert + 2 * res])
        faces.append([vert + 2 * res, nextVert + 2 * res, nextVert])
        faces.append([vert, nextVert, conVert])
        faces.append([vert + 2 * res, nextVert + 2 * res, conVert + 2 * res])
        
    faces = np.array([list(x) for x in  set(tuple(x) for x in faces)])

    # Create the mesh
    duct = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        for j in range(3):
            duct.vectors[i][j] = vertices[f[j],:]
            
    return duct
    
    
################################
#Function: drawBlade
#Inputs:
#camberRoot: camber of root
#camberTip: camber of tip
#camberPos: posistion of maximum camber
#thickness: maximum thickness
#bladeHeight: blade height
#twistAngle: blade twist
#rootChord: chord at root
#tipChord: chord at tip
#cot: center of twist coordinates
#Returns:
#bladeMesh: blade mesh object
################################
def drawBlade(camberRoot, camberTip, camberPos, thickness, bladeHeight, twistAngle, rootChord, tipChord, cot):
    #Draw Blade Profile
    bladeProf = NACA4Blade(camberRoot = camberRoot,\
                            camberTip = camberTip,\
                            camberPos = camberPos,\
                            thickness = thickness,\
                            bladeHeight = bladeHeight,\
                            twistAngle = twistAngle,\
                            rootChord = rootChord,\
                            tipChord = tipChord,\
                            cot = cot)
                            
    #Blade Vertices
    bladeVertices = np.array(bladeProf[1])
    #Blade Faces
    bladeFaces = np.array(bladeProf[0])
    
    #Generate Blade Mesh
    bladeMesh = mesh.Mesh(np.zeros(bladeFaces.shape[0], dtype=mesh.Mesh.dtype))
    
    for i, f in enumerate(bladeFaces):
        for j in range(3):
            bladeMesh.vectors[i][j] = bladeVertices[f[j],:]
    
    return bladeMesh

    
    
    
###USED FOR QUICK TESTING
    
if __name__ == '__main__':
    
    from matplotlib import pyplot
    from mpl_toolkits import mplot3d

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    cylinder = drawDuct(10, 2, 5)
    # Render the cylinder
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cylinder.vectors))

    # Auto scale to the mesh size
    scale = cylinder.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    
    xLabel = axes.set_xlabel('X', linespacing=3.2)
    yLabel = axes.set_ylabel('Y', linespacing=3.1)
    zLabel = axes.set_zlabel('Z', linespacing=3.4)
    
    # Show the plot to the screen
    pyplot.show()

