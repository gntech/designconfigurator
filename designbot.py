#!/usr/bin/env python2

import os
import sys

import designconfigurator as dc

def build_design(user_parameters):
    if user_parameters["design"] == "ct1":
        d = dc.ct1_defaults
        d.update(user_parameters)
        dc.ct1.build_all(d)

    elif user_parameters["design"] == "ct2":
        d = dc.ct2_defaults
        d.update(user_parameters)
        dc.ct2.build_all(d)

    else:
        print("Unrecognized design: " + user_parameters["design"])

user_parameters = sys.argv[1]
d = dc.common.load_parameters(user_parameters)
d["outfolder"] = os.path.dirname(os.path.abspath(sys.argv[1]))
build_design(d)
