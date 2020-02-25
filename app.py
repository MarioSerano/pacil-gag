import random
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from reddit_handler import get_posts, ClientInfo, is_img_link, Meme, MemeCollection
from prawcore.exceptions import ResponseException, Redirect

meme_subreddits = ['memes', 'dankmemes']
SAVEDMEMES_ID = []
SAVEDMEMES = MemeCollection()
MEMES_DATABASE = MemeCollection()
IDS = 0

app = Flask(__name__, template_folder="templates")
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/discover')
def discover():
    global IDS
    global SAVEDMEMES
    global MEMES_DATABASE
    re = get_posts(random.choice(meme_subreddits), 100)

    memes_temp = []
    memes_title_temp = []
    for post in re:
        if is_img_link(post.url) and post.title not in SAVEDMEMES.title_collection:
            post.id(IDS)
            memes_temp.append(post)
            memes_title_temp.append(post.title)
            IDS+=1

    MEMES_DATABASE.extend_memes(memes_temp)
    MEMES_DATABASE.extend_title(memes_title_temp)

    return render_template("discover.html", memes=memes_temp)

@app.route('/save', methods=["GET","POST"])
def save():
    global SAVEDMEMES_ID
    if request.method == "POST":
        jsonvar = request.json['memeid']
        for meme in MEMES_DATABASE.meme_collection:
            if meme.id == jsonvar and meme.title not in SAVEDMEMES.title_collection:
                SAVEDMEMES.append(meme)
                break
        else:
            SAVEDMEMES.remove(jsonvar)
    return json.dumps({"success":True}), 200, {"ContentType":"application/json"}


@app.route('/savedmemes')
def savedmemes():
    global SAVEDMEMES_ID
    global SAVEDMEMES
    global MEMES_DATABASE
    return render_template("savedmemes.html", memes=SAVEDMEMES.meme_collection)

@app.route('/search', methods=["GET","POST"])
def search(): 
    global MEMES_DATABASE
    if request.method == "POST":
        title = request.form.get("search")
        if title in MEMES_DATABASE.title_collection:
            meme_requested = MEMES_DATABASE.get_title(title)
            return render_template("search.html", title=meme_requested.title, img_url=meme_requested.url)

    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)