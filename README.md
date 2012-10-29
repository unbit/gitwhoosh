GitWhoosh
=========

A git repository indexer (using whoosh as the search engine)

GitWhoosh allows you to index in a whoosh database (a fulltext search engine) your git repositories.

The GitWhoosh class exports two main methods: index() and search()

The first one will index the content of your git repository, while the second one will query
the whoosh database.

The following snippet will index all of the restructuredtext files in your tree

```python
from gitwhoosh import GitWhoosh

gw = GitWhoosh('path_of_your_repository', '/tmp/indexes')
gw.index('\.rst$')
```

while the following one will reports all of the items containing the word FOO or the word BAR

```python
from gitwhoosh import GitWhoosh

gw = GitWhoosh('path_of_your_repository', '/tmp/indexes')
print gw.search('FOO OR BAR')
```

GitWhoosh instances are valid WSGI apps too:

```python
from gitwhoosh import GitWhoosh
application = GitWhoosh('path_of_your_repository', '/tmp/indexes')
```

save it as foo.py and run with your WSGI server of choice.

For example in uWSGI

```
uwsgi --http-socket :9090 --wsgi-file foo.py
```

Now just pass the query as the QUERY_STRING of your request:

```
http://localhost:9090/?optimize%20AND%20foobar
```

... will return a JSON of the search result for "optimize AND foobar".

The JSON is a list of objects, where 'path' is the path of the git object and 'terms' is a list of matching terms:

```json
[{"path": "plugins/cgi/cgi_plugin.c", "terms": ["foobar", "optimize"]}, {"path": "plugins/python/python_plugin.c", "terms": ["foobar", "optimize"]}]
```

Periodically running the indexer
================================

Obviously you need to reindex your repository whenever it changes.

You can do it periodically using your system cron or the uWSGI supplied one (if you are running the GitWhoosh WSGI app)

```python
from uwsgidecorators import cron
from gitwhoosh import GitWhoosh
application = GitWhoosh('path_of_your_repository', '/tmp/indexes')

@cron(59, 4, -1, -1, -1)
def reindex(signum):
    application.index()
```