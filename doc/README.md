pip install sphinx
pip install sphinx_rtd_theme

sphinx-quickstart

conf.py
```
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

#
extensions = ['sphinx.ext.autodoc']

#
html_theme = 'sphinx_rtd_theme' #'alabaster'

```

index.rst
```
.. automodule:: auto_video_maker
   :members:
   
.. toctree::
   :maxdepth: 3
   :caption: Contents:
   
   modules
```

sphinx-apidoc -o source/ ../src/auto_video_maker

You should now populate your master file /home/fernando/Proyectos/PROGRAMACION/GITHUB/AUTO-VIDEO-MAKER/auto-video-maker/doc/source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.

