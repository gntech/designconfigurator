import datetime
import os
import sys

sys.path.append("/usr/lib/freecad-daily/lib") # change this by your own FreeCAD lib path import FreeCAD
import FreeCAD, TechDraw
from FreeCAD import Base
import yaml

def load_parameters(fn):
    with open(fn, "r") as f:
        d = yaml.load(f)
    return d

def fn(d, part=""):
    #fnparts = [d[part]["nr"],
    #            d[part]["rev"],
    #            d[part]["name"],

    fnparts = [d["project"].replace(" ", "-"),
                part,
                datetime.datetime.now().strftime("%Y-%m-%d")]

    return os.path.join(d["outfolder"], "_".join(fnparts))

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

def writeinfo(d):
    pass
