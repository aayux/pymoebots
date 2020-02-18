""" Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

Modifications:

1) Uncommented import os, import sys, sys.path.insert(0, os.path.abspath('../../'))

2) added extensions - 'sphinx.ext.autodoc'

3) added add_module_names = False

4) set up django documentation
    * import django - imports django module
    * sys.path.append(os.path.abspath('../')) - makes the django root director a path to use for os.eviron.setdefault.
      Use this command if your sphinx config file is not pointed directly to the root of the django project.
    * os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hashthat.settings") - makes the setting file in your django app
      the default setting files for the django module. If this part is causing errors when using make settings saying
      that your django app is not a module and you are sure you are spelling it right, then the problem is that sys.path
      is not storing your django root folder and it needs to be appended to it.
    * django.setup() - setup sphinx with the django environment so it can document your django project successful.
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import django
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))
sys.path.append(os.path.abspath('../research'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "research_projects.settings")
django.setup()


# -- Project information -----------------------------------------------------

project = 'Bot Algorithms'
copyright = '2020, Jesse Thomas'
author = 'Jesse Thomas'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False
