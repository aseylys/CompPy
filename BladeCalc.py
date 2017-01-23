from math import *
import stl


################################
##Function: NACA4Blade
##Inputs:
#camberRoot: camber of root (float)
#camberTip: camber of tip (float)
#camberPos: posistion of maximum camber (float)
#thickness: maximum thickness (float)
#bladeHeight: blade height (float)
#twistAngle: blade twist (float)
#rootChord: chord at root (float)
#tipChord: chord at tip (float)
#cot: center of twist coordinates (list)
##Returns:
#(faces, verts): list of faces and list of verts
################################
def NACA4Blade(camberRoot, camberTip, camberPos, thickness,\
                        bladeHeight, twistAngle, rootChord, tipChord, cot):
    
    twist = radians(twistAngle) / bladeHeight
    
    cot = [x / 100 for x in cot]
    
    nspan = 1
    npts = 24
    dspan = bladeHeight / nspan

    xUpTwist= [0]*npts
    yUpTwist= [0]*npts
    xLowTwist= [0]*npts
    yLowTwist= [0]*npts
    faces = []
    verts = []
    origin = (0, 0, 0)
    
    #Generate Vertices for Unmodified Airfoil Shape
    for j in range(0, nspan + 1):
        x = []
        yThickness = []
        yCamber =[]
        xUpper = []
        xLower = []
        yUpper =[]
        yLower =[]
        
        m = (1 - j / nspan) * camberRoot + j / nspan * camberTip   

        
        #NACA4Profile
        for i in range(0, npts + 1):
            x.append(1 - cos(i * (pi / 2) / npts))
            yThickness.append(thickness / 0.2 * (0.2969 * pow(x[i], 0.5) - 0.126 * x[i] - 0.3516 * pow(x[i], 2) + 0.2843 * pow(x[i], 3) - 0.1015 * pow(x[i], 4)))
            
            if (x[i] < camberPos):
                yCamber.append(m / pow(camberPos, 2) * (2 * camberPos * x[i] - pow(x[i], 2)))
                dycdx = 2 * m / pow(camberPos, 2) * (camberPos - x[i])
                
            else:
                yCamber.append(m / pow(1 - camberPos, 2) * (1 - 2 * camberPos + 2 * camberPos * x[i] - pow(x[i], 2)))
                dycdx = 2 * m / pow(1 - camberPos , 2) * (camberPos - x[i])
                
            x[i] -= cot[0]
            yCamber[i] -= cot[1]
        
            #Upper and Lower Vertices
            xUpper.append(x[i] - yThickness[i] * (sin(atan(dycdx))))
            yUpper.append(yCamber[i] + yThickness[i] * (cos(atan(dycdx))))
            xLower.append(x[i] + yThickness[i] * (sin(atan(dycdx))))
            yLower.append(yCamber[i] - yThickness[i] * (cos(atan(dycdx))))
        
        #Generate Vertices Following Twist
        angle = twist * j * dspan
        chord = rootChord - j * dspan * (rootChord - tipChord) / bladeHeight
        
        for i in range(0, npts):
            xUpTwist[i] = (xUpper[i] * cos(angle) - yUpper[i] * sin(angle)) * chord
            yUpTwist[i] = (xUpper[i] * sin(angle) + yUpper[i] * cos(angle)) * chord
            
            verts.append([xUpTwist[i], yUpTwist[i], j * dspan])

        for i in range(0, npts):

            xLowTwist[i] = (xLower[i] * cos(angle) - yLower[i] * sin(angle)) * chord
            yLowTwist[i] = (xLower[i] * sin(angle) + yLower[i] * cos(angle)) * chord
            
            
            verts.append([xLowTwist[i], yLowTwist[i], j * dspan])
    
    #Bottom Prof
    faces.append([0, 1, npts + 1])
    for i in range(0, npts - 1):
        faces.append([i, i + 1, npts + i + 1])    
        faces.append([i, npts + i + 1, npts + i])    

    #Sides
    nPerStage = npts * 2
    for j in range(0, nspan):
        for i in range(0, npts - 1):
            faces.append([nPerStage * j + i, nPerStage * (j + 1) + i, nPerStage * (j + 1) + i + 1])
            faces.append([nPerStage * j + i, nPerStage * (j + 1) + i + 1, nPerStage * j + i + 1])
            
        for i in range(0, npts - 1):
            faces.append([nPerStage * j + i + npts, nPerStage * (j + 1) + i + 1 + npts, nPerStage * (j + 1) + i + npts])
            faces.append([nPerStage * j + i + npts, nPerStage * j + i + 1 + npts, nPerStage * (j + 1) + i + 1 + npts])
        faces.append([nPerStage * j + npts - 1, nPerStage * (j + 1) + npts - 1, nPerStage * (j + 1) + npts * 2 - 1])
        faces.append([nPerStage * j + npts - 1, nPerStage * (j + 1) + npts * 2 - 1, nPerStage * j +npts * 2 - 1])
        
    #Top Prof
    faces.append([nPerStage * nspan, nPerStage * nspan + 1, nPerStage * nspan + npts + 1])
    for i in range(0, npts - 1):
        faces.append([nPerStage * nspan + i, nPerStage * nspan + npts + i + 1, nPerStage * nspan + i + 1])    
        faces.append([nPerStage * nspan + i, nPerStage * nspan + npts + i, nPerStage * nspan + npts + i + 1])  
    
    return (faces, verts)
    
    
