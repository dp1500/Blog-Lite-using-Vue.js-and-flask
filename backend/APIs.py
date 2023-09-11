from flask_restful import Resource, fields, marshal_with,reqparse, Api
from flask import jsonify
from models import *
from database import db
from validation import *
from flask import request, flash,Blueprint
from sqlalchemy import desc , select, join
from useful_functions import update_followers_AND_following_count

# from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from jwt_utils import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_jwt_extended import create_access_token

# Create blueprint for API routes
api_routes = Blueprint('api', __name__)
api = Api(api_routes)

# from getImage import *

# from werkzeug.utils import secure_filename
# import os


# #configuring path and constraint to save images
# UPLOAD_FOLDER = 'static\images'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# def allowed_file(filename):
#   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# parser for updating profile data
profile_parser = reqparse.RequestParser()
profile_parser.add_argument('name')
profile_parser.add_argument('username')
profile_parser.add_argument('about')
profile_parser.add_argument('old_password')
profile_parser.add_argument('new_password')
profile_parser.add_argument('file')

profile_parser.add_argument('password')

#creating api for login
class Login(Resource):
    def post(self):
        
        username = request.json.get('username')
        password = request.json.get('password')

        user = users.query.filter_by(username=username).first()

        if user == None:
            response = jsonify(error='Username Does Not Exist')
            response.status_code = 409  # HTTP status code for conflict
            return response
        
        elif user.password != password:
            response = jsonify(error='Invalid credentials')
            response.status_code = 401  # HTTP status code for conflict
            return response
        
        elif user.password == password:
            access_token = create_access_token(identity=username)

            #update last activity time so that celery can notify the user by sending email, to open app
            user.last_activity = datetime.utcnow()
            db.session.commit()
            
            return {'access_token': access_token}, 200


# api to login using token based authentication
api.add_resource(Login, '/api/login')


#api for login out that deletes the cookie (token)
class Logout(Resource):
    def post(self):
        pass

class ProfileDataApi(Resource):
    
    @jwt_required()
    def get(self):
        
        current_user = get_jwt_identity()
        
        # update_followers_AND_following_count(Uid)

        user = users.query.filter_by(username=current_user).first() 

        if user:
            response = { "Uid": user.Uid, "name": user.name, "username": user.username, "posts": user.posts, "n_followers": user.n_followers, "n_following": user.n_following, "email": user.email,"about": user.about, "profile_pic_url" : user.profile_pic_url}
            # not sending password to the client for secuirty reasons

            return jsonify(response)
        else:
            response = jsonify(error='Username Does Not Exist')
            response.status_code = 409  # HTTP status code for conflict
            return response

    def post(self):

        name = request.json.get('name')
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        
        username_exists = users.query.filter_by(username=username).first()

        if username_exists:
            response = jsonify(error='Username already exists')
            response.status_code = 409  # HTTP status code for conflict
            return response

        else:
            new_user = users(username=username, name=name, password = password, email = email, posts = 0, n_followers=0, n_following=0)
            db.session.add(new_user)
            db.session.commit()

            return 200

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        
        user = users.query.filter_by(username=current_user).first() 

        if user:

            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            about = request.form.get('about')
            new_password = request.form.get('new_password')
            old_password = request.form.get('old_password')
            image_file = request.files.get('file')

            if name == None or username == None or email == None or old_password == None:
                raise BusinessValidationError(status_code= 400, error_code=	"input missing", error_message= "input missing")

            if old_password == user.password:

                if name != 'null':
                    user.name = name
                if username != 'null':
                    user.username = username
                if email != 'null':
                    user.email = email
                if about != 'null':
                    user.about = about
                
                if image_file is not None:

                    # save the file to a folder on the server
                    file_path = 'static/images/profile_pics/' + image_file.filename
                    image_file.save(file_path)

                    # including backend server path so that frontend can acces the image
                    file_path = 'http://127.0.0.1:5000/static/images/profile_pics/' + image_file.filename
                    user.profile_pic_url = file_path
                
                if new_password and new_password!= "null":
                    user.password = new_password
            
                        
                db.session.commit()
                flash("profile updated succesfully")
                return 200
            
            else:
                return 409
                # invalid credentials
        else:
            raise NotFoundError(message = "user not found", status_code= 404)

    @jwt_required()
    def delete(self):

        current_user = get_jwt_identity()

        user = db.session.query(users).filter(users.username == current_user).first()

        if user:
            # blogs_by_user = db.session.query(blogs).filter(blogs.user_id == Uid).all()
            delete_blogs_by_user = blogs.__table__.delete().where(blogs.user_id == user.Uid)


            # followings = follows.query.filter(follows.follower == Uid or follows.following == Uid).all()

            followings_id = follows.query.filter(follows.following == user.Uid).all()
            for id in followings_id:
                temp_user = db.session.query(users).filter(users.Uid == id.follower).first()
                temp_user.n_following -= 1
                
            
            followers_id = follows.query.filter(follows.follower == user.Uid).all()
            for id in followers_id:
                temp_user = db.session.query(users).filter(users.Uid == id.following).first()
                temp_user.n_followers -= 1
                

            delete_followings = follows.__table__.delete().where(follows.follower == user.Uid)
            delete_followers = follows.__table__.delete().where(follows.following == user.Uid)


            db.session.delete(user)

            # db.session.delete(blogs_by_user)
            # db.session.delete(followings)

            db.session.execute(delete_blogs_by_user)
            db.session.execute(delete_followings)
            db.session.execute(delete_followers)

            db.session.commit()
            return "profile succesfully deleted", 200
        else:
           raise NotFoundError(message = "user not found", status_code= 204)
 


