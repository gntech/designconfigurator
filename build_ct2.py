#!/usr/bin/env python2

import math
import sys
import yaml
sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD
from FreeCAD import Base

import designconfigurator as dc

def load_parameters(fn):
    d = {"project": "Undefined",
        "assy":     {"nr": "aaaaaa-aaa", "name": "Assy", "rev": "A"},
        "tabletop": {"nr": "bbbbbb-bbb", "name": "Tabletop", "rev": "A"},
        "leg":      {"nr": "cccccc-ccc", "name": "Leg", "rev": "A"},
        "ccx": 600,
        "ccy": 350,
        "height": 500,
        "height_1": 180,
        "t_tabletop": 18,
        "t_leg": 36,
        "insertion_width_1": 50,
        "insertion_width_2": 80,
        "insertion_width_3": 40,
        "insertion_length": 3,
        "hole_dia_tabletop": 9,
        "hole_dia_leg": 8,
        "tabletop_corner_radii": 50,
        "tabletop_delta_x": -30,
        "tabletop_delta_y": -30,
        "leg_width": 60,
        "cx": 220}

    with open(fn, "r") as f:
        d_user = yaml.load(f)

    d.update(d_user)
    return d

def tabletop(d):
    y0 = d["ccy"] / 2.0 + d["tabletop_corner_radii"]
    x0 = d["ccx"] / 2.0 + d["tabletop_corner_radii"]
    x1 = x0 + d["tabletop_delta_x"]
    y1 = y0 + d["tabletop_delta_y"]

    points = [Base.Vector( x0,  y0, 0),
                Base.Vector( x1,   0, 0),
                Base.Vector( x0, -y0, 0),
                Base.Vector(  0, -y1, 0),
                Base.Vector(-x0, -y0, 0),
                Base.Vector(-x1,   0, 0),
                Base.Vector(-x0,  y0, 0),
                Base.Vector(  0,  y1, 0),
                Base.Vector( x0,  y0, 0)]

    face = Part.Face(Part.Wire(dc.model.create_arcs(points)))
    m = face.extrude(Base.Vector(0, 0, d["t_tabletop"]))
    m = dc.model.fillet_edges_by_length(m, d["tabletop_corner_radii"], d["t_tabletop"])

    hx = d["ccx"] / 2.0
    hy = d["ccy"] / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 45
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["t_tabletop"], p, Base.Vector(0, 0, 1), 360)
        insert = Part.makeBox(d["t_leg"], d["insertion_width"], d["insertion_length"])
        insert = dc.model.fillet_edges_by_length(insert, 5, d["insertion_length"])
        insert.translate(Base.Vector(-d["t_leg"]/2, -d["insertion_width"]/2, 0))
        insert.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -a)
        insert.translate(p)
        m = m.cut(hole).cut(insert)
        a = a + 90

    m.translate(Base.Vector(0, 0, -d["t_tabletop"]))
    return m

def lower_tabletop(d):
    r3edge = 100
    deltax = 35
    deltay = 35
    delta3 = 30
    x2 = d["ccx"] / 2.0 + 70
    y2 = d["ccy"] / 2.0 + 70
    x0 = x2 - math.sqrt((r3edge**2)/2)
    y0 = y2 - math.sqrt((r3edge**2)/2)
    x1 = x0 + math.sqrt((delta3**2)/2)
    y1 = y0 + math.sqrt((delta3**2)/2)
    x3 = x2 + deltax
    y3 = y2 - deltay

    points = [Base.Vector(-x0, y2,  0),    Base.Vector(  0, y3,  0),
                Base.Vector( x0, y2,  0), Base.Vector( x1, y1,  0),
                Base.Vector( x2, y0,  0), Base.Vector( x3,  0,  0),
                Base.Vector( x2, -y0, 0), Base.Vector( x1, -y1, 0),
                Base.Vector( x0, -y2, 0), Base.Vector(  0, -y3, 0),
                Base.Vector(-x0, -y2, 0), Base.Vector(-x1, -y1, 0),
                Base.Vector(-x2, -y0, 0), Base.Vector(-x3,   0, 0),
                Base.Vector(-x2,  y0, 0), Base.Vector(-x1,  y1, 0),
                Base.Vector(-x0, y2,  0)]

    face = Part.Face(Part.Wire(dc.model.create_arcs(points)))
    m = face.extrude(Base.Vector(0, 0, d["t_tabletop"]))
    m = dc.model.fillet_edges_by_length(m, 20, d["t_tabletop"])

    hx = d["ccx"] / 2.0
    hy = d["ccy"] / 2.0

    hole_points = [ Base.Vector( hx,  hy, 0),
                    Base.Vector(-hx,  hy, 0),
                    Base.Vector(-hx, -hy, 0),
                    Base.Vector( hx, -hy, 0)]

    a = 45
    for p in hole_points:
        hole = Part.makeCylinder(d["hole_dia_tabletop"]/2.0, d["t_tabletop"], p, Base.Vector(0, 0, 1), 360)
        insert = Part.makeBox(d["t_leg"], d["insertion_width_3"], d["insertion_length"])
        insert = dc.model.fillet_edges_by_length(insert, 5, d["insertion_length"])
        insert.translate(Base.Vector(-d["t_leg"]/2, -d["insertion_width_3"]/2, 0))
        insert.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -a)
        insert.translate(p)
        m = m.cut(hole).cut(insert)
        a = a + 90

    m.translate(Base.Vector(0, 0, -d["t_tabletop"]))
    return m

