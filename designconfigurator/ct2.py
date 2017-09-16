#!/usr/bin/env python2

import math
import os
import sys

sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD
import FreeCAD
from FreeCAD import Base, Part

import designconfigurator as dc

def upper_tabletop_2(d, dressup=True):
    m = Part.makeBox(d["length"], d["width"], d["upper_tabletop_t"])
    m.translate(Base.Vector(-d["length"]/2, -d["width"]/2, 0))
    m = dc.model.fillet_edges_by_length(m, 35, d["upper_tabletop_t"])

    print("Upper tabletop length: ", d["length"])
    print("Upper tabletop width: ", d["width"])

    ccx = d["length"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)
    ccy = d["width"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)
    hx = ccx / 2.0
    hy = ccy / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 135
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["upper_tabletop_t"], p, Base.Vector(0, 0, 1), 360)

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
        m = dc.model.fillet_edges_longer_than(m, d["tabletop_edge_radii"], 300)

    m.translate(Base.Vector(0, 0, -d["upper_tabletop_t"]))
    return m

def upper_tabletop_3(d, dressup=True):
    s = 45
    x1 = d["length"] / 2.0
    y1 = d["width"] / 2.0
    x2 = x1 - 25
    y2 = y1 - 25

    p = [None] * 12

    p[0] = Base.Vector(-x1, y2, 0)
    p[1] = Base.Vector(-x2, y1, 0)

    p[3] = Base.Vector( x2, y1, 0)
    p[4] = Base.Vector( x1, y2, 0)

    p[6] = Base.Vector( x1,-y2, 0)
    p[7] = Base.Vector( x2,-y1, 0)

    p[9] = Base.Vector(-x2,-y1, 0)
    p[10] = Base.Vector(-x1,-y2, 0)

    p[2] = dc.model.sagpoint(p[1], p[3], s)
    p[5] = dc.model.sagpoint(p[4], p[6], s)
    p[8] = dc.model.sagpoint(p[7], p[9], s)
    p[11] = dc.model.sagpoint(p[10], p[0], s)

    wire = [
        Part.makeLine(p[0], p[1]),
        dc.model.makeArc(p[1:4]),
        Part.makeLine(p[3], p[4]),
        dc.model.makeArc(p[4:7]),
        Part.makeLine(p[6], p[7]),
        dc.model.makeArc(p[7:10]),
        Part.makeLine(p[9], p[10]),
        dc.model.makeArc([p[10], p[11], p[0]])]

    face = Part.Face(Part.Wire(wire))
    m = face.extrude(Base.Vector(0, 0, d["upper_tabletop_t"]))
    m = dc.model.fillet_edges_by_length(m, 60, d["upper_tabletop_t"])

    print("Upper tabletop length: ", d["length"])
    print("Upper tabletop width: ", d["width"])

    ccx = d["length"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)
    ccy = d["width"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)
    hx = ccx / 2.0
    hy = ccy / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 135
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["upper_tabletop_t"], p, Base.Vector(0, 0, 1), 360)

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
        m = dc.model.fillet_edges_longer_than(m, d["tabletop_edge_radii"], 300)

    m.translate(Base.Vector(0, 0, -d["upper_tabletop_t"]))
    return m

def lower_tabletop_2(d, dressup=True):
    ccx = d["length"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)
    ccy = d["width"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)

    length = ccx + (2 * d["leg_distance_from_corner"] + d["insertion_width_3"]) / math.sqrt(2.0)
    width = ccy + (2 * d["leg_distance_from_corner"] + d["insertion_width_3"]) / math.sqrt(2.0)

    print("Lower tabletop length: ", length)
    print("Lower tabletop width: ", width)

    m = Part.makeBox(length, width, d["lower_tabletop_t"])
    m.translate(Base.Vector(-length / 2.0, -width / 2.0, 0))
    m = dc.model.fillet_edges_by_length(m, 35, d["lower_tabletop_t"])

    hx = ccx / 2.0
    hy = ccy / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 45
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["lower_tabletop_t"], p, Base.Vector(0, 0, 1), 360)
        insert = Part.makeBox(d["leg_t"], d["insertion_width_3"], d["insertion_length"])
        insert = dc.model.fillet_edges_by_length(insert, d["leg_edge_radii"], d["insertion_length"])
        insert.translate(Base.Vector(-d["leg_t"]/2, -d["insertion_width_3"]/2, 0))
        insert.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -a)
        insert.translate(p)
        m = m.cut(hole).cut(insert)
        a = a + 90

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, d["tabletop_edge_radii"], 150)

    m.translate(Base.Vector(0, 0, -d["lower_tabletop_t"]))
    return m