class UserProfileDataApi(Resource):
    
    
    def get(self, username):
        
        # update_followers_AND_following_count(Uid)

        user = users.query.filter_by(username=username).first() 

        if user:
            response = { "Uid": user.Uid, "name": user.name, "username": user.username, "posts": user.posts, "n_followers": user.n_followers, "n_following": user.n_following, "email": user.email,"about": user.about, "profile_pic_url" : user.profile_pic_url}
            # not sending password to the client for secuirty reasons
            print(" user response sent to frontend")
            return jsonify(response)
        else:
            response = jsonify(error='Username Does Not Exist')
            response.status_code = 409  # HTTP status code for conflict
            return response


class ProfileBlogsApi(Resource):

    @jwt_required()
    def get(self):
        
        # Uid = int(Uid)
        
        current_user = get_jwt_identity()

        user = users.query.filter_by(username=current_user).first()

        if user == None:
            return "error getting user or user not found ", 409
       
        Blogs = db.session.query(blogs).filter(blogs.user_id == user.Uid).order_by(desc(blogs.time_stamp)) 
        
        # if Blogs == None:
        #     return "error getting blogs or no blogs fouund", 407

        if Blogs:

            blogsData = []
            for blog in Blogs:
                # user = db.session.query(users).filter(users.Uid == blog.user_id).first()

                blogsData.append( { "username": user.username, "blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
                            "likes": blog.likes, "n_comments": blog.n_comments,"time_stamp": blog.time_stamp.isoformat()  })
        
            # jsonify(response)
            return blogsData

        else:
            raise NotFoundError(message = "blog not found", status_code= 204)
    
class UserProfileBlogsApi(Resource):
    
    def get(self, username):
        
        user = users.query.filter_by(username=username).first()

        if user == None:
            return "error getting user or user not found ", 409
       
        Blogs = db.session.query(blogs).filter(blogs.user_id == user.Uid).order_by(desc(blogs.time_stamp)) 
        
        # if Blogs == None:
        #     return "error getting blogs or no blogs fouund", 407

        if Blogs:

            blogsData = []
            for blog in Blogs:
                # user = db.session.query(users).filter(users.Uid == blog.user_id).first()

                blogsData.append( { "username": user.username, "blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
                            "likes": blog.likes, "n_comments": blog.n_comments,"time_stamp": blog.time_stamp.isoformat()  })
        
            # jsonify(response)
            return blogsData

        else:
            raise NotFoundError(message = "blog not found", status_code= 204)   


