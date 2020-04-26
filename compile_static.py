#!/usr/bin/env python
import os
import tempfile
from shutil import copyfile, rmtree

import coffeescript
import scss

from mediacrush.app import app
from mediacrush.config import _cfg, _cfgi

app.static_folder = os.path.join(os.getcwd(), "static")
scss.config.LOAD_PATHS = [os.path.join(os.getcwd(), "styles")]


def prepare():
    path = tempfile.mkdtemp()

    compiler = scss.Scss(scss_opts={"style": "compressed" if not app.debug else None})

    # Unsafe extnsion function used only here
    extension = lambda f: f.rsplit(".", 1)[1].lower()

    # Compile styles (scss)
    d = os.walk("styles")
    for f in list(d)[0][2]:
        if extension(f) == "scss":
            print(("[scss] %s" % f))

            with open(os.path.join("styles", f)) as r:
                output = compiler.compile(r.read())

            parts = f.rsplit(".")
            css = ".".join(parts[:-1]) + ".css"

            with open(os.path.join(path, css), "w") as w:
                w.write(output)
                w.flush()

    # Compile scripts (coffeescript)
    d = os.walk("scripts")
    preprocess = ["scripts/mediacrush.js"]
    for f in list(d)[0][2]:
        outputpath = os.path.join(path, os.path.basename(f))
        inputpath = os.path.join("scripts", f)

        if extension(f) == "js":
            if inputpath in preprocess:
                with open(inputpath) as r:
                    output = r.read()
                    output = output.replace("{{ protocol }}", _cfg("protocol"))
                    output = output.replace("{{ domain }}", _cfg("domain"))

                with open(outputpath, "w") as w:
                    w.write(output)
                    w.flush()
            else:
                copyfile(inputpath, outputpath)

        elif extension(f) == "manifest":
            with open(inputpath) as r:
                manifest = r.read().split("\n")

            javascript = ""
            for script in manifest:
                script = script.strip(" ")

                if script == "" or script.startswith("#"):
                    continue

                bare = False
                if script.startswith("bare: "):
                    bare = True
                    script = script[6:]

                print(("[coffee] %s" % script))
                with open(os.path.join("scripts", script)) as r:
                    coffee = r.read()
                    if script.endswith(".js"):
                        javascript += coffee  # straight up copy
                    else:
                        javascript += coffeescript.compile(coffee, bare=bare)
            output = ".".join(f.rsplit(".")[:-1]) + ".js"

            with open(os.path.join(path, output), "w") as w:
                w.write(javascript)
                w.flush()

    if os.path.exists(app.static_folder):
        rmtree(app.static_folder)
    os.makedirs(app.static_folder)

    d = os.walk(path)
    for f in list(d)[0][2]:
        inputpath = os.path.join(path, os.path.basename(f))
        outputpath = os.path.join(app.static_folder, f)
        copyfile(inputpath, outputpath)

    d = os.walk("images")
    for f in list(d)[0][2]:
        outputpath = os.path.join(app.static_folder, os.path.basename(f))
        inputpath = os.path.join("images", f)
        copyfile(inputpath, outputpath)


if __name__ == "__main__":
    prepare()
