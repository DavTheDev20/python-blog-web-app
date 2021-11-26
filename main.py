import re
from flask import Flask, jsonify, request, render_template, redirect, Response
import json
from bson.objectid import ObjectId
from flask.helpers import url_for
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


@app.route('/posts')
def posts_page():
    posts_data = posts_collection.find()
    posts = [post for post in posts_data]
    return render_template('posts.html', posts=posts)


@app.route('/posts/<id>')
def post_page(id):
    post = posts_collection.find_one({"_id": ObjectId(id)})
    return render_template('post.html', post=post)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/edit/<id>', methods=["GET", "PUT"])
def edit(id):
    if request.method == "GET":
        post = posts_collection.find_one({"_id": ObjectId(id)})
        return render_template('edit.html', post=post)
    elif request.method == "PUT":
        post = posts_collection.find_one({"_id": ObjectId(id)})
        if post:
            updated_post = {
                "title": request.form['title'],
                "content": request.form['content'],
                "dateCreated": post.dateCreated,
                "dateUpdated": datetime.datetime.utcnow()
            }
            updated_post_id = posts_collection.replace_one(
                {"_id": post._id}, updated_post).upserted_id
            print(updated_post_id)
            return redirect(f'/posts/{updated_post_id}')

# API Routing


@app.route('/api/posts', methods=["GET", "POST"])
def posts():
    if request.method == "GET":
        posts_data = posts_collection.find()
        posts = [post for post in posts_data]
        return Response(json.dumps(posts, default=str), mimetype="application/json", status=200)
    elif request.method == "POST":
        new_post = {
            "title": request.form['title'],
            "content": request.form['content'],
            "dateCreated": datetime.datetime.utcnow()
        }
        new_post_id = posts_collection.insert_one(new_post).inserted_id
        if new_post_id:
            Response(
                f"New post with id: {new_post_id}, was created.", status=200)
            return redirect(url_for('posts_page'))
        else:
            return Response("Error creating new post", status=400)


if __name__ == "__main__":
    app.run(debug=True)
