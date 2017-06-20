#!/usr/bin/env python2

import math
import os
import sys

sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD
import FreeCAD
from FreeCAD import Base, Part

import designconfigurator as dc

def upper_tabletop(d, dressup=True):
    x1 = d["length"] / 2.0
    y1 = d["width"] / 2.0
    s1 = d["upper_tabletop_s1"]
    s2 = d["upper_tabletop_s2"]

    p = [None] * 9

    p[0] = Base.Vector(-x1,  y1, 0)
    p[2] = Base.Vector( x1,  y1, 0)
    p[4] = Base.Vector( x1, -y1, 0)
    p[6] = Base.Vector(-x1, -y1, 0)
    p[8] = Base.Vector(-x1,  y1, 0)

    p[1] = dc.model.sagpoint(p[0], p[2], s1)
    p[3] = dc.model.sagpoint(p[2], p[4], s2)
    p[5] = dc.model.sagpoint(p[4], p[6], s1)
    p[7] = dc.model.sagpoint(p[6], p[8], s2)

    face = Part.Face(Part.Wire(dc.model.create_arcs(p)))
    m = face.extrude(Base.Vector(0, 0, d["tabletop_t"]))
    m = dc.model.fillet_edges_by_length(m, d["upper_tabletop_corner_radii"], d["tabletop_t"])

    ccx = d["length"] - 2 * math.sqrt((d["cx"]**2) / 2.0) - 2 * d["leg_distance_from_corner"]
    ccy = d["width"] - 2 * math.sqrt((d["cx"]**2) / 2.0) - 2 * d["leg_distance_from_corner"]
    hx = ccx / 2.0
    hy = ccy / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 135
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["tabletop_t"], p, Base.Vector(0, 0, 1), 360)

        insert_1 = Part.makeBox(d["leg_t"], d["insertion_width_1"], d["insertion_length"])
        insert_1 = dc.model.fillet_edges_by_length(insert_1, d["leg_edge_radii"], d["insertion_length"])
        insert_1.translate(Base.Vector(-d["leg_t"]/2, -d["cx"], 0))
        insert_1.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), a)
        insert_1.translate(p)

        insert_2 = Part.makeBox(d["leg_t"], d["insertion_width_2"], d["insertion_length"])
        insert_2 = dc.model.fillet_edges_by_length(insert_2, d["leg_edge_radii"], d["insertion_length"])
        insert_2.translate(Base.Vector(-d["leg_t"]/2, -d["insertion_width_3"] / 2.0, 0))
        insert_2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), a)
        insert_2.translate(p)

        m = m.cut(insert_1).cut(insert_2).cut(hole)
        a = a + 90

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, d["tabletop_edge_radii"], 500)

    m.translate(Base.Vector(0, 0, -d["tabletop_t"]))
    return m

def lower_tabletop(d, dressup=True):
    ccx = d["length"] - 2 * math.sqrt((d["cx"]**2) / 2.0) - 2 * d["leg_distance_from_corner"]
    ccy = d["width"] - 2 * math.sqrt((d["cx"]**2) / 2.0) - 2 * d["leg_distance_from_corner"]

    r3 =  d["tabletop_r3"]
    s1 = d["tabletop_s1"]
    s2 = d["tabletop_s2"]
    s3 = d["tabletop_s3"]
    x2 = (ccx + 2 * r3) / 2.0
    x1 = x2 - r3
    y1 = (ccy + 2 * r3) / 2.0
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

    hx = ccx / 2.0
    hy = ccy / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 45
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["tabletop_t"], p, Base.Vector(0, 0, 1), 360)
        insert = Part.makeBox(d["leg_t"], d["insertion_width_3"], d["insertion_length"])
        insert = dc.model.fillet_edges_by_length(insert, d["leg_edge_radii"], d["insertion_length"])
        insert.translate(Base.Vector(-d["leg_t"]/2, -d["insertion_width_3"]/2, 0))
        insert.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -a)
        insert.translate(p)
        m = m.cut(hole).cut(insert)
        a = a + 90

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, d["tabletop_edge_radii"], 300)

    m.translate(Base.Vector(0, 0, -d["tabletop_t"]))
    return m