# to sort list of bolgs according time
from operator import itemgetter


class FeedBlogsApi(Resource):

    @jwt_required()
    def get(self):
        # Uid = int(Uid)

        print("feed api called")
        current_user = get_jwt_identity()

        Currentuser = users.query.filter_by(username=current_user).first()

        followings = follows.query.filter(follows.follower == Currentuser.Uid).all()

        # blogsData = []

        # if followings == None:
        #     return blogsData, 204

        #     # raise NotFoundError(message = "blog not found", status_code= 204)   

        # else:
        FeedPageData = {
            "logged_user_name": Currentuser.name,
            "logged_user_followings": Currentuser.n_following,
            "blogsData": []
        }


        for follow in followings:
            Blogs = db.session.query(blogs).filter(blogs.user_id == follow.following).order_by(desc(blogs.time_stamp)).all()
            user = db.session.query(users).filter(users.Uid == follow.following).first()

            for blog in Blogs:
                if blog.n_views == None:
                    blog.n_views = 0
                blog.n_views += 1
                db.session.commit()
                FeedPageData["blogsData"].append( { "Uid":  user.Uid, "username": user.username, "profile_pic_url": user.profile_pic_url,"blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
                             "likes": blog.likes, "n_comments": blog.n_comments, "time_stamp": blog.time_stamp.isoformat()  }) 
        
        # if blogsData == []:
        #     raise NotFoundError(message = "blog not found", status_code= 204)   

        FeedPageData["blogsData"] = sorted(FeedPageData["blogsData"], key=itemgetter('time_stamp'), reverse=True)
        print(FeedPageData)
        return FeedPageData


