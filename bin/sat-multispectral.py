#!/usr/bin/env python

import os
import argparse
from satmultispectral import Scene

'''
    Basic command line parser for processing
'''

if __name__ == '__main__':
    dhf = argparse.ArgumentDefaultsHelpFormatter

    parser = argparse.ArgumentParser(description='Multispectral processing', formatter_class=dhf)
    parser.add_argument('sceneids', help='Scene IDs to process')
    parser.add_argument('--indir', help='Input Directory', default='./')
    parser.add_argument('--outdir', help='Output Directory', defalt='./')
    Scene.add_product_parser(parser)

    args = parser.parse_args()

    print args

    for sid in args.sceneids:
        fname = os.path.join(args.indir, sid)
        scene = Scene(fname)