def leg(d, dressup=True):
    x0 = d["insertion_width_1"]
    x2 = 150
    x1 = (x0 + x2) / 2.0 - 30
    x4 = d["cx"] - d["insertion_width_3"] / 2.0
    x3 = (x2 + x4) / 2.0 + 10
    x5 = x4 + d["insertion_width_2"]
    x7 = d["cx"] + d["insertion_width_3"] / 2.0
    x6 = (x5 + x7) / 2.0 - 10
    x8 = d["cx"] - d["insertion_width_3"] / 2.0
    x9 = x8 - 30
    x11 = 100
    x10 = (x9 + x11) / 2.0 - 5
    x12 = x11 - 50
    x13 = x12 + 12

    y0 = d["height"]
    y1 = d["height"] - d["tabletop_t"]
    y4 = d["height"] - d["tabletop_t"] + d["insertion_length"]
    y3 = d["height_1"] + 120
    y2 = (y1 + y3) / 2.0
    y6 = d["height_1"] - d["insertion_length"]
    y5 = (y4 + y6) / 2.0
    y7 = y6 + 25
    y8 = y7 / 2.0
    y9 = y0 - 50

    p = [
        Base.Vector(  0, y4, 0),
        Base.Vector( x0, y4, 0),
        Base.Vector( x0, y1, 0),
        Base.Vector( x1, y2, 0),
        Base.Vector( x2, y3, 0),
        Base.Vector( x3, y2, 0),
        Base.Vector( x4, y4, 0),
        Base.Vector( x5, y4, 0),
        Base.Vector( x6, y5, 0),
        Base.Vector( x7, y6, 0),
        Base.Vector( x8, y6, 0),
        Base.Vector( x8, y7, 0),
        Base.Vector( x9, y7, 0),
        Base.Vector(x10, y8, 0),
        Base.Vector(x11,  0, 0),
        Base.Vector(x12,  0, 0),
        Base.Vector(x13, y8, 0),
        Base.Vector(  0, y9, 0)]

    wire = [
        Part.makeLine(p[0], p[1]),
        Part.makeLine(p[1], p[2]),
        dc.model.makeArc(p[2:5]),
        dc.model.makeArc(p[4:7]),
        Part.makeLine(p[6], p[7]),
        dc.model.makeArc(p[7:10]),
        Part.makeLine(p[9], p[10]),
        Part.makeLine(p[10], p[11]),
        Part.makeLine(p[11], p[12]),
        dc.model.makeArc(p[12:15]),
        Part.makeLine(p[14], p[15]),
        dc.model.makeArc(p[15:]),
        Part.makeLine(p[17], p[0])]

    face = Part.Face(Part.Wire(wire))
    m = face.extrude(Base.Vector(0, 0, d["leg_t"]))
    m = dc.model.fillet_edge_xy(m, 20, p[4])
    m = dc.model.fillet_edge_xy(m,  7, p[11])
    m = dc.model.fillet_edge_xy(m, 12, p[12])
    m = dc.model.fillet_edge_xy(m, 150, p[17])
    m.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    m.translate(Base.Vector(0, d["leg_t"] / 2.0, 0))

    hole = Part.makeCylinder(d["hole_dia_leg"] / 2.0, d["height"], Base.Vector(d["cx"], 0, d["height_1"] - d["insertion_length"]), Base.Vector(0, 0, 1), 360)
    m = m.cut(hole)

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, d["leg_edge_radii"], 100)

    return m

def coffetable_assy(d):
    ccx = d["length"] - 2 * math.sqrt((d["cx"]**2) / 2.0) - 2 * d["leg_distance_from_corner"]
    ccy = d["width"] - 2 * math.sqrt((d["cx"]**2) / 2.0) - 2 * d["leg_distance_from_corner"]

    x = ccx / 2.0 + math.sqrt((d["cx"]**2) / 2.0)
    y = ccy / 2.0 + math.sqrt((d["cx"]**2) / 2.0)

    # The upper oak tabletop
    tt1 = upper_tabletop(d)
    tt1.translate(Base.Vector(0, 0, d["height"]))

    # The lower oak tabletop
    tt2 = lower_tabletop(d)
    tt2.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    tt2.translate(Base.Vector(0, 0, d["height_1"] - d["tabletop_t"]))

    # The first leg
    leg1 = leg(d)
    leg1.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 225)
    leg1.translate(Base.Vector( x, y, 0))

    # The second leg
    leg2 = leg(d)
    leg2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 315)
    leg2.translate(Base.Vector(-x, y, 0))

    # The third leg
    leg3 = leg(d)
    leg3.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 45)
    leg3.translate(Base.Vector(-x, -y, 0))

    # The fourth leg
    leg4 = leg(d)
    leg4.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 135)
    leg4.translate(Base.Vector( x, -y, 0))

    doc = dc.common.create_doc()
    dc.common.add_model(doc, tt1, "upper_tabletop")
    dc.common.add_model(doc, tt2, "lower_tabletop")
    dc.common.add_model(doc, leg1, "leg1")
    dc.common.add_model(doc, leg2, "leg2")
    dc.common.add_model(doc, leg3, "leg3")
    dc.common.add_model(doc, leg4, "leg4")

    doc.saveAs(dc.common.fn(d, "assy") + ".fcstd")

def upper_tabletop_drw(d):
    # The oak tabletop
    tt1 = upper_tabletop(d, dressup=False)
    tt1.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, tt1, "upper_tabletop")
    p = dc.common.add_drawing_page(doc)
    dc.drawing.create_drawing(doc, p, m, d["upper_tabletop"])
    dc.drawing.add_info(p, "SI-2", "Mill pockets to depth: " + str(d["insertion_length"]) + " mm")
    doc.saveAs(dc.common.fn(d, "upper_tabletop") + ".fcstd")

def lower_tabletop_drw(d):
    # The oak tabletop
    tt1 = lower_tabletop(d, dressup=False)
    tt1.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, tt1, "lower_tabletop")
    p = dc.common.add_drawing_page(doc)
    dc.drawing.create_drawing(doc, p, m, d["lower_tabletop"])
    dc.drawing.add_info(p, "SI-2", "Mill pockets to depth: " + str(d["insertion_length"]) + " mm")
    doc.saveAs(dc.common.fn(d, "lower_tabletop") + ".fcstd")

def leg_drw(d):
    leg1 = leg(d, dressup=False)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, leg1, "leg")
    p = dc.common.add_drawing_page(doc)
    dc.drawing.create_drawing(doc, p, m, d["leg"], viewplane="xz")
    dc.common.add_model(doc, leg1, "leg")
    doc.saveAs(dc.common.fn(d, "leg") + ".fcstd")

def build_all(user_parameters):
    d = dc.common.load_parameters(os.path.join(os.path.dirname(__file__), "ct2_defaults.yml"))
    d.update(user_parameters)
    coffetable_assy(d)
    upper_tabletop_drw(d)
    lower_tabletop_drw(d)
    leg_drw(d)

if __name__ == "__main__":
    print("This file should not be run directly.")
