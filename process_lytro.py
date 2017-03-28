import subprocess
import math
import shlex
import sys
import os
import shutil

'''
cmd = 'lfptool raw -i IMG_0487.LFR --image-out --imagerep png  -P 6 --focus '
'''
def getfilenames(output):
    s = output.split('\r\n')
    inputfile = s[-3].split(":")[-1].strip()
    outputfile = s[-2].split(":")[-1].strip()
    return inputfile, outputfile


def getnewfilename(index, filename, output_dir):
    basename = os.path.basename(filename)
    start = basename[0:8]
    ext = filename.split(".")[-1].strip()
    name = start + "-" + str(index).zfill(3)
    return output_dir + name + "." + ext


def lfptoolcommand(cmdlist, output_dir):
    index = 0
    for com in cmdlist:
        args = shlex.split(com)
        x = subprocess.Popen(args, stdout=subprocess.PIPE)
        out = x.stdout.read()
        inputfile, outputfile = getfilenames(out)
        newfilename = getnewfilename(index, outputfile, output_dir)
        shutil.move(outputfile, newfilename)
        index += 1

        print index, outputfile, newfilename

def makecommand(imagename):
    cmd = 'lfptool raw -i '
    cmd += imagename
    cmd += ' --image-out --imagerep png  -P 6 --focus '
    return cmd

def makecmdlist(cmd, fstart, fstop, df):
    cmdlist = list()
    f = fstart
    while f < fstop:
        if abs(f) < .001:
            f = 0.0
        fstr = str(f)
        a = cmd + fstr
        cmdlist.append(a)
        f += df

    return cmdlist

if __name__ == '__main__':
    a = sys.argv
    inputimage = a[1]
    output_dir = a[2]
    start = float(a[3])
    stop = float(a[4])
    df = float(a[5])

    slash = os.sep;
    if output_dir[-1] != slash:
        output_dir += slash

    print a
    print output_dir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    cmd = makecommand(inputimage)
    cmdlist = makecmdlist(cmd, start, stop, df)
    lfptoolcommand(cmdlist, output_dir)


# inputimage = "/Users/cjw/Desktop/IMG_0487.LFR"
# output_dir = "/Users/cjw/Desktop/lpout/"
# if not os.path.exists(output_dir):
#     os.mkdir(output_dir)
#
# cmd = makecommand("/Users/cjw/Desktop/IMG_0487.LFR")
# cmdlist = makecmdlist(cmd, -1, 2, 1)
# lfptoolcommand(cmdlist, output_dir)



