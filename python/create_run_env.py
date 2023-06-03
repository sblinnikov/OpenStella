#!/usr/bin/env python
# A helper to create a standalone directory tree for running a Stella model
# Current version is still undocumented
from __future__ import print_function
import os
import argparse
import shutil

copy_list = ["eve_exe", "eve_config", "eve_file", "opacity_exe", "opacity_config", "stella_exe", "stella_config", "stella_dat", "zone.inc", "opacity.inc", "info.txt"]
link_list = ["opacity_helper_dir", "linelist", "modmake"]

opacitydestpath = "vladsf"
evedestpath = "eve/run"
straddestpath = "strad/run"
objdestpath = "obj"


def make_copy_dict(evepath, vladsfpath, stradpath, objpath, eve_exe = "eve1a.exe", eve_file = "toya1.eve", opacity_exe = "xronfict.exe", strad_exe = "xstella7BQeps.exe", strad_file = "m030307mh.dat"):

    eve_config = "eve.1.sample"
    opacity_config = "ronfict.1"
    strad_config = "strad.1"



    copy_dict = dict([
            ("eve_exe", [evepath + eve_exe, evedestpath]),
            ("eve_config", [evepath + eve_config, os.path.join(evedestpath, "eve.1")]),
            ("eve_file", [evepath + eve_file, evedestpath]),
            ("opacity_exe", [vladsfpath + opacity_exe, opacitydestpath]),
            ("opacity_config", [vladsfpath + opacity_config, opacitydestpath]),
            ("stella_exe", [stradpath + strad_exe, straddestpath]),
            ("stella_config", [stradpath + strad_config, os.path.join(straddestpath, "strad.1")]),
            ("stella_dat", [stradpath + strad_file, straddestpath]),
            ("zone.inc", [objpath + "zone.inc", objdestpath]),
            ("opacity.inc", [objpath + "opacity.inc", objdestpath]),
            ("info.txt", ["./info_mask.txt", "info.txt"])
            ])

    return copy_dict

def make_link_dict(vladsfpath, modmakepath):

    linelist = "linedata.dump"

    link_dict = dict([
        ("opacity_helper_dir", [vladsfpath + "yakovlev", opacitydestpath]),
        ("linelist", [vladsfpath + linelist, opacitydestpath]),
        ("modmake", [modmakepath, None]),
        ])

    return link_dict

def cleanup(dirname):

    print("Cleaning up:")
    for root, dirs, files in os.walk(dirname, topdown = False, followlinks = False):
        for name in files:
            print("removing file '%s'" % os.path.join(root, name))
            #os.remove(os.path.join(root, name))
        for name in dirs:
            print("removing directory '%s'" % os.path.join(root, name))
            #os.remdir(os.path.join(root, name))
    print("removing directory '%s'" % dirname)
    os.rmdir(dirname)


def main(dirname, eve_exe = "eve1a.exe", opacity_exe = "xronfict.exe", stella_exe = "xstella7BQeps.exe", eve_file = "toya1.eve", strad_file = "m030307mh.dat"):

    evepath = None
    vladsfpath = None
    stradpath = None
    objpath = None
    modmakepath = None

    if os.path.exists(dirname):
        print("Warning: '%s' already exists; aborting" % dirname)
        return False


    os.mkdir(dirname)
    os.mkdir(os.path.join(dirname, "vladsf"))
    os.mkdir(os.path.join(dirname, "res"))
    os.mkdir(os.path.join(dirname, "obj"))
    os.makedirs(os.path.join(dirname, "strad/run"))
    os.makedirs(os.path.join(dirname, "eve/run"))

    curdir = os.getcwd()
    pathelems = curdir.rsplit("/")

    for i in xrange(len(pathelems), 1, -1):
        path = "/".join(pathelems[:i])

        dirs = os.listdir(path)

        if "eve" in dirs:
            evepath = path + "/eve/run/"

        if "vladsf" in dirs:
            vladsfpath = path + "/vladsf/"

        if "strad" in dirs:
            stradpath = path + "/strad/run/"

        if "obj" in dirs:
            objpath = path + "/obj/"

        if "modmake" in dirs:
            modmakepath = path + "/modmake/"

        if evepath is not None and vladsfpath is not None and stradpath is not None and objpath is not None and modmakepath is not None:
            break

    if evepath is None:
        print("Warning: could not find eve directory; aborting")
        cleanup(dirname)
        return False

    if vladsfpath is None:
        print("Warning: could not find vladsf directory; aborting")
        cleanup(dirname)
        return False

    if stradpath is None:
        print("Warning: could not find strad directory; aborting")
        cleanup(dirname)
        return False

    if not os.path.exists(evepath):
        print("Warning: default eve directory '%s' does not exist" % evedir)
        cleanup(dirname)
        return False

    copy_dict = make_copy_dict(evepath, vladsfpath, stradpath, objpath, eve_exe = eve_exe, opacity_exe = opacity_exe, strad_exe = stella_exe, eve_file = eve_file, strad_file = strad_file)

    link_dict = make_link_dict(vladsfpath, modmakepath)


    for copy_ident in copy_list:
        try:
            src, dest = copy_dict[copy_ident]
            if dest is None:
                dest = dirname
            else:
                dest = os.path.join(dirname, dest)
            try:
                shutil.copy2(src, dest)
            except IOError:
                print("Warning: file '%s' not found; aborting" % src)
                cleanup(dirname)
                return False
        except KeyError:
            print("Warning: incomplete copy_dict, no entry for key '%s'; aborting" % copy_ident)
            return False

    for link_ident in link_list:
        try:
            src, dest = link_dict[link_ident]
            if dest is None:
                dest = dirname + "/"
            else:
                dest = os.path.join(dirname,dest)
            try:
                os.system("ln -r -s %s %s" % (src, dest))
            except IOError:
                print("Warning: file '%s' not found; aborting" % src)
                cleanup(dirname)
                return False
        except KeyError:
            print("Warning: incomplete link_dict, no entry for key '%s'; aborting" % link_ident)
            return False




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create self-contained run environment for Stella")
    parser.add_argument("dirname", help="Name of directory")
    parser.add_argument("--eve", help="Name of eve executable", default= "eve1a.exe")
    parser.add_argument("--opacity", help="Name of opacity table executable", default="xronfict.exe")
    parser.add_argument("--stella", help="Name of stella executable", default="xstella7BQeps.exe")
    parser.add_argument("--evefile", help="Name of .eve file", default = "toya1.eve")
    parser.add_argument("--stellafile", help="Name of .dat file", default = "m030307mh.dat")
    args = parser.parse_args()

    main(args.dirname, eve_exe = args.eve, opacity_exe = args.opacity, stella_exe = args.stella, eve_file = args.evefile, strad_file = args.stellafile)


