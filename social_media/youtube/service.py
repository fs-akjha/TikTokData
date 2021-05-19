from app.base import es
from app import app
from persistance.campaign_dao import campaign_dao
from persistance.social_media_dao import youtube_user_search_dao,youtube_user_search_history_dao,youtube_influencers_dao,youtube_denial_dao,youtube_stop_words_dao,social_network_dao,social_network_removal_user_dao,social_network_removal_user_reason_dao
import googleapiclient.discovery
import google_auth_oauthlib.flow
from .serializers import influencer_schema,influencers_schema,denial_schema,denials_schema
from google.oauth2 import service_account
import googleapiclient.errors
from flask import Blueprint,jsonify,current_app,Response,request
from elasticsearch import Elasticsearch
from googleapiclient.discovery import build
import requests
import datetime
from social_media.youtube.analysis import youtube_analysis
from datetime import datetime
from isodate import parse_duration
import json
import math
import socket

es = Elasticsearch([{"host":'localhost',"port":'9200'}])

class Youtube:
    def get_videos_q(self,search):
        api_key=current_app.config['YOUTUBE_API_KEY']
        api_service_name = "youtube"
        api_version = "v3"
        youtube=build(api_service_name,api_version,developerKey=api_key)
        start_time=datetime(year=2010,month=1,day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time=datetime(year=2021,month=1,day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
        req=youtube.search().list(q=search,part='snippet',type='video',maxResults=5,publishedAfter=start_time,publishedBefore=end_time)
        res=req.execute()
        channel=[]
        vid_data=[]
        videos_ids=[]
        channels_ids=[]
        for items in sorted(res['items'],key=lambda x:x['snippet']['publishedAt']):
            chanel_ids=items['snippet']['channelId']
            video_id=items['id']['videoId']
            channels_ids.append(chanel_ids)
            videos_ids.append(video_id)
        # for x in range(len(channels_ids)):
        #     pl_request=youtube.playlists().list(part='contentDetails,snippet',channelId=channels_ids[x])
        #     pl_response=pl_request.execute()

        

        for x in range(0,len(channels_ids)):
            pl_request=youtube.channels().list(part='contentDetails,snippet,statistics,brandingSettings',id=channels_ids[x])
            pl_response=pl_request.execute()
            for channel_details in pl_response['items']:
                data1={
                    'id':channel_details['id']
                }

        video_result=youtube.videos().list(id=','.join(videos_ids),part='snippet,statistics,contentDetails')
        video_response=video_result.execute()

        for v_items in video_response['items']:

            v_data={
                'url':'https://www.youtube.com/watch?v={}'.format(v_items['id']),
                'Videothumbnail':v_items['snippet']['thumbnails']['high']['url'],
                'videoTitle':v_items['snippet']['title'],
                'tags':v_items['snippet']['tags'],
                'publishedAt':v_items['snippet']['publishedAt'],
                'Videodescription':v_items['snippet']['description'],
                'comments':v_items['statistics']['commentCount'],
                'viewcount':v_items['statistics']['viewCount'],
                'likecount':v_items['statistics']['likeCount'],
                'duration':parse_duration(v_items['contentDetails']['duration']).total_seconds(),
                'Dislikecount':v_items['statistics']['dislikeCount'],
            }
            pl_request=youtube.channels().list(part='contentDetails,snippet,statistics,topicDetails,brandingSettings',id=v_items['snippet']['channelId'])
            pl_response=pl_request.execute()
            # result_analsis=youtube_analysis.get_play_with_channels(v_items['snippet']['channelId'])
            for channel_details in pl_response['items']:
                subscount=int(channel_details['statistics']['subscriberCount'])
                vidcount=int(channel_details['statistics']['videoCount'])
                subs_vid=int(subscount/vidcount)
                subs_vid_value=int(subs_vid*100)
                follwers_post=int((subs_vid_value)/vidcount)
                data={
                        'id':channel_details['id'],
                        'Channelurl':'https://www.youtube.com/channel/{}'.format(channel_details['id']),
                        'topicsIds':channel_details['topicDetails']['topicIds'],
                        'topicCategories':channel_details['topicDetails']['topicCategories'],
                        'Channelthumbnail':channel_details['snippet']['thumbnails']['high']['url'],
                        'Channeldescription':channel_details['snippet']['description'],
                        'channelTitle':channel_details['snippet']['title'],
                        'publishedAt':channel_details['snippet']['publishedAt'],
                        'SubscriberCount':channel_details['statistics']['subscriberCount'],
                        'VideoCount':channel_details['statistics']['videoCount'],
                        'ChannelView':channel_details['statistics']['viewCount'],
                        'Follwers_BY_POST':follwers_post,
                        'country':channel_details['snippet']['country'],
                        'favorites':channel_details['contentDetails']['relatedPlaylists']['favorites'],
                        'playlistid':channel_details['contentDetails']['relatedPlaylists']['uploads']
                    }
    

            #Merging 2 dictionaries
                merged_dict={**data,**v_data}
                # analysis_results={**result_analsis,**merged_dict}
                vid_data.append(merged_dict)

                youtube_user_search_dao.create_user(merged_dict)
                # result = es.index(index='youtubesearch', doc_type='YoutubeSearchData',body=merged_dict,timeout="1000000000s")
        # return Response(json.dumps(total_videos),mimetype='application/json')
        return vid_data


    def get_play_with_channel(self,channelid):
        api_key=current_app.config['YOUTUBE_API_KEY']
        api_service_name = "youtube"
        api_version = "v3"
        total_videos=0
        total_subscribers=0
        Average_Likes=0.0
        Average_DisLikes=0.0
        Average_Views=0.0
        Average_Comments=0.0
        Average_Duration=0.0
        Average_Engagements=0.0
        like_dislike_ratio=0.0
        sub_video_ratio=0.0
        youtube=build(api_service_name,api_version,developerKey=api_key)
        channelsid=build(api_service_name,api_version,developerKey=api_key)
        res=youtube.channels().list(id=channelid,part='contentDetails,snippet,statistics').execute()
        for channel_details in res['items']:
                data1={
                    'id':channel_details['id'],
                    'Channelurl':'https://www.youtube.com/channel/{}'.format(channel_details['id']),
                    'Channelthumbnail':channel_details['snippet']['thumbnails']['high']['url'],
                    'Channeldescription':channel_details['snippet']['description'],
                    'channelTitle':channel_details['snippet']['title'],
                    'SubscriberCount':channel_details['statistics']['subscriberCount'],
                    'VideoCount':channel_details['statistics']['videoCount'],
                    'ChannelView':channel_details['statistics']['viewCount'],
                    'country':channel_details['snippet']['country'],
                }
        playlistid=res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        total_videos=data1['VideoCount']
        total_subscribers=data1['SubscriberCount']
        videos=[]
        likes=[]
        averages=[]
        dislikes=[]
        views=[]
        comments=[]
        duration=[]
        eng_add=[]
        related_videos=[]
        next_page_token=None

        while 1:
            res=youtube.playlistItems().list(playlistId=playlistid,part='snippet',maxResults=5,pageToken=next_page_token).execute()
            videos +=res['items']
            
            next_page_token=res.get('nextPageToken')

            if next_page_token is None:
                break
            for vids in res['items']:
                video_result=youtube.videos().list(id=vids['snippet']['resourceId']['videoId'],part='snippet,statistics,contentDetails',maxResults=5).execute()
                for new_data in sorted(video_result['items'],key=lambda x:x['snippet']['publishedAt'],reverse=True):
                    data={
                        'url':'https://www.youtube.com/watch?v={}'.format(new_data['id']),
                        'comments':new_data['statistics']['commentCount'],
                        'viewcount':new_data['statistics']['viewCount'],
                        'likecount':new_data['statistics']['likeCount'],
                        'duration':parse_duration(new_data['contentDetails']['duration']).total_seconds(),
                        'Dislikecount':new_data['statistics']['dislikeCount'],
                        }

                    likecounts=data['likecount']
                    likes.append(likecounts)

                    viewcounts=data['viewcount']
                    views.append(viewcounts)

                    dislikecounts=data['Dislikecount']
                    dislikes.append(dislikecounts)

                    commentcounts=data['comments']
                    comments.append(commentcounts)

                    durations=data['duration']
                    duration.append(durations)

                    eng_add.extend((commentcounts,viewcounts,likecounts))

                    for i in range(0, len(eng_add)):
                        eng_add[i] = int(eng_add[i])

                    for i in range(0, len(likes)):
                        likes[i] = int(likes[i])
                    for i in range(0, len(views)):
                        views[i] = int(views[i])  
                    for i in range(0, len(dislikes)):
                        dislikes[i] = int(dislikes[i])
                    for i in range(0, len(comments)):
                        comments[i] = int(comments[i])
                    for i in range(0, len(duration)):
                        duration[i] = int(duration[i])

                    related_videos.append(data1)


        # print('Total Likes',sum(likes))
        all_likes_sum=int(sum(likes))
        all_views_sum=int(sum(views))
        all_dislikes_sum=int(sum(dislikes))
        all_comments_sum=int(sum(comments))
        all_duration_sum=int(sum(duration))
        total_engagements=int(sum(eng_add))
        # print('Total Videos',total_videos)
        tot_vide=int(total_videos)
        tot_subs=int(total_subscribers)
        Average_Likes=(all_likes_sum/tot_vide)
        Average_Views=(all_views_sum/tot_vide)
        Average_Dislikes=(all_dislikes_sum/tot_vide)
        Average_Comments=(all_comments_sum/tot_vide)
        Average_Duration=(all_duration_sum/tot_vide)
        Average_Engagements=(total_engagements/tot_vide)
        like_dislike_ratio=(Average_Likes/Average_Dislikes)
        sub_video_ratio=(tot_subs/tot_vide)
        # print('Average Likes',Average_Likes)
        result_dict={
            'Total Likes':all_likes_sum,
            'Total Dislikes':all_dislikes_sum,
            'Total Views':all_views_sum,
            'Total Comments':all_comments_sum,
            'Total Durations':all_duration_sum,
            'Total Engagements':total_engagements,
            'Total Videos':tot_vide,
            'Average Likes':Average_Likes,
            'Average Views':Average_Views,
            'Average Dislikes':Average_Dislikes,
            'Average Comments':Average_Comments,
            'Average Durations':Average_Duration,
            'Average Engagements':Average_Engagements,
            'Like-Dislike-Ratio':like_dislike_ratio,
            'Subscriber-Video-Ratio':sub_video_ratio
        }
        averages.append(result_dict)
        new_avg={**data1,**result_dict}

        youtube_user_search_dao.create_user(new_avg)
        # result = es.index(index='youtubesearch', doc_type='YoutubeSearchData',body=new_avg,timeout="10000000000s")
        return new_avg

    def get_all_videos_channel(self,channelid):
        api_key=current_app.config['YOUTUBE_API_KEY']
        api_service_name = "youtube"
        api_version = "v3"
        youtube=build(api_service_name,api_version,developerKey=api_key)
        channelsid=build(api_service_name,api_version,developerKey=api_key)
        res=youtube.channels().list(id=channelid,part='contentDetails,snippet,statistics').execute()
        for channel_details in res['items']:
                data1={
                    'id':channel_details['id'],
                    'Channelurl':'https://www.youtube.com/channel/{}'.format(channel_details['id']),
                    'thumbnail':channel_details['snippet']['thumbnails']['high']['url'],
                    'Channeldescription':channel_details['snippet']['description'],
                    'SubscriberCount':channel_details['statistics']['subscriberCount'],
                    'VideoCount':channel_details['statistics']['videoCount'],
                    'channelTitle':channel_details['snippet']['title'],
                    'country':channel_details['snippet']['country'],
                }
        playlistid=res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        videos=[]
        related_videos=[]
        next_page_token=None

        while 1:
            res=youtube.playlistItems().list(playlistId=playlistid,part='snippet',pageToken=next_page_token).execute()
            videos +=res['items']
            
            next_page_token=res.get('nextPageToken')

            if next_page_token is None:
                break
            for vids in res['items']:
                video_result=youtube.videos().list(id=vids['snippet']['resourceId']['videoId'],part='snippet,statistics',maxResults=50).execute()
                for new_data in (video_result['items']):
                    data={
                        'channelsTitle':new_data['snippet']['channelTitle'],
                        'videoTitle':new_data['snippet']['title'],
                        'publishedAt':new_data['snippet']['publishedAt'],
                        'Videodescription':new_data['snippet']['description'],
                        'url':'https://www.youtube.com/watch?v={}'.format(new_data['id']),
                        'comments':new_data['statistics']['commentCount'],
                        'viewcount':new_data['statistics']['viewCount'],
                        'likecount':new_data['statistics']['likeCount'],
                        'Videothumbnail':new_data['snippet']['thumbnails']['high']['url'],
                        'Dislikecount':new_data['statistics']['dislikeCount'],
                    }

                    merged_dict={**data1,**data}
                    related_videos.append(merged_dict)
                    youtube_user_search_history_dao.create_user_history(merged_dict)
                    # result = es.index(index='youtubechannelhistory', doc_type='ChannelVideoPlaylist',body=merged_dict,timeout="10000000000s")
        return related_videos



    def create_influencer_data(self,campaign_id,approved_by_user_id,social_network,social_network_user_id,post_id,created_date,modified_date):
        create_influencerers=youtube_influencers_dao.create_influencer(campaign_id,approved_by_user_id,social_network,social_network_user_id,post_id,created_date,modified_date)
        campaign_dao.get_by_totalinfcinc_id(id=campaign_id)
        return {"status":create_influencerers}

    def create_denial_data(self,campaign_id,denied_by_user_id,social_network,social_network_user_id,post_id,created_date,modified_date):
        create_influencerers=youtube_denial_dao.create_denails(campaign_id,denied_by_user_id,social_network,social_network_user_id,post_id,created_date,modified_date)
        return {"status":create_influencerers}

    def list_influencers(self,campaign_id):
        channelid=0
        channels_data=[]
        channels=youtube_influencers_dao.get_channelinfcid(campaign_id=campaign_id)
        for data1 in channels:
            channelid=data1.social_network_user_id
            basic_data = es.search(index="youtube_user_index", body={"query": {"match": {'id':channelid}}},size=1000)
            for doc in basic_data['hits']['hits']:
                channel_data={
                    'ChannelId':doc["_source"]["id"],
                    'ChannelURL':doc["_source"]["Channelurl"],
                    'ChannelTitle':doc["_source"]["channelTitle"],
                    'thumbnail':doc["_source"]["Channelthumbnail"],
                    'Subscribers':doc["_source"]["SubscriberCount"],
                    'VideoCount':doc["_source"]["VideoCount"]
                }
                channels_data.append(channel_data)
        return ({'Channels':channels_data})

    def list_denials(self,campaign_id):
        channelid=0
        channels_data=[]
        channels=youtube_denial_dao.get_channeldenid(campaign_id=campaign_id)
        for data1 in channels:
            channelid=data1.social_network_user_id
            basic_data = es.search(index="youtube_user_index", body={"query": {"match": {'id':channelid}}},size=1000)
            for doc in basic_data['hits']['hits']:
                channel_data={
                    'ChannelId':doc["_source"]["id"],
                    'ChannelURL':doc["__source"]["Channelurl"],
                    'ChannelTitle':doc["_source"]["channelTitle"],
                    'thumbnail':doc["_source"]["Channelthumbnail"],
                    'Subscribers':doc["_source"]["SubscriberCount"],
                    'VideoCount':doc["_source"]["VideoCount"]
                }
                channels_data.append(channel_data)
        return ({'Channels':channels_data})

    def list_stop_words(self,channelid):
        all_words = youtube_stop_words_dao.get_all_stopwords()
        results = youtube_user_search_dao.flagged_video(channelid,all_words)
        return results

    def delete_yt_influencer(self,id):
        result=youtube_influencers_dao.remove_influencer(id)
        return result

    def create_reason(self,reason,created_date,modified_date):
        social_network_removal_user_reason_dao.create_reason(reason=reason,created_date=created_date,modified_date=modified_date)
        reason_id=social_network_removal_user_reason_dao.get_reason_detail_id(reason)
        for i in reason_id:
            social_network_user_removal_reason_id=i
        return social_network_user_removal_reason_id


    def add_deleted_user(self,social_network_user_id,social_network_user_removal_reason_id,removed_by_user_id,created_date,modified_date,social_network):
        network_id=0
        social_reason_id=0
        networkid = social_network_dao.get_network_id(name=social_network)
        for nks in networkid:
            network_id=nks.id
        social_network_id=network_id
        results = social_network_removal_user_dao.user_removal(social_network_id,social_network_user_id,removed_by_user_id,social_network_user_removal_reason_id,created_date,modified_date)
        return results

    def filter_prospect(self,search_query,min_followers,max_followers,min_posts,max_posts,max_follwers_to_post,min_follwers_to_post):
        if (len(min_followers)==0):
            min_followers=0
        if (len(max_followers)==0):
            max_followers=9999999999999999

        if(len(min_posts)==0):
            min_posts=0
        if(len(max_posts)==0):
            max_posts=9999999999999999
        
        if(len(min_follwers_to_post)==0):
            min_follwers_to_post=0
        if(len(max_follwers_to_post)==0):
            max_follwers_to_post=9999999999999999
        data = es.search(index="youtube_user_index",size=1000, body=
        {
    "query": {
        "bool": {
        "must": [
            {
            "query_string": {
                "fields": ["Videodescription","tags","videoTitle"],
                "query": search_query
            }
            },
            {
            "range": {
                "SubscriberCount": {
                "gte": min_followers,
                "lte": max_followers
                }
            }
            },
            {
            "range": {
                "VideoCount": {
                "gte": min_posts,
                "lte": max_posts
                }
            }
            },
            {
            "range": {
                "Follwers_BY_POST": {
                "gte": min_follwers_to_post,
                "lte": max_follwers_to_post
                }
            }
            }
        ]
        }
    }
    })
        return data
            

youtube_service = Youtube()