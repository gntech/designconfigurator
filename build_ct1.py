#!/usr/bin/env python2

import math
import sys
import yaml
sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD
from FreeCAD import Base

import designconfigurator as dc

def load_parameters(fn):
    parameters = {
        "project": "Undefined",
        "assy":     {"nr": "aaaaaa-aaa", "name": "Assy", "rev": "A"},
        "tabletop": {"nr": "bbbbbb-bbb", "name": "Tabletop", "rev": "A"},
        "leg":      {"nr": "cccccc-ccc", "name": "Leg", "rev": "A"},
        "length": 1000,
        "width": 700,
        "height": 500,
        "height_1": 340,
        "height_1": 140,
        "t_tabletop": 18,
        "t_leg": 36,
        "t_glass": 8,
        "insertion_width": 50,
        "insertion_length": 3,
        "hole_dia_tabletop": 9,
        "hole_dia_leg": 8,
        "cx": 200
    }

    with open(fn, "r") as f:
        user_parameters = yaml.load(f)

    parameters.update(user_parameters)
    return parameters

def glasstop(d, dressup=True):
    m = Part.makeBox(d["length"], d["width"], d["t_glass"])
    m.translate(Base.Vector(-d["length"]/2, -d["width"]/2, -d["t_glass"]))

    if dressup:
        m = dc.model.chamfer_edges_longer_than(m, 2, 100)

    return m

def tabletop(d, dressup=True):
    r3edge = 100
    deltax = 35
    deltay = 35
    delta3 = 30
    x2 = (d["length"] - 140) / 2.0
    y2 = (d["width"] - 140) / 2.0
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

    hx = d["length"] / 2.0 - math.sqrt((d["cx"]**2) / 2.0)
    hy = d["width"] / 2.0 - math.sqrt((d["cx"]**2) / 2.0)

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

    if dressup:
        m = dc.model.fillet_edges_longer_than(m, 7, 300)

    m.translate(Base.Vector(0, 0, -d["t_tabletop"]))
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
    y2 = d["height_1"] - d["t_tabletop"] + d["insertion_length"]
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
    m = face.extrude(Base.Vector(0, 0, d["t_leg"]))

    m = dc.model.fillet_edge_xy(m, 100, p[3])
    m = dc.model.fillet_edge_xy(m, 20, p[7])
    m = dc.model.fillet_edge_xy(m, 8, p[8])
    m = dc.model.fillet_edge_xy(m, 8, p[16])
    m = dc.model.fillet_edge_xy(m, 20, p[17])

    m.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    m.translate(Base.Vector(-corner_protection, d["t_leg"]/2, 0))

    hole = Part.makeCylinder(d["hole_dia_leg"] / 2.0, d["height"], Base.Vector(d["cx"], 0, 0), Base.Vector(0, 0, 1), 360)
    m = m.cut(hole)
    corner_cutout = Part.makeBox(2*d["t_leg"], 2*d["t_leg"], d["t_glass"])
    corner_cutout.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -45)
    corner_cutout.translate(Base.Vector(0, 0, d["height"] - d["t_glass"]))
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
    tt2.translate(Base.Vector(0, 0, d["height_2"] - d["t_tabletop"]))

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

d = load_parameters("ct1_designparameters.yml")

coffetable_assy(d)
glasstop_drw(d)
tabletop_drw(d)
leg_drw(d)