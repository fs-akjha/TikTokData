#TODO Users related Views that would call the camapign service to resolve the request
from flask import request,jsonify,make_response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import sys, os
import time
import datetime
from app.base import Session
from app import app
from werkzeug.security import generate_password_hash,check_password_hash
from users.service import user_service,company_service,message_service,batch_service
from securities.service import auth_service
from TikTokApi import TikTokApi

api = TikTokApi()

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message':'Hello!!'})


@app.route('/login', methods=['POST'])
def login():
    payload = request.json
    user = auth_service.login(payload)

    if not user:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login Required!"'})
    else:
        access_token = create_access_token(identity=user, fresh=True)
        refresh_token = create_refresh_token(identity=user)
        user["access_token"] = access_token
        user["refresh_token"] = refresh_token
        return user

    # if check_password_hash(user.hashed_password,auth.password):
    #     token=jwt.encode({'id':user.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
    #     return jsonify({'token':token.decode('UTF-8')})
    #
    # return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login Required!"'})


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@app.route('/getallusers', methods=['GET'])
@jwt_required()
def get_all_users():
    identity = get_jwt_identity()
    if (identity['role']=='hashoff-admin'):
        result = user_service.list_users()
        return result
    else:
        return ({"message":'No Access'})


@app.route('/createuser',methods=['GET','POST'])
@jwt_required()
def create_new_user():
    ts = time.time()
    identity = get_jwt_identity()
    if (identity['role']=='hashoff-admin'):
        if request.method == "POST":
            data=request.get_json()
            hashed_password=generate_password_hash(data['hashed_password'],method='sha256')
            email_address=request.json['email_address']
            name=request.json['name']
            role=request.json['role']
            company_id=request.json['company_id']
            created_date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            modified_date=datetime.datetime.utcnow()
            result=user_service.create_user(email_address,hashed_password,name,role,created_date,modified_date,company_id)
            return result
    else:
        return ({"message":'No Access'})

@app.route('/getallcompanies',methods=['GET'])
@jwt_required()
def show_companies():
    identity = get_jwt_identity()
    if (identity['role']=='hashoff-admin'):
        result = company_service.list_companies()
        return result
    else:
        return ({"message":'No Access'})

@app.route('/createcompany',methods=['POST'])
@jwt_required()
def create_new_company():
    ts = time.time()
    identity = get_jwt_identity()
    if (identity['role']=='hashoff-admin'):
        if request.method == "POST":
            data=request.get_json()
            name=request.json['name']
            added_by_user_id=identity['id']
            seat_limit=request.json['seat_limit']
            campaign_limit=request.json['campaign_limit']
            facebook_limit=request.json['facebook_limit']
            instagram_limit=request.json['instagram_limit']
            twitter_limit=request.json['twitter_limit']
            youtube_limit=request.json['youtube_limit']
            created_date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            modified_date=datetime.datetime.utcnow()
            result=company_service.create_company(name,seat_limit,campaign_limit,facebook_limit,instagram_limit,twitter_limit,youtube_limit,created_date,modified_date,added_by_user_id)
            return result
    else:
        return ({"message":'No Access'})

@app.route('/showcompany/<id>',methods=['GET'])
@jwt_required()
def show_one_company(id):
    user=company_service.show_one_company(id)
    return user

@app.route('/createmessage',methods=['POST'])
@jwt_required()
def create_new_message():
    ts = time.time()
    identity = get_jwt_identity()
    if request.method == "POST":
        data=request.get_json()
        campaign_id=request.json['campaign_id']
        created_by_user_id=identity['id']
        message_template=request.json['message_template']
        created_date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        modified_date=datetime.datetime.utcnow()
        result=message_service.create_message_template(campaign_id,created_by_user_id,message_template,created_date,modified_date)
        return result

@app.route('/getallmessages',methods=['GET'])
@jwt_required()
def show_messages():
    result = message_service.list_messages()
    return result

@app.route('/showusersbycid/<id>',methods=['GET'])
@jwt_required()
def show_users_on_company(id):
    identity = get_jwt_identity()
    if (identity['role']=='hashoff-admin'):
        users=user_service.filtered_users_by_cid(company_id=id)
        return users
    else:
        return ({"message":'No Access'})

@app.route('/showbatches',methods=['GET'])
@jwt_required()
def show_batches():
    identity = get_jwt_identity()
    if (identity['role']=='hashoff-admin'):
        result = batch_service.list_batches()
        return result
    else:
        return ({"message":'No Access'})


@app.route('/createbatch',methods=['POST'])
@jwt_required()
def create_new_batches():
    ts = time.time()
    identity = get_jwt_identity()
    if (identity['role']=='hashoff-admin'):
        if request.method == "POST":
            data=request.get_json()
            created_by_user_id=identity['id']
            batch_status=request.json['batch_status']
            send_date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            subject=request.json['subject']
            desired_batch_size=request.json['desired_batch_size']
            created_date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            modified_date=datetime.datetime.utcnow()
            result=batch_service.create_batch(created_by_user_id,batch_status,send_date,subject,created_date,modified_date,desired_batch_size)
            return result
    else:
        return ({"message":'No Access'})


@app.route('/getrends',methods=['POST'])
@jwt_required()
def get_hashtage():
    trends = api.trending()
    return ({"TrendsData":trends})

@app.route('/getposts',methods=['POST'])
@jwt_required()
def get_posts():
    results = 10
    username = request.json["username"]
    posts = api.byUsername(username, count=results)
    return ({"PostsData":posts})

@app.route('/getusers',methods=['POST'])
@jwt_required()
def get_users():
    results = 10
    search_term = request.json["search_term"]
    users = api.search_for_users(search_term)
    return ({"Users":users})


@app.route('/searchbyhashtag',methods=['POST'])
@jwt_required()
def get_hashtag():
    results = 10
    hashtag = request.json["hashtag"]
    hashtag_result = api.byHashtag(hashtag, count=results)
    return ({"HashtagsResults":hashtag_result})


@app.route('/searchformusic',methods=['POST'])
@jwt_required()
def get_music():
    search_music = request.json["search_music"]
    music = api.search_for_music(search_music)
    return ({"Music":music})


@app.route('/getlikesforuser',methods=['POST'])
@jwt_required()
def get_likes_users():
    username = request.json["username"]
    results = 30
    liked_list = api.userLikedbyUsername(username, count=results)
    return ({"UsersLikes":liked_list})


@app.route('/searchbyhashtags',methods=['POST'])
@jwt_required()
def get_by_hashtags():
    search_hashtags = request.json["search_hashtags"]
    hashtags = api.search_for_hashtags(search_hashtags)
    return ({"HashtagsResult":hashtags})