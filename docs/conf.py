extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'lazy-object-proxy'
year = '2014-2024'
author = 'Ionel Cristian Mărieș'
copyright = f'{year}, {author}'
try:
    from pkg_resources import get_distribution

    version = release = get_distribution('lazy_object_proxy').version
except Exception:
    import traceback

    traceback.print_exc()
    version = release = '1.11.0'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/ionelmc/python-lazy-object-proxy/issues/%s', '#%s'),
    'pr': ('https://github.com/ionelmc/python-lazy-object-proxy/pull/%s', 'PR #%s'),
}

html_theme = 'furo'
html_theme_options = {
    'githuburl': 'https://github.com/ionelmc/python-lazy-object-proxy/',
}

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_short_title = f'{project}-{version}'

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
