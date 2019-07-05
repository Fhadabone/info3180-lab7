from app import app,db
from flask import request ,jsonify,make_response
from .models import *
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
import jwt
import datetime

from functools import wraps

def token_required(function):
    @wraps(function)
    def decorated(*args,**kwards):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is not present!'})
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id = data['id']).first()
        except:
            return jsonify({'messsage':'Not a valid token',}),401
        return function(current_user,*args,**kwards)
    return decorated

@app.route("/api/users/register", methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(username=data['username'], password=hashed_password,firstname=data['firstname'], lastname=data['lastname'],email=data['email'], biography=data['biography'])
    #add user to the data base
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User successfully registered!!"})


@app.route("/api/auth/login", methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return make_response('Authentication not verified',401,{'WWW-Austhenticate':'Basic realm ="Login Required!"'})
    user = User.query.filter_by(username=auth['username']).first()
    if not user:
        return make_response('Authentication not verified',401,{'WWW-Authenicate':'Basic realm ="Login Required!"'})
    if check_password_hash(user.password,auth['password']):
        token = jwt.encode({'id':user.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})
    return make_response('Authentication not verified',401,{'WWW-Austhenticate':'Basic realm ="Login Required!"'})


@app.route("/api/auth/logout", methods=['GET'])
@token_required
def logout():
    return jsonify({"message": "User successfully logged out"})

@app.route("/api/users/<user_id>/posts", methods=['POST'])
@token_required
def create_post(current_user,user_id):
    data = request.get_json()
    post = Post(user_id=user_id, photo=data["photo"], caption=data["caption"])
    #add post to database
    db.session.add(post)
    db.session.commit()

    return jsonify({"msg": "Successfully made a new post"})

@app.route("/api/users/<user_id>/posts", methods=['GET'])
@token_required
def get_posts(current_user, user_id):
    posts = Post.query.filter_by(user_id=user_id).all()
    post_lst = []
    for post in posts:
        post_data = {
            'id': post.id,
            'user_id': post.user_id,
            "photo": post.photo,
            "caption": post.caption,
            "created": post.created_on
        }
        post_lst.append(post_data)

    return jsonify({"posts": post_lst})

@app.route("/api/users/<user_id>/follow", methods=['POST'])
@token_required
def follow(current_user, user_id):     
    follow = Follows(user_id=user_id, follower_id=current_user.id)
    db.session.add(follow)
    db.session.commit()
    return jsonify({"message":"Now following '{}'".format(user_id)})

@app.route("/api/posts",methods=['GET'])
@token_required
def get_all_posts(current_user):
    posts = Post.query.all()
    post_lst = []
    for post in posts:
        post_data = {
            'id': post.id,
            'user_id': post.user_id,
            "photo": post.photo,
            "description": post.caption,
            "created_on": post.created_on,
        }
        post_lst.append(post_data)

    return jsonify({"posts": post_lst})

@app.route("/api/posts/<post_id>/like", methods=['POST'])
@token_required
def like(current_user, post_id):
    liked = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if not liked:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({"message":"Post liked"})
    else:
        return jsonify({"message":"You already liked this post!!"})

@app.route("/api/users/<user_id>", methods=['GET'])
@token_required
def get_profile(current_user,user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "No user exist!!"})

    profile = {
        "id": user.id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "biography": user.biography,
        "profile_photo": user.profile_photo,
        "joined_on": user.joined_on,
    }
    return jsonify(profile)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)

    
