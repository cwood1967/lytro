import subprocess
import math
import shlex
import sys
import os
import shutil
import time

def get_lytro_files(inputdir):

    if inputdir[-1] != os.sep or inputdir[-1] != "/":
        inputdir += os.sep

    files = os.listdir(inputdir)
    files = [f for f in files if f.endswith(".LFR")]
    files = [inputdir + file for file in files]
    return sorted(files)


def update_recipe_file(recipe_file, aperture):
## recipetool view --aperture .1 --focus 0 --defringe --defringe-threshold 10 -i ../Recipes/recipe.json
    cmd = "recipetool view --aperture {:.4f} -i {}".format(aperture, recipe_file)
    args = shlex.split(cmd)
    x = subprocess.call(args)
    print(cmd)
    print(args)
    print(x)

def topng(file, dirout, recipe):
    cmd = 'lfptool raw -i "{}" --image-out --imagerep png --dir-out "{}" --recipe-in={} -P 4 --threads 8'.format(
        file, dirout, recipe)
    args = shlex.split(cmd)
    # print(cmd)
    # print(args)
    x = subprocess.Popen(args, shell=False, stdin=None, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return x

def make_output_path(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            return None
    else:
        os.makedirs(path)
        return path

def pollsubs(subs):
    if subs is None:
        return 0
    for p in subs:

        if p.poll() is not None:
            subs.remove(p)
            print("removed", p.args)

    return len(subs)


def batch(files, output_path, recipe):

    num = 6
    # print(files)
    i = 0
    running = list()

    for f in files:
        print(f)
        if pollsubs(running) < num:
            running.append(topng(f, output_path, recipe))
            print("continuing")
        else:
            while pollsubs(running) >= num:
                time.sleep(1)
            running.append(topng(f, output_path, recipe))
        i += 1
        if i > 20:
            break
        print(i)
        time.sleep(2)

    while pollsubs(running) > 0:
        time.sleep(1)

dir = "/Volumes/projects/jjl/public/Chris Arnold/3 camera timelapse/03232017/lytro"
output_path = make_output_path("/Users/cjw/Desktop/Worm323-3")

files = get_lytro_files(dir)

recipe_file = "/Users/cjw/Desktop/Recipes/recipetest.json"
update_recipe_file(recipe_file, 1./16)
#topng(files[0], output_path, recipe_file)
batch(files, output_path, recipe_file)
