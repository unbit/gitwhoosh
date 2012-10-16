from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, STORED, TEXT, ID
from whoosh.qparser import QueryParser
from dulwich.repo import Repo
import simplejson as json
import re
import urllib

class GitWhoosh:

    def __init__(self, repos_path, index_path):
        self.repo = Repo(repos_path)
        self.index_path = index_path
        self.git_index = self.repo.open_index()
        if not exists_in(self.index_path):
            schema = Schema(path=ID(unique=True, stored=True), itime=STORED, content=TEXT)
            self.ix = create_in(self.index_path, schema)
        else:
            self.ix = open_dir(self.index_path)

    def hook_index(self, func, path):
        mtime = self.git_index[path][1]
        sha = self.git_index[path][8]
        blob = self.repo.get_blob(sha).as_raw_string()
        func(path=path.decode('utf-8'), content=blob.decode('utf-8'), itime=mtime)

    def index(self, regexp=None):
        with self.ix.searcher() as searcher:
            writer = self.ix.writer()
            # first of all, check for removed items
            paths = {}
            for fields in searcher.all_stored_fields():
                paths[fields['path']] = fields['itime']
                if not fields['path'] in self.git_index:
                    writer.delete_by_term('path', fields['path'])
            # now check for new or updated items
            for path in self.git_index:
                if regexp:
                    if not re.search(regexp, path): continue
                if path in paths:
                    if self.git_index[path][1] > paths[path.decode('utf-8')]:
                        self.hook_index(writer.update_document, path)       
                else:
                    self.hook_index(writer.add_document, path) 
            writer.commit()

    def search(self, query):
        parser = QueryParser('content', schema=self.ix.schema)
        q = parser.parse(query.decode('utf-8'))
        found_items = []
        with self.ix.searcher() as searcher:
            results = searcher.search(q, terms=True)
            for r in results:
                terms = []
                for term in r.matched_terms():
                    terms.append(term[1])
                found_items.append({'path':r['path'], 'terms':terms})
        return found_items

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'application/json')])
        output = []
        qs = environ.get('QUERY_STRING', None)
        if qs:
            output = self.search(urllib.unquote(qs))
        return json.dumps(output) 
