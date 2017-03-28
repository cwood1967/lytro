import subprocess
import math
import shlex
import sys
import os
import shutil

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
    print(cmd)
    print(args)
    x = subprocess.call(args)

def make_output_path(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            return None
    else:
        os.makedirs(path)
        return path

def batch(files, output_path, recipe):
    print files
    i = 0
    for f in files:
        print f
        topng(f, output_path, recipe)
        i += 1
        if i > 10:
            break

dir = "/Volumes/projects/jjl/public/Chris Arnold/3 camera timelapse/03232017/lytro"
output_path = make_output_path("/Users/cjw/Desktop/Worm323")

files = get_lytro_files(dir)

print(files)
recipe_file = "/Users/cjw/Desktop/Recipes/recipetest.json"
update_recipe_file(recipe_file, 1./16)
#topng(files[0], output_path, recipe_file)
batch(files, output_path, recipe_file)