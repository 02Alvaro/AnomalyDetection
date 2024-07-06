import os
import sys


sys.path.insert(0, os.path.abspath('../anomalyDetection/src'))

project = 'AnomalyDetection'
copyright = '2024, Álvaro'
author = 'Álvaro'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
