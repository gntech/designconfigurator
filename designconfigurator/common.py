import datetime
import sys
sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD

import FreeCAD, TechDraw
from FreeCAD import Base

def fn(d):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return "_" + d["project_nr"] + "_" + d["rev"] + "_" + d["project"].replace(" ", "-") + "_" + date

def create_doc():
    doc = FreeCAD.newDocument()
    return doc

def add_model(doc, m, name):
    part = doc.addObject("Part::Feature", name)
    part.Shape = m

def add_drawing_page(doc):
    page = doc.addObject('TechDraw::DrawPage','myPage')
    doc.addObject('TechDraw::DrawSVGTemplate','Template')
    doc.Template.Template = '/usr/share/freecad-daily/Mod/TechDraw/Templates/A3_Landscape_ISO7200TD.svg'
    doc.myPage.Template = doc.Template