class ProfileStats(Resource):

    @jwt_required()
    def get(self):
        
        """ graph mei followers_following_ratio, "avg_engagement_rate": avg_engagement_rate,
            "avg_likes_per_post": avg_likes_per_post,
            "avg_comments_per_post": avg_comments_per_post. ye sab dikha dena """
        

        # avg_engagement_rate = ((total_likes + total_comments) / total_views) * 100


        current_user = get_jwt_identity()

        user = users.query.filter_by(username=current_user).first()
        blogs_by_user = blogs.query.filter(blogs.user_id == user.Uid).all()
        # followings = follows.query.filter(follows.follower == user.Uid).all()

        total_posts = len(blogs_by_user)
        total_followers = user.n_followers
        total_following = user.n_following
        

        if total_following == 0:
            followers_following_ratio = "ND"
        else:
            followers_following_ratio = total_followers/total_following
        
        total_likes_from_all_posts = 0
        total_comments_from_all_posts = 0
        total_views_from_all_posts = 0

        most_liked_post_title = ""
        most_liked_post_likes = 0

        most_commented_post_title = ""
        most_commented_post_n_comments = 0


        for blog in blogs_by_user:

            total_likes_from_all_posts += blog.likes
            total_comments_from_all_posts += blog.n_comments
            if blog.n_views == None:
                blog.n_views = 0
            total_views_from_all_posts += blog.n_views

            if blog.likes > most_liked_post_likes:
                most_liked_post_title = blog.title
                most_liked_post_likes = blog.likes

            if blog.n_comments > most_commented_post_n_comments:
                most_commented_post_title = blog.title
                most_commented_post_n_comments = blog.n_comments
        
        if total_posts == 0:
            avg_engagement_rate = "ND"
            avg_likes_per_post = "ND"
            avg_comments_per_post = "ND"
        
        else:
            avg_engagement_rate = ((total_likes_from_all_posts + total_comments_from_all_posts) / total_views_from_all_posts) 
            avg_engagement_rate = round(avg_engagement_rate, 2)

            avg_likes_per_post = total_likes_from_all_posts / total_posts
            avg_likes_per_post = round(avg_likes_per_post, 2)

            avg_comments_per_post = total_comments_from_all_posts / total_posts
            avg_comments_per_post = round(avg_comments_per_post, 2)
        


        import matplotlib.pyplot as plt
        import datetime

        # Define the data to be plotted
        stats = {'avg_likes_per_post': avg_likes_per_post, 'avg_comments_per_post': avg_comments_per_post, 'avg_engagement_rate': avg_engagement_rate}

        plt.figure(figsize=(8, 6))
        # Create a bar chart
        plt.bar(range(len(stats)), list(stats.values()), align='center')
        plt.xticks(range(len(stats)), list(stats.keys()))
        plt.ylabel('Average')
        plt.title('Profile Stats')
        for i, v in enumerate(stats.values()):
            plt.text(i, v, str(v), ha='center', va='bottom')

    

        # Save the bar chart image to a desired location

        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        file_path = f'static/images/profile_stats/{current_datetime}.jpg'

        plt.savefig(file_path)

        print("profile stats api called 5")

         # including backend server path so that frontend can acces the image
        file_path = f'http://127.0.0.1:5000/static/images/profile_stats/{current_datetime}.jpg'
        # Save the bar chart image to a desired location
        
        print("profile stats api called 6")

        # Close the plot
        plt.close()

        profile_stats = {
            "total_posts": total_posts,
            "total_followers": total_followers,
            "total_following": total_following,
            "followers_following_ratio": followers_following_ratio,

            "most_liked_post_title": most_liked_post_title,
            "most_liked_post_likes": most_liked_post_likes,

            "most_commented_post_title": most_commented_post_title,
            "most_commented_post_n_comments": most_commented_post_n_comments,

            "total_likes_from_all_posts": total_likes_from_all_posts,
            "total_comments_from_all_posts": total_comments_from_all_posts,
            "total_views_from_all_posts": total_views_from_all_posts,
            "avg_engagement_rate": avg_engagement_rate,
            "avg_likes_per_post": avg_likes_per_post,
            "avg_comments_per_post": avg_comments_per_post,
            "graph_image_file_path": file_path,
            "username": current_user,
            "email": user.email
            }

        return jsonify(profile_stats)
    
# Add API resource routes
api.add_resource(ProfileStats, '/api/profilestats')



class LikePost(Resource):
    def post(self, blog_id):
        # Retrieve the post_id from the request body
        # post_id = request.json.get('post_id')
        blog_id = int(blog_id)
        blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()
        # Increment the like count for the post with post_id in the blog with blog_id
        blog.likes += 1
        # and store the updated count in your database
        db.session.commit()
        # ...
        
        # Return the updated like count and whether the user has liked the post
        return {
            'likes': blog.likes,
            'isLiked': True,  # assuming the user has just liked the post
        }

api.add_resource(LikePost, '/api/LikePost/<string:blog_id>')

class Comments(Resource):

    def get(self, blog_id):
        blog_id = int(blog_id)

        commentS = db.session.query(comments).filter(comments.blog_id == blog_id).all()
        comments_list = []
        for comment in commentS:
            user = db.session.query(users).filter(users.Uid == comment.poster_user_id).first()
            comments_list.append({"comment_id": comment.comment_id, "blog_id": comment.blog_id, "comment": comment.comment, "poster_user_id": comment.poster_user_id,"username": user.username, "profile_pic_url": user.profile_pic_url,})
            
        return jsonify(comments_list)
    
    @jwt_required()
    def post(self, blog_id):
        blog_id = int(blog_id)

        comment = request.form.get('comment')

        # comment = request.json.get('comment')

        current_user = get_jwt_identity()
        user = users.query.filter_by(username=current_user).first()
        new_comment = comments(blog_id=blog_id, comment=comment, poster_user_id=user.Uid)
        db.session.add(new_comment)
        blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()
        blog.n_comments += 1
        db.session.commit()

        blog_id = int(blog_id)

        commentS = db.session.query(comments).filter(comments.blog_id == blog_id).all()
        comments_list = []
        for comment in commentS:
            user = db.session.query(users).filter(users.Uid == comment.poster_user_id).first()
            comments_list.append({"comment_id": comment.comment_id, "blog_id": comment.blog_id, "comment": comment.comment, "poster_user_id": comment.poster_user_id,"username": user.username, "profile_pic_url": user.profile_pic_url,})
            
        return jsonify(comments_list)

        # return {"message": "comment added"}, 201

