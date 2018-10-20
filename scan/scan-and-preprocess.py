#!/usr/bin/env python
import subprocess
import sys
import os
import glob

def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

        
if len(sys.argv) > 3:
    outputpath = sys.argv[1]
    colorstr = sys.argv[2]
    duplexstr = sys.argv[3]
else:
    print "Missing arguments!"
    sys.exit(0)
    
if not (outputpath.endswith('/')):
    outputpath += '/'
ensure_dir(outputpath)
os.chdir(outputpath)

filecount = 0
if os.path.exists(outputpath + 'cntr'):
    with open(outputpath + 'cntr', 'r') as f:
        filecount = int(f.readline())


pdfoutputdir = outputpath + "/pdf/"
ensure_dir(pdfoutputdir)

outputarg = "--batch=\"out%04d.pnm\" --batch-start=" + str(filecount)
devicearg = "-d \"brother4:net1;dev0\""
resolutionarg = "--resolution 300"
sizearg = "-x 208mm -y 295mm"
miscargs = ""

colorarg = "--mode \"24bit Color\""
if colorstr.lower() == "gray":
    colorarg = "--mode \"True Gray\""
    
duplexarg = "--source \"Automatic Document Feeder(centrally aligned)\""
if duplexstr.lower() == "duplex":
    duplexarg = "--source \"Automatic Document Feeder(centrally aligned,Duplex)\""
    
scanimg = ["scanimage", devicearg, outputarg, resolutionarg, sizearg, miscargs, colorarg, duplexarg]

scanimgcmd = ' '.join(scanimg)
print scanimgcmd
subprocess.check_call(scanimgcmd, shell=True)

for filename in glob.iglob(outputpath + "/*.pnm"):
    filecount += 1
    basefilename, x = os.path.splitext(os.path.basename(filename));

    pdfcmd2 = "convert -page A4 " + filename + " " + pdfoutputdir + basefilename + ".pdf"
    subprocess.check_call(pdfcmd2, shell=True)
    os.remove(filename)
    
with open(outputpath + 'cntr', 'w') as f:
    f.truncate()
    f.write(str(filecount))
    f.write('\n')
    

# scanimage check possibilities for SANE scanner:
# scanimage --help --device-name 'brother4:net1;dev0'
# output for brother MFC-9342CDW:

# Options specific to device `brother4:net1;dev0':
  # Mode:
    # --mode Black & White|Gray[Error Diffusion]|True Gray|24bit Color[Fast] [24bit Color[Fast]]
        # Select the scan mode
    # --resolution 100|150|200|300|400|600|1200|2400|4800|9600dpi [200]
        # Sets the resolution of the scanned image.
    # --source FlatBed|Automatic Document Feeder(left aligned)|Automatic Document Feeder(left aligned,Duplex)|Automatic Document Feeder(centrally aligned)|Automatic Document Feeder(centrally aligned,Duplex) [Automatic Document Feeder(left aligned)]
        # Selects the scan source (such as a document-feeder).
    # --brightness -50..50% (in steps of 1) [inactive]
        # Controls the brightness of the acquired image.
    # --contrast -50..50% (in steps of 1) [inactive]
        # Controls the contrast of the acquired image.
  # Geometry:
    # -l 0..215.9mm (in steps of 0.0999908) [0]
        # Top-left x position of scan area.
    # -t 0..355.6mm (in steps of 0.0999908) [0]
        # Top-left y position of scan area.
    # -x 0..215.9mm (in steps of 0.0999908) [215.88]
        # Width of scan-area.
    # -y 0..355.6mm (in steps of 0.0999908) [355.567]
        # Height of scan-area.



