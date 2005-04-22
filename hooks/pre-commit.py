#!/usr/bin/env python
"""This is a pre-commit hook that checks whether py files being committed
contain tabs in their significant whitespace.
TODO?: check for a file property that says to ignore the significant tabs,
in cases where they're actually needed (although I can't think of any).
"""
import sys
import re
 
from svn import core, fs, delta, repos
 
_tabs = re.compile(r'^\s*\t\s*.*$')
 
class ChangeReceiver(delta.Editor):
    def __init__(self, txn_root, base_root, pool):
        self.txn_root = txn_root
        self.base_root = base_root
        self.pool = pool
 
    def add_file(self, path, parent_baton,
                 copyfrom_path, copyfrom_revision, file_pool):
        return [0, path]
 
    def open_file(self, path, parent_baton, base_revision, file_pool):
        return [0, path]
 
    def apply_textdelta(self, file_baton, base_checksum):
        file_baton[0] = 1
        # no handler
        return None
 
    def close_file(self, file_baton, text_checksum):
        changed, path = file_baton
        if len(path) < 3 or path.lower()[-3:] != '.py' or not changed:
            # This is not a .py file, don't care about tabs
            # TODO - only look inside trunk
            return
 
        # Read the file contents through a tab-finder
        subpool = core.svn_pool_create(self.pool)
 
        stream = core.Stream(fs.file_contents(self.txn_root, path, subpool))
 
        data = stream.read()  # core.SVN_STREAM_CHUNK_SIZE)
        for line in data.splitlines():
            if _tabs.match(line):
                core.svn_pool_destroy(subpool)
                msg = ("Python file contains lines that begin with tabs: '%s'\n" 
                       "There may be others as well." % (path,))
                sys.stderr.write(msg)
                sys.exit(1)
 
        core.svn_pool_destroy(subpool)
 
def check_tabs(pool, repos_path, txn):
    def authz_cb(root, path, pool):
        return 1
 
    fs_ptr = repos.svn_repos_fs(repos.svn_repos_open(repos_path, pool))
    txn_ptr = fs.open_txn(fs_ptr, txn, pool)
    txn_root = fs.txn_root(txn_ptr, pool)
    base_root = fs.revision_root(fs_ptr, fs.txn_base_revision(txn_ptr), pool)
    editor = ChangeReceiver(txn_root, base_root, pool)
    e_ptr, e_baton = delta.make_editor(editor, pool)
    repos.svn_repos_dir_delta(base_root, '', '', txn_root, '',
                              e_ptr, e_baton, authz_cb, 0, 1, 0, 0, pool)
 
 
if __name__ == '__main__':
    assert len(sys.argv) == 3
    core.run_app(check_tabs, sys.argv[1], sys.argv[2])

