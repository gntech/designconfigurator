import datetime
import sys
sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD, TechDraw
from FreeCAD import Base

def fn(d, part=""):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    fnparts = [d[part]["nr"],
                d[part]["rev"],
                d["project"].replace(" ", "-"),
                d[part]["name"],
                date]
    return "_".join(fnparts)

def create_doc():
    doc = FreeCAD.newDocument()
    return doc

def add_model(doc, m, name):
    part = doc.addObject("Part::Feature", name)
    part.Shape = m
    return part

def add_drawing_page(doc):
    page = doc.addObject('TechDraw::DrawPage','myPage')
    doc.addObject('TechDraw::DrawSVGTemplate','Template')
    doc.Template.Template = '/usr/share/freecad-daily/Mod/TechDraw/Templates/A3_Landscape_ISO7200TD.svg'
    doc.myPage.Template = doc.Template
    return page