def leg(d):
    x0 = d["insertion_width_1"]
    x2 = 140
    x1 = (x0 + x2) / 2.0 - 12
    x4 = d["cx"] - d["insertion_width_3"] / 2.0
    x3 = (x2 + x4) / 2.0 + 10
    x5 = d["cx"] + (d["insertion_width_2"] - d["insertion_width_3"]) / 2.0
    x7 = d["cx"] + d["insertion_width_3"] / 2.0
    x6 = (x5 + x7) / 2.0 - 10
    x8 = d["cx"] - d["insertion_width_3"] / 2.0
    x9 = x8 - 30
    x11 = 120
    x10 = (x9 + x11) / 2.0 - 5
    x12 = x11 - 60
    x13 = x12 + 12

    y0 = d["height"]
    y1 = d["height"] - d["t_tabletop"]
    y4 = d["height"] - d["t_tabletop"] + d["insertion_length"]
    y3 = y0 - 160
    y2 = (y1 + y3) / 2.0
    y6 = d["height_1"] - d["insertion_length"]
    y5 = (y4 + y6) / 2.0
    y7 = y6 + 10
    y8 = y7 / 2.0
    y9 = y0 - 50

    p = [
        Base.Vector(  0, y0, 0),
        Base.Vector( x0, y0, 0),
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
    m = face.extrude(Base.Vector(0, 0, d["t_leg"]))
    m = dc.model.fillet_edge_xy(m,  7, p[4])
    m = dc.model.fillet_edge_xy(m,  7, p[11])
    m = dc.model.fillet_edge_xy(m, 12, p[12])
    m = dc.model.fillet_edge_xy(m, 120, p[17])
    m.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    m.translate(Base.Vector(0, d["t_leg"] / 2.0, 0))

    hole = Part.makeCylinder(d["hole_dia_leg"] / 2.0, d["height"], Base.Vector(d["cx"], 0, d["height_1"] - d["insertion_length"]), Base.Vector(0, 0, 1), 360)
    m = m.cut(hole)
    return m

def coffetable_assy(d):
    x = d["ccx"] / 2.0 + math.sqrt((d["cx"]**2) / 2.0)
    y = d["ccy"] / 2.0 + math.sqrt((d["cx"]**2) / 2.0)
    # The upper oak tabletop
    #tt1 = tabletop(d)
    #tt1.translate(Base.Vector(0, 0, d["height"]))

    # The lower oak tabletop
    tt2 = lower_tabletop(d)
    tt2.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    tt2.translate(Base.Vector(0, 0, d["height_1"] - d["t_tabletop"]))

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
    #dc.common.add_model(doc, tt1, "upperTableTop")
    dc.common.add_model(doc, tt2, "lowerTableTop")
    dc.common.add_model(doc, leg1, "leg1")
    dc.common.add_model(doc, leg2, "leg2")
    dc.common.add_model(doc, leg3, "leg3")
    dc.common.add_model(doc, leg4, "leg4")

    doc.saveAs(dc.common.fn(d, "assy") + ".fcstd")

def tabletop_drw(d):
    # The oak tabletop
    tt1 = lower_tabletop(d)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, tt1, "tableTop")
    #p = dc.common.add_drawing_page(doc)
    #dc.drawing.create_drawing(doc, p, m, d["tabletop"])
    doc.saveAs(dc.common.fn(d, "tabletop") + ".fcstd")

def leg_drw(d):
    leg1 = leg(d)
    doc = dc.common.create_doc()
    dc.common.add_model(doc, leg1, "leg")
    doc.saveAs(dc.common.fn(d, "leg") + ".fcstd")

d = load_parameters("ct2_designparameters.yml")

coffetable_assy(d)
#tabletop_drw(d)
leg_drw(d)
