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
    r3 = 60# d["tabletop_r3"]
    s1 = d["tabletop_s1"]
    s2 = -100#d["tabletop_s2"]
    s3 = d["tabletop_s3"]
    x2 = (d["length"] - 150) / 2.0
    x1 = x2 - r3
    y1 = (d["width"] - 150) / 2.0
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

    p[1] = dc.model.sagpoint_by_r(p[0], p[2], -2500)
    p[3] = dc.model.sagpoint_by_r(p[2], p[4], s2)
    p[5] = dc.model.sagpoint(p[4], p[6], s3)
    p[7] = dc.model.sagpoint_by_r(p[6], p[8], s2)
    p[9] = dc.model.sagpoint_by_r(p[8], p[10], -2500)
    p[11] = dc.model.sagpoint_by_r(p[10], p[12], s2)
    p[13] = dc.model.sagpoint(p[12], p[14], s3)
    p[15] = dc.model.sagpoint_by_r(p[14], p[0], s2)

    face = Part.Face(Part.Wire(dc.model.create_arcs(p)))
    m = face.extrude(Base.Vector(0, 0, d["tabletop_t"]))
    m = dc.model.fillet_edges_by_length(m, 20, d["tabletop_t"])

    hx = d["length"] / 2.0 - math.sqrt((d["cx"]**2) / 2.0)
    hy = d["width"] / 2.0 - math.sqrt((d["cx"]**2) / 2.0)

    print("Holes: x distance", hx*2)
    print("Holes: y distance", hy*2)
    print("Holes: diagonal distance", math.sqrt((hx*2)**2 + (hy*2)**2))

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 45
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"] / 2.0, d["tabletop_t"], p, Base.Vector(0, 0, 1), 360)
        insert = Part.makeBox(d["leg_t"], d["insertion_width"], d["insertion_length"])
        insert = dc.model.fillet_edges_by_length(insert, 5, d["insertion_length"])
        insert.translate(Base.Vector(-d["leg_t"] / 2.0, -d["insertion_width"] / 2.0, 0))
        insert.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -a)
        insert.translate(p)
        m = m.cut(hole).cut(insert)
        a = a + 90

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, 7, 300)

    m.translate(Base.Vector(0, 0, -d["tabletop_t"]))
    return m

