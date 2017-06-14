import sys
sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD, Part
from FreeCAD import Base

def vector(x, y, z):
    return Base.Vector(x, y, z)

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

    return obj.makeFillet(r, edges_to_fillet)
