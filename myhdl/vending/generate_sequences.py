
import os
import argparse
import csv
from random import randint

import vending_models as vm


parser = argparse.ArgumentParser()
parser.add_argument("filename", default="sequences",
                    help="filename to save seqeuences in")
parser.add_argument("--nseq", default=1, type=int,
                   help="the number of seqeunces to generate")
args = parser.parse_args()

fn,ext = os.path.splitext(args.filename)

validfn = args.filename+'_valid.csv'
invalidfn = args.filename+'_invalid.csv'

# generate the valid sequences
with open(validfn, 'wb') as csvfile:
    cw = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for ii in xrange(args.nseq):
        vend = vm.Vend(vm.Sequence(randint(1,4), valid=True))
        for bb,ll,ts in vend:
            cw.writerow([bb,"%02X"%(ll),vend.total,ts])
    cw.writerow([])

# generate the invalid sequences
with open(invalidfn, 'wb') as csvfile:
    cw = csv.writer(csvfile, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for ii in xrange(args.nseq):
        vend = vm.Vend(vm.Sequence(randint(1,4), valid=True))
        for bb,ll,ts in vend:
            cw.writerow([bb,"%02X"%(ll),vend.total,ts])
    cw.writerow([])

