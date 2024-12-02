import sys
import requests
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
    def _extract_bookmark_info(self, repo):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description'] if repo['description'] else 'NA'
        }

    def execute(self, data):
        username = data['username']
        preserve_timestamp = data['preserve_timestamp']

        resp = requests.get(
            f'https://api.github.com/users/{username}/starred',
            headers={'Accept': 'application/vnd.github.v3.star+json'}
        )

        cnt = 0

        for star_info in resp.json():
            bookmark = self. _extract_bookmark_info(star_info['repo'])
            if preserve_timestamp:
                bookmark['date_added'] = datetime.strptime(
                    star_info['starred_at'],
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            AddBookmarkCommand().execute(bookmark)
            cnt += 1

        return f'Imported {cnt} bookmarks from starred repos!'
