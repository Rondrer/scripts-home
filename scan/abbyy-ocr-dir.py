#!/usr/bin/env python
import subprocess
import sys
import os
import glob

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

f = open(os.path.dirname(os.path.realpath(__file__)) + '/abbyyocr.license', 'r')
license = f.readline()

subprocess.call("abbyyocr11 --viewLicenseParameters " + license, shell=True)

if len(sys.argv) > 2:
    inputpath = sys.argv[1]
    outputpath = sys.argv[2]
else:
    print "No path given!"
    sys.exit(0)

resultpath = outputpath + "/output/"
xmloutputpath = outputpath + "/xml/"
archivepath = outputpath + "/archive/"

ensure_dir(resultpath)
ensure_dir(xmloutputpath)
ensure_dir(archivepath)

for filename in glob.iglob(inputpath + "/*.pdf"):
    basename = os.path.basename(filename)
    subprocess.call("cp -v " + filename + " " + archivepath, shell=True)
    cmd = "abbyyocr11 -if " + filename + " -ido -rl German English -f PDF -of " + resultpath + basename + " -pfv Version17 -pjq 80"
    print cmd
    subprocess.call(cmd, shell=True)
    cmd = "abbyyocr11 -if " + filename + " -ido -rl German English -f XML -of " + xmloutputpath + basename + ".xml"
    print cmd
    subprocess.call(cmd, shell=True)
    subprocess.call("rm -v " + filename, shell=True) 