def leg(d, dressup=True):
    corner_protection = 14
    s1 = d["leg_s1"]
    s2 = d["leg_s2"]
    s3 = d["leg_s3"]
    s4 = d["leg_s4"]

    x0 = d["cx"] + d["insertion_width"]/2.0 + corner_protection
    x1 = d["cx"] - d["insertion_width"]/2.0 + corner_protection
    x2 = x1 - 25
    x3 = 100
    x4 = 80
    x5 = x3 - 55

    y0 = d["height"]
    y2 = d["height_1"] - d["tabletop_t"] + d["insertion_length"]
    y1 = y2 - 12
    y3 = y2 - d["insertion_length"]
    y5 = d["height_2"] - d["insertion_length"]
    y4 = y5 + d["insertion_length"]
    y6 = y5 + 12
    y7 = y0 - 30

    p = [None] * 19
    p[0] = Base.Vector(  0,  y0, 0)
    p[1] = Base.Vector( x4,  y0, 0)

    p[3] = Base.Vector( x2,  y1, 0)
    p[4] = Base.Vector( x1,  y1, 0)
    p[5] = Base.Vector( x1,  y2, 0)
    p[6] = Base.Vector( x0,  y2, 0)
    p[7] = Base.Vector( x0,  y3, 0)

    p[9] = Base.Vector(  x0,  y4, 0)
    p[10] = Base.Vector( x0,  y5, 0)
    p[11] = Base.Vector( x1,  y5, 0)
    p[12] = Base.Vector( x1,  y6, 0)
    p[13] = Base.Vector( x2,  y6, 0)

    p[15] = Base.Vector( x3,   0, 0)
    p[16] = Base.Vector( x5,   0, 0)

    p[18] = Base.Vector(  0,  y7, 0)

    p[2] = dc.model.sagpoint(p[1], p[3], s1)
    p[8] = dc.model.sagpoint(p[7], p[9], s2)
    p[14] = dc.model.sagpoint(p[13], p[15], s3)
    p[17] = dc.model.sagpoint(p[16], p[18], s4)

    wire = [
            Part.makeLine(p[0], p[1]),
            dc.model.makeArc(p[1:4]),
            Part.makeLine(p[3], p[4]),
            Part.makeLine(p[4], p[5]),
            Part.makeLine(p[5], p[6]),
            Part.makeLine(p[6], p[7]),
            dc.model.makeArc(p[7:10]),
            Part.makeLine(p[9], p[10]),
            Part.makeLine(p[10], p[11]),
            Part.makeLine(p[11], p[12]),
            Part.makeLine(p[12], p[13]),
            dc.model.makeArc(p[13:16]),
            Part.makeLine(p[15], p[16]),
            dc.model.makeArc([p[16], p[17], p[18]]),
            Part.makeLine(p[18], p[0])]

    face = Part.Face(Part.Wire(wire))
    m = face.extrude(Base.Vector(0, 0, d["leg_t"]))

    m = dc.model.fillet_edge_xy(m, 100, p[18])
    m = dc.model.fillet_edge_xy(m, 20, p[3])
    m = dc.model.fillet_edge_xy(m, 8, p[4])
    m = dc.model.fillet_edge_xy(m, 8, p[12])
    m = dc.model.fillet_edge_xy(m, 20, p[13])

    m.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    m.translate(Base.Vector(-corner_protection, d["leg_t"] / 2.0, 0))

    hole = Part.makeCylinder(d["hole_dia_leg"] / 2.0, d["height"], Base.Vector(d["cx"], 0, 0), Base.Vector(0, 0, 1), 360)
    m = m.cut(hole)
    corner_cutout = Part.makeBox(4.0*d["leg_t"], 4.0*d["leg_t"], d["glass_t"] + 2.0)
    corner_cutout.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -45.0)
    corner_cutout.translate(Base.Vector(-2, 0, d["height"] - d["glass_t"] - 2.0))
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
    leg1.translate(Base.Vector( d["length"] / 2.0, d["width"] / 2.0, 0))

    # The second leg
    leg2 = leg(d)
    leg2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 315)
    leg2.translate(Base.Vector(-d["length"] / 2.0, d["width"] / 2.0, 0))

    # The third leg
    leg3 = leg(d)
    leg3.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 45)
    leg3.translate(Base.Vector(-d["length"] / 2.0, -d["width"] / 2.0, 0))

    # The fourth leg
    leg4 = leg(d)
    leg4.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 135)
    leg4.translate(Base.Vector( d["length"] / 2.0, -d["width"] / 2.0, 0))

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
    #p = dc.common.add_drawing_page(doc)
    #dc.drawing.create_drawing(doc, p, m, d["tabletop"])
    doc.saveAs(dc.common.fn(d, "tabletop") + ".fcstd")

def leg_drw(d):
    leg1 = leg(d, dressup=False)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, leg1, "leg")
    #p = dc.common.add_drawing_page(doc)
    #dc.drawing.create_drawing(doc, p, m, d["leg"], viewplane="xz")
    doc.saveAs(dc.common.fn(d, "leg") + ".fcstd")

def build_all(user_parameters):
    d = dc.common.load_parameters(os.path.join(os.path.dirname(__file__), "ct1_defaults.yml"))
    d.update(user_parameters)
    coffetable_assy(d)
    #glasstop_drw(d)
    tabletop_drw(d)
    leg_drw(d)
    dc.common.writeinfo(d)

if __name__ == "__main__":
    print("This file should not be run directly.")
