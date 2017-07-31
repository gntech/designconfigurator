import math
import sys
sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD, Part
from FreeCAD import Base

def sagpoint(p1, p2, sag):
    assert p1.z == p2.z

    pm = p2.sub(p1)
    pm.multiply(0.5)

    p = p2.sub(p1)
    p.normalize() # Make length 1
    p.multiply(abs(sag)) # Make length sag
    if(sag > 0):
        p.x, p.y = -p.y, p.x # Rotate sag 90 deg
    else:
        p.x, p.y = p.y, -p.x # Rotate sag -90 deg

    return p1.add(pm).add(p)

def sagpoint_by_r(p1, p2, r):
    l = p2.sub(p1).Length / 2.0
    print l
    s = abs(r) - math.sqrt(r**2 - l**2)
    print s
    if r > 0:
        return sagpoint(p1, p2, s)
    else:
        return sagpoint(p1, p2, -s)

def makeArc(p):
    arc = Part.Arc(p[0], p[1], p[2])
    return arc.toShape()

def create_arcs(points):
    arcs = []
    for i in range(1, len(points), 2):
        arcs.append(makeArc(points[i-1:i+2]))
    return arcs

def fillet_edge_xy(obj, r, p):
    for edge in obj.Edges:
        v0 = edge.Vertexes[0]
        v1 = edge.Vertexes[1]
        if round(v0.X) == p[0] and round(v0.Y) == p[1] and round(v1.X) == p[0] and round(v1.Y) == p[1]:
            return obj.makeFillet(r, [edge])
    print("No edge found to be filled")
    return obj

def fillet_edges_by_length(obj, r, edgelength):
    edges_to_fillet = []
    for edge in obj.Edges:
        if edge.Length == edgelength:
            edges_to_fillet.append(edge)

    if edges_to_fillet == []:
        print("Did not find any edge with lenght " + str(edgelength))
        return obj
    else:
        return obj.makeFillet(r, edges_to_fillet)

def fillet_edges_longer_than(obj, r, edgelength):
    edges_to_fillet = []
    for edge in obj.Edges:
        if edge.Length > edgelength:
            edges_to_fillet.append(edge)

    if edges_to_fillet == []:
        print("Didnt find any edges longer than " + str(edgelength))
        return obj
    else:
        return obj.makeFillet(r, edges_to_fillet)

def chamfer_edges_longer_than(obj, r, edgelength):
    edges_to_chamfer = []
    for edge in obj.Edges:
        if edge.Length > edgelength:
            edges_to_chamfer.append(edge)

    if edges_to_chamfer == []:
        print("Didnt find any edges longer than " + str(edgelength))
        return obj
    else:
        return obj.makeChamfer(r, edges_to_chamfer)

def fillet_edges_by_nr(obj, r, edge_nr):
    edges_to_fillet = []
    for nr in edge_nr:
        edges_to_fillet.append(obj.Edges[nr])

    return obj.makeFillet(r, edges_to_fillet)
