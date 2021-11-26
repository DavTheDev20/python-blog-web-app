from flask import Flask, request, render_template, redirect, Response, url_for
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


@app.route('/posts', methods=["GET", "POST"])
def posts():
    if request.method == "GET":
        posts_data = posts_collection.find()
        posts = [post for post in posts_data]
        return render_template('posts.html', posts=posts)
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
            return redirect(url_for('posts'))
        else:
            return Response("Error creating new post", status=400)


@app.route('/posts/<id>', methods=["GET", "POST"])
def post_page(id):
    if request.method == "GET":
        post = posts_collection.find_one({"_id": ObjectId(id)})
        return render_template('post.html', post=post)
    elif request.method == "POST":
        print('hit')
        result = posts_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return redirect(url_for('posts'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/edit/<id>', methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        post = posts_collection.find_one({"_id": ObjectId(id)})
        return render_template('edit.html', post=post)
    elif request.method == "POST":
        post = posts_collection.find_one({"_id": ObjectId(id)})
        if post:
            updated_post = {
                "title": request.form['title'],
                "content": request.form['content'],
                "dateCreated": post['dateCreated'],
                "dateUpdated": datetime.datetime.utcnow()
            }
            updated_post_id = posts_collection.replace_one(
                {"_id": post['_id']}, updated_post).upserted_id
            print(updated_post_id)
            return redirect(f'/posts/{post["_id"]}')


if __name__ == "__main__":
    app.run(debug=True)
