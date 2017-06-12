#!/usr/bin/env python2

import math
import sys
import yaml
sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD
from FreeCAD import Base

import designconfigurator as dc
import coffetabledesign as design

def coffetable_assy(d):
    # The glass tabletop
    gt1 = design.glasstop(d)
    gt1.translate(Base.Vector(0, 0, d["height"]))

    # The upper oak tabletop
    tt1 = design.tabletop(d)
    tt1.translate(Base.Vector(0, 0, d["height_1"]))

    # The lower oak tabletop
    tt2 = design.tabletop(d)
    tt2.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 180)
    tt2.translate(Base.Vector(0, 0, d["height_2"] - d["t_tabletop"]))

    # The first leg
    leg1 = design.leg(d)
    leg1.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 225)
    leg1.translate(Base.Vector( d["length"] / 2, d["width"] / 2, 0))

    # The second leg
    leg2 = design.leg(d)
    leg2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 315)
    leg2.translate(Base.Vector(-d["length"] / 2, d["width"] / 2, 0))

    # The third leg
    leg3 = design.leg(d)
    leg3.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 45)
    leg3.translate(Base.Vector(-d["length"] / 2, -d["width"] / 2, 0))

    # The fourth leg
    leg4 = design.leg(d)
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
    gt1 = design.glasstop(d)
    doc = dc.common.create_doc()
    dc.common.add_model(doc, gt1, "glassTop")
    doc.saveAs(dc.common.fn(d, "glasstop") + ".fcstd")

def tabletop_drw(d):
    # The oak tabletop
    tt1 = design.tabletop(d)
    doc = dc.common.create_doc()
    m = dc.common.add_model(doc, tt1, "tableTop")
    p = dc.common.add_drawing_page(doc)
    dc.drawing.create_drawing(doc, p, m, d["tabletop"])
    doc.saveAs(dc.common.fn(d, "tabletop") + ".fcstd")

def leg_drw(d):
    leg1 = design.leg(d)
    doc = dc.common.create_doc()
    dc.common.add_model(doc, leg1, "leg")
    doc.saveAs(dc.common.fn(d, "leg") + ".fcstd")

with open("designparameters.yml", "r") as f:
    d = yaml.load(f)

coffetable_assy(d)
glasstop_drw(d)
tabletop_drw(d)
leg_drw(d)