def lower_tabletop_3(d, dressup=True):
    ccx = d["length"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)
    ccy = d["width"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)

    length = ccx + (2 * d["leg_distance_from_corner"] + d["insertion_width_3"]) / math.sqrt(2.0)
    width = ccy + (2 * d["leg_distance_from_corner"] + d["insertion_width_3"]) / math.sqrt(2.0)

    print("Lower tabletop length: ", length)
    print("Lower tabletop width: ", width)

    x1 = length / 2.0
    y1 = width / 2.0
    x2 = x1 - 25
    y2 = y1 - 25

    p = [None] * 12

    p[0] = Base.Vector(-x1, y2, 0)
    p[1] = Base.Vector(-x2, y1, 0)

    p[3] = Base.Vector( x2, y1, 0)
    p[4] = Base.Vector( x1, y2, 0)

    p[6] = Base.Vector( x1,-y2, 0)
    p[7] = Base.Vector( x2,-y1, 0)

    p[9] = Base.Vector(-x2,-y1, 0)
    p[10] = Base.Vector(-x1,-y2, 0)

    p[2] = dc.model.sagpoint(p[1], p[3], -45)
    p[5] = dc.model.sagpoint(p[4], p[6], -45)
    p[8] = dc.model.sagpoint(p[7], p[9], -45)
    p[11] = dc.model.sagpoint(p[10], p[0], -45)

    wire = [
        Part.makeLine(p[0], p[1]),
        dc.model.makeArc(p[1:4]),
        Part.makeLine(p[3], p[4]),
        dc.model.makeArc(p[4:7]),
        Part.makeLine(p[6], p[7]),
        dc.model.makeArc(p[7:10]),
        Part.makeLine(p[9], p[10]),
        dc.model.makeArc([p[10], p[11], p[0]])]

    face = Part.Face(Part.Wire(wire))
    m = face.extrude(Base.Vector(0, 0, d["lower_tabletop_t"]))
    m = dc.model.fillet_edges_by_length(m, 20, d["lower_tabletop_t"])

    hx = ccx / 2.0
    hy = ccy / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 45
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["lower_tabletop_t"], p, Base.Vector(0, 0, 1), 360)
        insert = Part.makeBox(d["leg_t"], d["insertion_width_3"], d["insertion_length"])
        insert = dc.model.fillet_edges_by_length(insert, d["leg_edge_radii"], d["insertion_length"])
        insert.translate(Base.Vector(-d["leg_t"]/2, -d["insertion_width_3"]/2, 0))
        insert.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -a)
        insert.translate(p)
        m = m.cut(hole).cut(insert)
        a = a + 90

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, d["tabletop_edge_radii"], 150)

    m.translate(Base.Vector(0, 0, -d["lower_tabletop_t"]))
    return m

