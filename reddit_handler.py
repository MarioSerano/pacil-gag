import praw #ini reddit API Wrapper
import random

from prawcore.exceptions import Redirect
from prawcore.exceptions import ResponseException


class ClientInfo:
    id = 'TpEjWEc2SHTafQ'
    secret = 'kuojXoBkMZs_JWrCVEaDWgW8FhA'
    user_agent = 'Meme Api'

class Meme:
    def __init__(self, title, url, link):
        self.title = title
        self.url = url
        self.link = link

class MemeCollection:
    def __init__(self):
        self.meme_collection = []
        self.title_collection = []
    def append(self, meme):
        self.meme_collection.append(meme)
        self.title_collection.append(meme.title)
    def extend_memes(self, memes):
        self.meme_collection += memes
    def extend_title(self, titles):
        self.title_collection += titles
    def get_title(self, title):
        for meme in self.meme_collection:
            if title == meme.title:
                return meme
    def remove(self, ids):
        for meme in self.meme_collection:
            if ids == meme.id:
                self.title_collection.remove(meme.title)
                self.meme_collection.remove(meme)
                

def is_img_link(link):
    ext = link[-4:]
    if ext == '.jpg' or ext == '.png':
        return True
    else:
        return False


def get_posts(sub, limit):

    r = praw.Reddit(client_id=ClientInfo.id, client_secret=ClientInfo.secret,
                    user_agent=ClientInfo.user_agent) 

    class Meme:
        def __init__(self, title, url, shortlink):
            self.title = title
            self.url = url
            self.shortlink = shortlink
        def id(self, ids):
            self.id = ids

    submissions = r.subreddit(sub).hot(limit=limit)

    result = [
        Meme(submission.title, submission.url, submission.shortlink) for submission in submissions
    ]

    return result




