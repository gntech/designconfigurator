#!/usr/bin/env python2

import math
import os
import sys

sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD
import FreeCAD
from FreeCAD import Base, Part

import designconfigurator as dc

def glasstop(d, dressup=True):
    m = Part.makeBox(d["length"], d["width"], d["glass_t"])
    m.translate(Base.Vector(-d["length"]/2, -d["width"]/2, -d["glass_t"]))

    if dressup:
        m = dc.model.chamfer_edges_longer_than(m, 2, 100)

    return m

def tabletop(d, dressup=True):
    r3 =  d["tabletop_r3"]
    s1 = d["tabletop_s1"]
    s2 = d["tabletop_s2"]
    s3 = d["tabletop_s3"]
    x2 = (d["length"] - 140) / 2.0
    x1 = x2 - r3
    y1 = (d["width"] - 140) / 2.0
    y2 = y1 - r3

    p = [None] * 17

    p[0] = Base.Vector(-x1,  y1, 0)
    p[2] = Base.Vector( x1,  y1, 0)
    p[4] = Base.Vector( x2,  y2, 0)
    p[6] = Base.Vector( x2, -y2, 0)
    p[8] = Base.Vector( x1, -y1, 0)
    p[10] = Base.Vector(-x1, -y1, 0)
    p[12] = Base.Vector(-x2, -y2, 0)
    p[14] = Base.Vector(-x2,  y2, 0)
    p[16] = Base.Vector(-x1,  y1, 0)

    p[1] = dc.model.sagpoint(p[0], p[2], s1)
    p[3] = dc.model.sagpoint(p[2], p[4], s2)
    p[5] = dc.model.sagpoint(p[4], p[6], s3)
    p[7] = dc.model.sagpoint(p[6], p[8], s2)
    p[9] = dc.model.sagpoint(p[8], p[10], s1)
    p[11] = dc.model.sagpoint(p[10], p[12], s2)
    p[13] = dc.model.sagpoint(p[12], p[14], s3)
    p[15] = dc.model.sagpoint(p[14], p[0], s2)

    face = Part.Face(Part.Wire(dc.model.create_arcs(p)))
    m = face.extrude(Base.Vector(0, 0, d["tabletop_t"]))
    m = dc.model.fillet_edges_by_length(m, 20, d["tabletop_t"])

    hx = d["length"] / 2.0 - math.sqrt((d["cx"]**2) / 2.0)
    hy = d["width"] / 2.0 - math.sqrt((d["cx"]**2) / 2.0)

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 45
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["tabletop_t"], p, Base.Vector(0, 0, 1), 360)
        insert = Part.makeBox(d["leg_t"], d["insertion_width"], d["insertion_length"])
        insert = dc.model.fillet_edges_by_length(insert, 5, d["insertion_length"])
        insert.translate(Base.Vector(-d["leg_t"]/2, -d["insertion_width"]/2, 0))
        insert.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -a)
        insert.translate(p)
        m = m.cut(hole).cut(insert)
        a = a + 90

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, 7, 300)

    m.translate(Base.Vector(0, 0, -d["tabletop_t"]))
    return m