def leg(d, dressup=True):
    s1 = d["leg_s1"]
    s2 = d["leg_s2"]
    s3 = d["leg_s3"]
    s4 = d["leg_s4"]
    s5 = d["leg_s5"]

    x0 = d["insertion_width_1"]
    x1 = 105
    x2 = d["cx"] - d["insertion_width_3"] / 2.0
    x3 = x2 + d["insertion_width_2"]
    x4 = d["cx"] + d["insertion_width_3"] / 2.0
    x5 = x2 - 20
    x6 = 100
    x7 = x6 - 50

    y0 = d["height"] - d["upper_tabletop_t"] + d["insertion_length"]
    y1 = d["height"] - d["upper_tabletop_t"] - 5
    y2 = y0 - 10
    y3 = d["height_1"] + 100
    y4 = d["height_1"] - d["insertion_length"]
    y5 = y4 + 15

    print("Leg length: ", y0)
    print("Leg width: ", x3)

    p = [None] * 21

    p[0] = Base.Vector(  0,  y0, 0)
    p[1] = Base.Vector( x0,  y0, 0)
    p[2] = Base.Vector( x0,  y1, 0)

    p[4] = Base.Vector( x1,  y3, 0)

    p[6] = Base.Vector( x2,  y1, 0)
    p[7] = Base.Vector( x2,  y0, 0)
    p[8] = Base.Vector( x3,  y0, 0)
    p[9] = Base.Vector( x3,  y1, 0)

    p[11] = Base.Vector( x4,  y5, 0)
    p[12] = Base.Vector( x4,  y4, 0)
    p[13] = Base.Vector( x2,  y4, 0)
    p[14] = Base.Vector( x2,  y5, 0)
    p[15] = Base.Vector( x5,  y5, 0)

    p[17] = Base.Vector( x6,   0, 0)
    p[18] = Base.Vector( x7,   0, 0)

    p[20] = Base.Vector(  0,  y2, 0)

    p[3] = dc.model.sagpoint(  p[2],  p[4], s1)
    p[5] = dc.model.sagpoint(  p[4],  p[6], s2)
    p[10] = dc.model.sagpoint( p[9], p[11], s3)
    p[16] = dc.model.sagpoint(p[15], p[17], s4)
    p[19] = dc.model.sagpoint(p[18], p[20], s5)

    wire = [
        Part.makeLine(p[0], p[1]),
        Part.makeLine(p[1], p[2]),
        dc.model.makeArc(p[2:5]),
        dc.model.makeArc(p[4:7]),
        Part.makeLine(p[6], p[7]),
        Part.makeLine(p[7], p[8]),
        Part.makeLine(p[8], p[9]),
        dc.model.makeArc(p[9:12]),
        Part.makeLine(p[11], p[12]),
        Part.makeLine(p[12], p[13]),
        Part.makeLine(p[13], p[14]),
        Part.makeLine(p[14], p[15]),
        dc.model.makeArc(p[15:18]),
        Part.makeLine(p[17], p[18]),
        dc.model.makeArc(p[18:]),
        Part.makeLine(p[20], p[0])]

    face = Part.Face(Part.Wire(wire))
    m = face.extrude(Base.Vector(0, 0, d["leg_t"]))

    m = dc.model.fillet_edge_xy(m,  7, p[2])
    m = dc.model.fillet_edge_xy(m, 12, p[4])
    m = dc.model.fillet_edge_xy(m,  7, p[6])
    m = dc.model.fillet_edge_xy(m,  7, p[9])
    m = dc.model.fillet_edge_xy(m,  7, p[14])
    m = dc.model.fillet_edge_xy(m, 12, p[15])
    m = dc.model.fillet_edge_xy(m, 30, p[20])
    m.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    m.translate(Base.Vector(0, d["leg_t"] / 2.0, 0))

    hole = Part.makeCylinder(d["hole_dia_leg"] / 2.0, d["height"], Base.Vector(d["cx"], 0, d["height_1"] - d["insertion_length"]), Base.Vector(0, 0, 1), 360)
    m = m.cut(hole)

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, d["leg_edge_radii"], 95)

    return m

def coffetable_assy(d):
    ccx = d["length"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)
    ccy = d["width"] - 2 * math.sqrt(((d["cx"] + d["leg_distance_from_corner"])**2) / 2.0)

    x = ccx / 2.0 + math.sqrt((d["cx"]**2) / 2.0)
    y = ccy / 2.0 + math.sqrt((d["cx"]**2) / 2.0)

    # The upper oak tabletop
    tt1 = upper_tabletop_2(d)
    tt1.translate(Base.Vector(0, 0, d["height"]))

    # The upper oak tabletop 2nd version
    tt4 = upper_tabletop_3(d)
    tt4.translate(Base.Vector(0, 0, d["height"]))

    # The lower oak tabletop
    tt2 = lower_tabletop_2(d)
    tt2.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    tt2.translate(Base.Vector(0, 0, d["height_1"] - d["lower_tabletop_t"]))

    # The lower oak tabletop 2nd version
    tt3 = lower_tabletop_3(d)
    tt3.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    tt3.translate(Base.Vector(0, 0, d["height_1"] - d["lower_tabletop_t"]))

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
    dc.common.add_model(doc, tt4, "upper_tabletop_3")
    dc.common.add_model(doc, tt2, "lower_tabletop")
    dc.common.add_model(doc, tt3, "lower_tabletop_3")
    dc.common.add_model(doc, leg1, "leg1")
    dc.common.add_model(doc, leg2, "leg2")
    dc.common.add_model(doc, leg3, "leg3")
    dc.common.add_model(doc, leg4, "leg4")

    doc.saveAs(dc.common.fn(d, "assy") + ".fcstd")

def upper_tabletop_drw(d):
    # The oak tabletop
    tt1 = upper_tabletop_2(d, dressup=False)
    tt1.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, tt1, "upper_tabletop")
    p = dc.common.add_drawing_page(doc)
    dc.drawing.create_drawing(doc, p, m, d["upper_tabletop"])
    dc.drawing.add_info(p, "SI-2", "Mill pockets to depth: " + str(d["insertion_length"]) + " mm")
    doc.saveAs(dc.common.fn(d, "upper_tabletop") + ".fcstd")

def lower_tabletop_drw(d):
    # The oak tabletop
    tt1 = lower_tabletop_2(d, dressup=False)
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