api.add_resource(Comments, "/api/comments/<string:blog_id>")


import csv

class BlogApi(Resource):

    def get(self, blog_id):

        # blog_id = int(blog_id)

        blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()

        if blog:
            return {"blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
                                        "time_stamp": blog.time_stamp.isoformat() }, 200
        else:
            raise NotFoundError(message = "blog not found", status_code= 204)   

    @jwt_required()
    def put(self, blog_id):

        current_user = get_jwt_identity()

        blog_id = int(blog_id)
        blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()

        if blog:

            title = request.form.get('title')
            description = request.form.get('description')
            image_file = request.files.get('file')

            if title == None or description == None:
                raise BusinessValidationError(status_code= 400, error_code=	"input missing", error_message= "input missing")
            

            if image_file is not None:

                # save the file to a folder on the server
                file_path = 'static/images/blogs/' + image_file.filename
                image_file.save(file_path)

                # including backend server path so that frontend can acces the image
                file_path = 'http://127.0.0.1:5000/static/images/blogs/' + image_file.filename
                blog.image_url = file_path
            
            if title != 'null':
                blog.title = title
            if description != 'null':
                blog.description = description
            

            db.session.commit()
            
            # return { "Uid": user.Uid, "name": user.name, "username": user.username, "posts": user.posts, "followers": user.n_followers, "following": user.n_following, "about": user.about}
            return 200
        else:
            raise NotFoundError(message = "blog not found", status_code= 204)
    
    @jwt_required()
    def delete(self, blog_id):

        current_user = get_jwt_identity()

        blog_id = int(blog_id)

        blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()

        user = db.session.query(users).filter(users.Uid == blog.user_id).first()

        if blog:
            db.session.delete(blog)
            user.posts = user.posts-1

            db.session.commit()
            return 200
        else:
            raise BusinessValidationError(status_code= 400, error_code=	"input missing", error_message= "bad request")



    @jwt_required()
    def post(self):

        current_user = get_jwt_identity()

        print(" level 1")

        csvFlag = request.form.get('csvFlag')

        print("level 1.2")

        if csvFlag != "null":
            csv_file = request.files['csv'] # add this line to access the uploaded CSV file
            print(" level 2")
            # print(csv_file)
            if csv_file:
                print(" level 3")
                image_file = request.files.get('file')
                print(" level 4")
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                csv_row = next(csv_data)
                csv_row = next(csv_data)  # read the first (and only) row of the CSV file
                csv_title = csv_row[0]  # assume that the title is in the first column of the CSV file
                csv_description = csv_row[1]  # assume that the description is in the second column of the CSV file
                print(" level 5")
                if image_file is None:
                    return 'No file uploaded', 409
                print(" level 6")
                # save the file to a folder on the server
                file_path = 'static/images/blogs/' + image_file.filename
                image_file.save(file_path)

                # including backend server path so that frontend can acces the image
                file_path = 'http://127.0.0.1:5000/static/images/blogs/' + image_file.filename

                user = users.query.filter_by(username=current_user).first()
                print(" level 7")
                new_blog = blogs(user_id = user.Uid, title = csv_title, description = csv_description, image_url = file_path, likes =0, n_comments =0,n_views =0)
                db.session.add(new_blog)

                user.posts = user.posts + 1
                db.session.commit()
                print(" level 8")
                return 200
        else:
            print(" level 9")

            title = request.form.get('title')
            description = request.form.get('description')

            image_file = request.files.get('file')
            
            print(" level 10")

            if image_file is None:
                return 'No file uploaded', 409

            print(" level 12")

            # save the file to a folder on the server
            file_path = 'static/images/blogs/' + image_file.filename
            image_file.save(file_path)

            # including backend server path so that frontend can acces the image
            file_path = 'http://127.0.0.1:5000/static/images/blogs/' + image_file.filename

            user = users.query.filter_by(username=current_user).first()

            new_blog = blogs(user_id = user.Uid, title = title, description = description, image_url = file_path, likes =0, n_comments =0)
            db.session.add(new_blog)

            user.posts = user.posts + 1
            db.session.commit()

            return 200 


