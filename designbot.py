#!/usr/bin/env python2

import os
import sys

import designconfigurator as dc

def build_design(user_parameters):
    if user_parameters["design"] == "ct1":
        dc.ct1.build_all(user_parameters)

    elif user_parameters["design"] == "ct2":
        dc.ct2.build_all(user_parameters)

    else:
        print("Unrecognized design: " + user_parameters["design"])

user_parameters = sys.argv[1]
d = dc.common.load_parameters(user_parameters)
d["outfolder"] = os.path.dirname(os.path.abspath(sys.argv[1]))
build_design(d)