def leg(d, dressup=True):
    corner_protection = 12

    x0 = d["cx"] + d["insertion_width"]/2 + corner_protection
    x1 = d["cx"] - d["insertion_width"]/2 + corner_protection
    x2 = x1 - 25
    x3 = 115
    x4 = 80
    x5 = 60

    y1 = d["height"] - 30
    y2 = d["height_1"] - d["tabletop_t"] + d["insertion_length"]
    y3 = y2 - 5
    y4 = y2 - 12
    y7 = d["height_2"] - d["insertion_length"]
    y6 = y7 + 5
    y5 = y7 + 12

    dx = 5

    p = [
            Base.Vector( x3, 0, 0),
            Base.Vector( x5, 0,  0),
            Base.Vector( x5+12, y6, 0),
            Base.Vector(  0, y1,  0),
            Base.Vector(  0, d["height"],  0),
            Base.Vector( x4, d["height"],  0),
            Base.Vector( x4+12, d["height"]-70, 0),
            Base.Vector( x2, y4, 0),
            Base.Vector( x1, y4, 0),
            Base.Vector( x1, y2, 0),
            Base.Vector( x0, y2, 0),
            Base.Vector( x0, y3, 0),
            Base.Vector( x0-dx, (y2+y7)/2, 0),
            Base.Vector( x0, y6, 0),
            Base.Vector( x0, y7, 0),
            Base.Vector( x1, y7, 0),
            Base.Vector( x1, y5, 0),
            Base.Vector( x2, y5, 0),
            Base.Vector( x3+18, 70, 0)]

    wire = [
            Part.makeLine(p[0], p[1]),
            dc.model.makeArc(p[1:4]),
            Part.makeLine(p[3], p[4]),
            Part.makeLine(p[4], p[5]),
            dc.model.makeArc(p[5:8]),
            Part.makeLine(p[7], p[8]),
            Part.makeLine(p[8], p[9]),
            Part.makeLine(p[9], p[10]),
            Part.makeLine(p[10], p[11]),
            dc.model.makeArc(p[11:14]),
            Part.makeLine(p[13], p[14]),
            Part.makeLine(p[14], p[15]),
            Part.makeLine(p[15], p[16]),
            Part.makeLine(p[16], p[17]),
            dc.model.makeArc([p[17], p[18], p[0]])]

    face = Part.Face(Part.Wire(wire))
    m = face.extrude(Base.Vector(0, 0, d["leg_t"]))

    m = dc.model.fillet_edge_xy(m, 100, p[3])
    m = dc.model.fillet_edge_xy(m, 20, p[7])
    m = dc.model.fillet_edge_xy(m, 8, p[8])
    m = dc.model.fillet_edge_xy(m, 8, p[16])
    m = dc.model.fillet_edge_xy(m, 20, p[17])

    m.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    m.translate(Base.Vector(-corner_protection, d["leg_t"]/2, 0))

    hole = Part.makeCylinder(d["hole_dia_leg"] / 2.0, d["height"], Base.Vector(d["cx"], 0, 0), Base.Vector(0, 0, 1), 360)
    m = m.cut(hole)
    corner_cutout = Part.makeBox(2*d["leg_t"], 2*d["leg_t"], d["glass_t"])
    corner_cutout.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -45)
    corner_cutout.translate(Base.Vector(0, 0, d["height"] - d["glass_t"]))
    m = m.cut(corner_cutout)

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, 7, 100)

    return m

def coffetable_assy(d):
    # The glass tabletop
    gt1 = glasstop(d)
    gt1.translate(Base.Vector(0, 0, d["height"]))

    # The upper oak tabletop
    tt1 = tabletop(d)
    tt1.translate(Base.Vector(0, 0, d["height_1"]))

    # The lower oak tabletop
    tt2 = tabletop(d)
    tt2.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    tt2.translate(Base.Vector(0, 0, d["height_2"] - d["tabletop_t"]))

    # The first leg
    leg1 = leg(d)
    leg1.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 225)
    leg1.translate(Base.Vector( d["length"] / 2, d["width"] / 2, 0))

    # The second leg
    leg2 = leg(d)
    leg2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 315)
    leg2.translate(Base.Vector(-d["length"] / 2, d["width"] / 2, 0))

    # The third leg
    leg3 = leg(d)
    leg3.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 45)
    leg3.translate(Base.Vector(-d["length"] / 2, -d["width"] / 2, 0))

    # The fourth leg
    leg4 = leg(d)
    leg4.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 135)
    leg4.translate(Base.Vector( d["length"] / 2, -d["width"] / 2, 0))

    doc = dc.common.create_doc()
    dc.common.add_model(doc, gt1, "glassTop")
    dc.common.add_model(doc, tt1, "upperTableTop")
    dc.common.add_model(doc, tt2, "lowerTableTop")
    dc.common.add_model(doc, leg1, "leg1")
    dc.common.add_model(doc, leg2, "leg2")
    dc.common.add_model(doc, leg3, "leg3")
    dc.common.add_model(doc, leg4, "leg4")

    doc.saveAs(dc.common.fn(d, "assy") + ".fcstd")

def glasstop_drw(d):
    # The glass tabletop
    gt1 = glasstop(d)
    doc = dc.common.create_doc()
    dc.common.add_model(doc, gt1, "glassTop")
    doc.saveAs(dc.common.fn(d, "glasstop") + ".fcstd")

def tabletop_drw(d):
    # The oak tabletop
    tt1 = tabletop(d, dressup=False)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, tt1, "tableTop")
    p = dc.common.add_drawing_page(doc)
    dc.drawing.create_drawing(doc, p, m, d["tabletop"])
    doc.saveAs(dc.common.fn(d, "tabletop") + ".fcstd")

def leg_drw(d):
    leg1 = leg(d, dressup=False)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, leg1, "leg")
    p = dc.common.add_drawing_page(doc)
    dc.drawing.create_drawing(doc, p, m, d["leg"], viewplane="xz")
    doc.saveAs(dc.common.fn(d, "leg") + ".fcstd")

def build_all(user_parameters):
    d = dc.common.load_parameters(os.path.join(os.path.dirname(__file__), "ct1_defaults.yml"))
    d.update(user_parameters)
    coffetable_assy(d)
    glasstop_drw(d)
    tabletop_drw(d)
    leg_drw(d)

if __name__ == "__main__":
    print("This file should not be run directly.")
