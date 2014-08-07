This repository contains various python utilities designed to help
facilitate running builds on a developer machine.   Currently the
scripts that provide build services for developers to build the iOS
Kernel SDK rely on this module.

The module is intended to be cloned and used as follows:

From your home directory:

mkdir python

cd python

git clone ssh://git@stash.wolfram.com:7999/misc/slib.git

Then in your python scripts:

import sys

sys.path.append(os.environ['HOME'] + os.path.sep + "python")

import slib
# etc...

This package could of course be set up to install using the Python setup.py
mechanism.

