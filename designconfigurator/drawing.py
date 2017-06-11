import datetime
from fractions import Fraction
import sys

sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD, TechDraw
from FreeCAD import Base

import common

def create_drawing(doc, pn, rev, title):
    volume = doc.myModel.Shape.Volume
    density = 0.74e-6 # kg / mm^3
    mass = volume * density
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    scale = 0.2

    page = doc.myPage

    page.Template.setEditFieldContent("AUTHOR_NAME", "Gustav Naslund")
    page.Template.setEditFieldContent("DRAWING_TITLE", title)
    page.Template.setEditFieldContent("SI-1", "")
    page.Template.setEditFieldContent("SI-2", "")
    page.Template.setEditFieldContent("FreeCAD_DRAWING", "")
    page.Template.setEditFieldContent("SI-4", "")
    page.Template.setEditFieldContent("SI-5", "")
    page.Template.setEditFieldContent("SI-6", "Weight: " + "{0:.2f}".format(mass) + " kg")
    page.Template.setEditFieldContent("PN", pn)
    page.Template.setEditFieldContent("DN", "1")
    page.Template.setEditFieldContent("FC-SC", str(Fraction(scale).limit_denominator()).replace("/",":"))
    page.Template.setEditFieldContent("FC-SH", "1/1")
    page.Template.setEditFieldContent("FC-REV", rev)
    page.Template.setEditFieldContent("FC-DATE", date)

    doc.addObject('TechDraw::DrawViewPart','View')
    doc.View.Source = doc.myModel
    doc.View.Direction = (0.0,0.0,1.0)
    doc.View.Scale = 1.0
    doc.View.Rotation = 0.0
    page.addView(doc.View)
    page.Scale = scale

    doc.recompute()