from  sqlalchemy.sql.expression import func, select
import random

# api to get blogss for browse page
class BrowseBlogsApi(Resource):

    def get(self):
        
        # Blogs = db.session.query(blogs).limit(6)

        # count = db.session.query(blogs).count()
        Blogs = db.session.query(blogs).limit(10)

        if blogs:

            blogsData = []

            for blog in Blogs:
                
                if random.randint(1, 40) > 4:
                    user = db.session.query(users).filter(users.Uid == blog.user_id).first()

                    blogsData.append( { "Uid":  user.Uid, "username": user.username, "profile_pic_url": user.profile_pic_url,"blog_id" : blog.blog_id, "title": blog.title, "description" : blog.description, "image_url": blog.image_url, 
                                "time_stamp": blog.time_stamp.isoformat() })

            random.shuffle(blogsData)        
            return blogsData
        else:
            raise NotFoundError(message = "blog not found", status_code= 204)

## api to get follow status of a current user to a given user
class FollowStatusApi(Resource):

    @jwt_required()
    def get(self, username):
        # here the ussername arg is for the userprofile current user is visiting
        current_user = get_jwt_identity()

        Currentuser = users.query.filter_by(username=current_user).first()
        user_being_visited = users.query.filter_by(username=username).first()

        followings = follows.query.filter(follows.follower == Currentuser.Uid).all()

        print(followings)

        print(user_being_visited.Uid)

        print("username for follow search is:   " + str(username))

        for following in followings:
            if following.following == user_being_visited.Uid:
                print(following.following)
                print(user_being_visited.Uid)
                print("step 2")
                return {'isFollowing': True}

        print("not following")
        return {'isFollowing': False}


        
        # result = follows.query.filter(follows.follower == Currentuser.Uid and follows.following == user_being_visited.Uid).first()
        
        # if result:
        #     return {'isFollowing': True}
        # else:
        #     return {'isFollowing': False}


    @jwt_required()
    def post(self,username):
        # here the ussername arg is for the userprofile current user is visiting
        current_user = get_jwt_identity()
        
        Currentuser = users.query.filter_by(username=current_user).first()
        user_being_visited = users.query.filter_by(username=username).first()
        
        # result = follows.query.filter(follows.follower == Currentuser.Uid and follows.following == user_being_visited.Uid).first()

        followings = follows.query.filter(follows.follower == Currentuser.Uid).all()

        result = False

        for following in followings:
            if following.following == user_being_visited.Uid:
                print(following.following)
                print(user_being_visited.Uid)
                result = True
            else:
                result = False

        if result:
            follows.query.filter_by(following= user_being_visited.Uid, follower = Currentuser.Uid).delete()
            # db.session.delete(result)
            Currentuser.n_following -= 1
            user_being_visited.n_followers -= 1
            db.session.commit()

            return {'isFollowing': False}
        
        else:
            new_following = follows(follower = Currentuser.Uid, following = user_being_visited.Uid)
            # db.session.add(new_following)

            new_follow = follows(follower=Currentuser.Uid, following=user_being_visited.Uid)

            # add the new Follow object to the session
            db.session.add(new_follow)

            Currentuser.n_following += 1
            user_being_visited.n_followers += 1
            db.session.commit()

            return {'isFollowing': True}

        
        

        
        # isFollowing = True
        # user = 'alice'  # Get the logged-in user from the session
        # is_following = args['isFollowing']
        # users[user] = is_following

