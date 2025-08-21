# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information



import sphinx_rtd_theme
import sphinx_fontawesome
import os
import sys
from sphinx.roles import MenuSelection
from docutils import nodes
from docutils.parsers.rst import roles

sys.path.insert(0, os.path.abspath('..'))
#sys.path.insert(0, os.path.abspath('../nv200'))

def styled_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    # Create a span element with a custom CSS class
    node = nodes.inline(text, text, classes=[name])
    return [node], []

def setup(app):
    roles.register_local_role('guinum', styled_role)
    # Or app.add_role('highlight', styled_role) if you want it globally


# -- Project information -----------------------------------------------------
project = 'PySoWorks'
copyright = '2025, piezosystem Jena'
author = 'piezosystem Jena'
release = '1.0.0'
html_show_copyright = True
html_show_sphinx = True
html_show_sourcelink = False


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
   'sphinx_rtd_dark_mode',
   'sphinx_fontawesome',
   'sphinx_togglebutton',
   'sphinx.ext.autosectionlabel', 
   'sphinx.ext.napoleon',
   "rst2pdf.pdfbuilder"
]

# user starts in, light mode
default_dark_mode = False

add_module_names = False
autodoc_class_signature = 'separated'
toc_object_entries_show_parents = "hide"
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autosummary_generate = True  # Turn on sphinx.ext.autosummary


napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True


# Set a bullet character for :menuselection: role
# easier to identify in non latin languages, e.g. japanese
from sphinx.roles import MenuSelection
#MenuSelection.BULLET_CHARACTER = '\u25BA' #'\N{BLACK RIGHT-POINTING POINTER}'
MenuSelection.BULLET_CHARACTER = '\u2192' #'\N{	rightwards arrow}'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html#theme-options
# rtd / read the docs theme options:
html_theme_options = {
    # collapse_navigation: With this enabled, navigation entries are not expandable – the [+] icons next to each entry are removed. Default: True
    'collapse_navigation': True,
    # sticky_navigation: Scroll the navigation with the main page content as you scroll the page. Default: True
    'sticky_navigation': True,
    # navigation_depth: The maximum depth of the table of contents tree. Set this to -1 to allow unlimited depth. Default: 4
    'navigation_depth': 4,
    # includehidden:Specifies if the navigation includes hidden table(s) of contents – that is, any toctree directive that is marked with the :hidden: option. Default: True,
    # 'includehidden': True,
    # canonical_url: This will specify a canonical URL meta link element to tell search engines which URL should be ranked as the primary URL for your documentation. This is important if you have multiple URLs that your documentation is available through. The URL points to the root path of the documentation and requires a trailing slash.
    #'canonical_url': 'https://docs.qgis.org/latest/en/',
    # display_version: If True, the version number is shown at the top of the sidebar. Default: True,
    #'display_version': True,
    # logo_only: Only display the logo image, do not display the project name at the top of the sidebar. Default: False,
    'logo_only': False,
    # prev_next_buttons_location': Location to display Next and Previous buttons. This can be either bottom, top, both , or None. Default: 'bottom',
    'prev_next_buttons_location': 'bottom',
    # style_external_links': Add an icon next to external links. Default: False,
    'style_external_links': False,
    # style_nav_header_background': Changes the background of the search area in the navigation bar. The value can be anything valid in a CSS background property. Default: 'white',
    # 'style_nav_header_background': 'Gray',
    # Toc options
    # titles_only: When enabled, page subheadings are not included in the navigation. Default: False
    # 'titles_only': False,
    #'style_nav_header_background': '#ff0000'
}


# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['./themes']



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'style_override_css/style_override.css',
    'style_override_css/color_roles.css',
]

html_favicon = '_static/favicon.png'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/piezosystem_logo_white.svg'
html_title = 'PySoWorks'
html_last_updated_fmt = '%b %d, %Y %H:%M'
html_show_sphinx = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'monokai'

# The name of a reST role to use as the default role, that is, for text marked
# up `like this`. The default role can always be set within individual
# documents using the standard reST default-role directive.
default_role = 'any'

# The default language to highlight source code.
highlight_language = 'python'

source_suffix = ['.rst', '.md']

suppress_warnings = ['autosectionlabel.*']

