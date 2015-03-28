from distutils.core import setup

setup(name='gitwhoosh',
        version='0.2',
        description='git repository indexer using whoosh',
        py_modules = ['gitwhoosh'],
        requires = ['dulwich', 'whoosh', 'simplejson']
        )