class FollowingsListApi(Resource):

    @jwt_required()
    def get(self):

        
        current_username = get_jwt_identity()
        user = users.query.filter_by(username=current_username).first()
        
        followings = follows.query.filter(follows.follower == user.Uid).all()
        
        followings_list = []
        
        for follow in followings:
            
            # following_user = users.query.filter_by(users.Uid == follow.following).first()
            following_user = users.query.filter_by(Uid = follow.following).first()
            
            followings_list.append({
                'id': following_user.Uid,
                'username': following_user.username,
                'profile_pic_url': following_user.profile_pic_url
            })
        
        return jsonify(followings_list)

api.add_resource(FollowingsListApi, '/api/followingsList')

class FollowersListApi(Resource):

    @jwt_required()
    def get(self):

        
        current_username = get_jwt_identity()
        user = users.query.filter_by(username=current_username).first()
        
        followings = follows.query.filter(follows.following == user.Uid).all()
        
        followings_list = []
        
        for follow in followings:
            
            # following_user = users.query.filter_by(users.Uid == follow.following).first()
            following_user = users.query.filter_by(Uid = follow.follower).first()
            
            followings_list.append({
                'id': following_user.Uid,
                'username': following_user.username,
                'profile_pic_url': following_user.profile_pic_url
            })
        
        return jsonify(followings_list)

api.add_resource(FollowersListApi, '/api/followersList')

# api to get search results for search box
class SearchUsersApi(Resource):

    
    @jwt_required()
    def get(self):

        q = request.args.get('q')
        current_user = get_jwt_identity()
        Users = users.query.filter(users.username.like(f'%{q}%')).limit(5).all()
        results = []
        for user in Users:
            if user.username != current_user:
                results.append({"Uid": user.Uid, "username": user.username, "profile_pic_url": user.profile_pic_url})

        return jsonify(results)

# class LikePostApi(Resource):
    
#     def get(self, blog_id):

#         blog_id = int(blog_id)

#         blog = db.session.query(blogs).filter(blogs.blog_id == blog_id).first()
#         blog.likes = blog.like + 1

#         db.session.commit()
#         return 200


##################### ADDING ALL APIs to the blueprint #################

#users data api
api.add_resource(ProfileDataApi, "/api/ProfileData","/api/ProfileData/<string:Uid>")

#current-user profile blogs api
api.add_resource(ProfileBlogsApi, "/api/ProfileBlogsData","/api/ProfileBlogsData/<string:Uid>")

#user profile blogs api
api.add_resource(UserProfileBlogsApi, "/api/UserProfileBlogsData","/api/UserProfileBlogsData/<string:username>")

#user profile data api
api.add_resource(UserProfileDataApi, "/api/UserProfileData","/api/UserProfileData/<string:username>")


#Feed blogs api
api.add_resource(FeedBlogsApi, "/api/FeedBlogsData","/api/FeedBlogsData/<string:Uid>")

# blogpost api
api.add_resource(BlogApi, "/api/BlogData","/api/BlogData/<string:blog_id>")

# api to get random blogs for browse page
api.add_resource(BrowseBlogsApi, "/api/BrowseBlogsApi","/api/BrowseBlogsApi/<string:Uid>")


# api to get users for search box
api.add_resource(SearchUsersApi, "/api/SearchUsers","/api/SearchUsers/<string:q>")

# api to get and change follow status of a current user to a given user
api.add_resource(FollowStatusApi, "/api/FollowStatus","/api/FollowStatus/<string:username>")