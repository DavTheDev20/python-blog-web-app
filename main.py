from flask import Flask, jsonify, request, render_template, redirect, Response
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['python-blog-web-app-DB']
posts_collection = db.posts

# Page Routing

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create')
def create():
    return render_template('create.html')

# API Routing


@app.route('/api/posts', methods=["GET", "POST"])
def posts():
    if request.method == "GET":
        posts_data = posts_collection.find()
        posts = [post for post in posts_data]
        return Response(json.dumps(posts, default=str), mimetype=
                    "application/json", status=200)
    elif request.method == "POST":
        new_post = {
            "title": request.form['title'],
            "content": request.form['content'],
            "dateCreated": datetime.datetime.utcnow()
        }
        new_post_id = posts_collection.insert_one(new_post).inserted_id
        if new_post_id:
            return Response(f"New post with id: {new_post_id}, was created.", status=200)
        else:
            return Response("Error creating new post", status=400)


if __name__ == "__main__":
    app.run(debug=True)
