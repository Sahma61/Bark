import sys
from datetime import datetime

from databasemanager import DatabaseManager

db = DatabaseManager("bookmarks.db")


class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table('bookmarks', {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL',
            'url': 'TEXT NOT NULL',
            'notes': 'TEXT NOT NULL',
            'date_added': 'TEXT NOT NULL'
        })


class AddBookmarkCommand:
    def execute(self, data):
        if 'date_added' not in data:
            data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!'


class DeleteBookmarkCommand:
    def execute(self, id):
        db.delete('bookmarks', {'id': id})
        return 'bookmark Deleted!'


class ListBookmarksCommand:
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class QuitCommand:
    def execute(self):
        sys.exit(0)


class ImportGithubStarsCommand:
    def execute(self, data):
        cnt = len(data)
        for row in data:
            AddBookmarkCommand().execute(row)
        return f'Imported {cnt} bookmarks from starred repos!'