################################
##Function: FindBounds
#Calculates bounding box for given object
##Inputs:
#obj: object to be bounded (mesh)
##Returns:
#minx, maxx, miny, maxy, minz, maxz: (floats)
################################
def FindBounds(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
            
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
            
    return minx, maxx, miny, maxy, minz, maxz

    
################################
##Function: StageProps
#Holds stage angles
##Inputs:
#None
##Returns:
#None
################################
class StageProps():
    beta1 = 0
    beta2 = 0
    alpha1 = 0
    alpha2 = 0
    cx = 0
    rpm = 0
    radius = 0
    camber = 0
    r = 0 
    phi = 0
    psi = 0
    

################################
##Function: LinearStageProp
#Holds stage properties
##Inputs:
#None
##Returns:
#None
################################    
class LinearStageProp():
    rootProps = StageProps()
    meanProps = StageProps()
    tipProps = StageProps()
    rootRadius = 0
    tipRadius = 0
    
 
################################
##Function: CalcStageBladeAngles
#Calculates stage angles for the blade
##Inputs:
#r: reaction (float)
#phi: flow (float)
#psi: loading (float)
#rpm: ...rpm (float)
#radius: radius of stage (float)
##Returns:
#stageProps: stage properties (object)
################################ 
def CalcStageBladeAngles(r, phi, psi, rpm, radius):
    u = rpm / 60 * 2 * pi * radius / 1000
    stageProps = StageProps()
    stageProps.rpm = rpm
    stageProps.radius = radius
    stageProps.beta2 = atan((r - psi / 2)  / phi)
    stageProps.beta1 = atan(psi / phi + (2 * r - psi) / (2 * phi))
    stageProps.cx = phi * u
    w1 = stageProps.cx / cos(stageProps.beta1)
    w2 = stageProps.cx / cos(stageProps.beta2)
    c1 = u - w1 * sin(stageProps.beta1)
    c2 = u - w2 * sin(stageProps.beta2)
    stageProps.alpha1 = atan(c1 / stageProps.cx)
    stageProps.alpha2 = atan(c2 / stageProps.cx)
    
    return stageProps
    

################################
##Function: StageCalc
#Calculates propeties of whole stage
##Inputs:
#r: reaction (float)
#phi: flow (float)
#psi: loading (float)
#rpm: ...rpm (float)
#rootRadius: hub radius of stage (float)
#tipRadius: radius of stage (float)
##Returns:
#stageProps: stage properties (object)
################################
def StageCalc(r, phi, psi, rpm, rootRadius, tipRadius):
    stageProps = LinearStageProp()
    stageProps.rootRadius = rootRadius
    stageProps.tipRadius = tipRadius
    
    mlr = (rootRadius + tipRadius) / 2
    stageProps.meanProps = CalcStageBladeAngles(r = r, phi = phi, psi = psi, rpm = rpm, radius = mlr)
    
    stageProps.meanProps.r = r
    stageProps.meanProps.psi = psi
    stageProps.meanProps.phi = phi
    
    stageProps.rootProps = CalcStageBladeAngles(r = r, phi = phi, psi = psi, rpm = rpm, radius = rootRadius)
    
    lphi = 1e-6
    hphi = 2 - 1e-6
    rootPhi = phi
    
    while (abs(stageProps.meanProps.cx - stageProps.rootProps.cx) > 1e-3):
        if (stageProps.rootProps.cx < stageProps.meanProps.cx):
            lphi = rootPhi
            
        else:
            hphi = rootPhi
            
        rootPhi = (hphi + lphi) / 2
        stageProps.rootProps = CalcStageBladeAngles(r = r, phi = rootPhi, psi = psi, rpm = rpm, radius = rootRadius)
        
    stageProps.meanProps.r = r
    stageProps.meanProps.psi = psi
    stageProps.meanProps.phi = rootPhi
    
    stageProps.tipProps = CalcStageBladeAngles(r = r, phi = phi, psi = psi, rpm = rpm, radius = tipRadius)
    
    lphi = 1e-6
    hphi = 2 - 1e-6
    tipPhi = phi
    
    while (abs(stageProps.meanProps.cx - stageProps.tipProps.cx) > 1e-3):
        if (stageProps.tipProps.cx < stageProps.meanProps.cx):
            lphi = tipPhi
            
        else:
            hphi = tipPhi
            
        tipPhi = (hphi + lphi) / 2
        stageProps.tipProps = CalcStageBladeAngles(r = r, phi = tipPhi, psi = psi, rpm = rpm, radius = tipRadius)
    
    stageProps.meanProps.r = r
    stageProps.meanProps.psi = psi
    stageProps.meanProps.phi = tipPhi
    
    return stageProps
    