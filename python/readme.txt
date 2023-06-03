To use the Stella python diagnostics module, your python installations must find
it. The easiest way to achieve this, is setting the PYTHONPATH environment
variable to include this directory. For bash-like shells, this may be done by

export PYTHONPATH=/path/to/this/directory/

or by 

export PYTHONPATH=/path/to/this/directory/:$PYTHONPATH

if this environment variable is already set and its current content should be
retained.

After making the stella diagnostics module available it may be imported by
(inside a python script or within a python interpreter shell)

import stella.name-of-submodule

The following submodules are currently available

stella
  eve.py
  lbol.py
  ph.py
  res.py
  snia.py
  swdn.py
  tt.py
  stella.py

Use the following command to import them all at once

from stella import *

The stella_reader in the stella.py module tries to load all files for a specific
run (for which python readers exist)
