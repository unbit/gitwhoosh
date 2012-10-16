GitWhoosh
=========

A git repository indexer (using whoosh as the search engine)

GitWhoosh allows you to index in a whoosh database (a fulltext search engine) your git repositories.

The GitWhoosh class exports two main methods: index(), search()

The first one will index the content of your git repository, while the second one will query
the whoosh database.

The following snippet will index all of the restructuredtext files in your tree

```python
from gitwhoosh import GitWhoosh

gw = GitWhoosh('path_of_your_repository', '/tmp/indexes')
gw.index('\.rst$\')
```

while the following one will reports all of the items containing the word FOO or the word BAR

```python
from gitwhoosh import GitWhoosh

gw = GitWhoosh('path_of_your_repository', '/tmp/indexes')
print gw.search('FOO OR BAR')
```