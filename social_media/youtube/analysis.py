from app.base import es
from app import app
from persistance.social_media_dao import youtube_user_search_dao
import googleapiclient.discovery
import google_auth_oauthlib.flow
from google.oauth2 import service_account
import googleapiclient.errors
from flask import Blueprint,jsonify,current_app,Response,request
from elasticsearch import Elasticsearch
from googleapiclient.discovery import build
import requests
import datetime
from datetime import datetime
from isodate import parse_duration
import json
import math



class YoutubeAnalysis:
    def get_play_with_channels(self,channelid):
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

                    durations=data['comments']
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

        # youtube_user_search_dao.create_user(new_avg)
        # result = es.index(index='youtubesearch', doc_type='YoutubeSearchData',body=new_avg,timeout="10000000000s")
        return new_avg


youtube_analysis=YoutubeAnalysis()




# elif(((max_follwers_to_post is None) and (min_follwers_to_post is not None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>min_followers and total_subs<=max_followers) and(total_vids>min_posts and total_vids<=max_posts) and(followers_by_post>=min_follwers_to_post)):
#                 print("aaya2")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>min_followers and total_subs<=max_followers) and(total_vids>min_posts and total_vids<=max_posts) and(followers_by_post<=max_follwers_to_post)):
#                 print("aaya3")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>min_followers and total_subs<=max_followers) and(total_vids<=max_posts) and(followers_by_post<=max_follwers_to_post)and(followers_by_post>=min_follwers_to_post)):
#                 print("aaya4")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None) and(min_posts is not None) and (max_posts is not None) and(min_followers is None) and (max_followers is not None) and (total_subs<=max_followers) and(total_vids>=min_posts) and(total_vids<=max_posts) and(followers_by_post<=max_follwers_to_post)and(followers_by_post>=min_follwers_to_post))):
#                 print("aaya5")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is None)) and (total_subs>=min_followers) and(total_vids>=min_posts) and(total_vids<=max_posts) and(followers_by_post<=max_follwers_to_post)and(followers_by_post>=min_follwers_to_post)):
#                 print("aaya6")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break


#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>=min_followers and total_subs<=max_followers) and(total_vids>min_posts and total_vids<=max_posts)):
#                 print("aaya7")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>=min_followers and total_subs<=max_followers) and(followers_by_post>=min_follwers_to_post and followers_by_post<=max_follwers_to_post)):
#                 print("aaya8")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is None) and (max_followers is None)) and(total_vids>=min_posts and total_vids<=max_posts) and(followers_by_post>=min_follwers_to_post and followers_by_post<=max_follwers_to_post)):
#                 print("aaya9")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>min_followers and total_subs<=max_followers) and(total_vids<=max_posts)):
#                 print("aaya10")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>min_followers and total_subs<=max_followers) and(total_vids>=min_posts)):
#                 print("aaya11")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>min_followers and total_subs<=max_followers) and(followers_by_post>=min_follwers_to_post)):
#                 print("aaya12")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>min_followers and total_subs<=max_followers) and(followers_by_post<=max_follwers_to_post)):
#                 print("aaya13")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is None) and (max_followers is None)) and(total_vids>=min_posts and total_vids<=max_posts) and(followers_by_post<=max_follwers_to_post)):
#                 print("aaya14")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is not None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is None) and (max_followers is None)) and(total_vids>=min_posts and total_vids<=max_posts) and(followers_by_post>=min_follwers_to_post)):
#                 print("aaya15")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is None)) and(total_vids>=min_posts and total_vids<=max_posts) and(total_subs>=min_followers)):
#                 print("aaya16")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is None) and (max_followers is not None)) and(total_vids>=min_posts and total_vids<=max_posts) and(total_subs<=max_followers)):
#                 print("aaya17")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is None)) and((min_followers is None) and (max_followers is not None)) and(followers_by_post>=min_follwers_to_post and followers_by_post<=max_follwers_to_post) and(total_subs<=max_followers)):
#                 print("aaya18")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is None)) and((min_followers is not None) and (max_followers is None)) and(followers_by_post>=min_follwers_to_post and followers_by_post<=max_follwers_to_post) and(total_subs>=min_followers)):
#                 print("aaya19")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is not None) and (max_posts is None)) and((min_followers is None) and (max_followers is None)) and(followers_by_post>=min_follwers_to_post and followers_by_post<=max_follwers_to_post) and(total_vids>=min_posts)):
#                 print("aaya20")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is not None)) and((min_followers is None) and (max_followers is None)) and(followers_by_post>=min_follwers_to_post and followers_by_post<=max_follwers_to_post) and(total_vids<=max_posts)):
#                 print("aaya21")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is None)) and((min_followers is not None) and (max_followers is not None)) and(total_subs>=min_followers and total_subs<=max_followers)):
#                 print("aaya22")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is None)) and((min_followers is not None) and (max_followers is None)) and(total_subs>=min_followers and total_vids>=min_posts)):
#                 print("New1")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is not None)) and((min_followers is not None) and (max_followers is None)) and(total_subs>=min_followers and total_vids<=max_posts)):
#                 print("New2")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is None)) and((min_followers is not None) and (max_followers is None)) and(total_subs>=min_followers and followers_by_post<=max_follwers_to_post)):
#                 print("New3")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is None)) and((min_followers is not None) and (max_followers is None)) and(total_subs>=min_followers and followers_by_post>=min_follwers_to_post)):
#                 print("New4")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is None)) and((min_followers is None) and (max_followers is not None)) and(total_subs<=max_followers and followers_by_post>=min_follwers_to_post)):
#                 print("New5")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is None)) and((min_followers is None) and (max_followers is not None)) and(total_subs<=max_followers and followers_by_post<=max_follwers_to_post)):
#                 print("New6")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is not None)) and((min_followers is None) and (max_followers is not None)) and(total_subs<=max_followers and total_vids<=max_posts)):
#                 print("New7")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is None)) and((min_followers is None) and (max_followers is not None)) and(total_subs<=max_followers and total_vids>=min_posts)):
#                 print("New7")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is not None)) and((min_followers is None) and (max_followers is None)) and(total_vids>=min_posts) and (total_vids<=max_posts)):
#                 print("aaya23")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is None)) and((min_posts is not None) and (max_posts is None)) and((min_followers is None) and (max_followers is None)) and(total_vids>=min_posts) and (followers_by_post<=max_follwers_to_post)):
#                 print("New8")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is not None)) and((min_posts is not None) and (max_posts is None)) and((min_followers is None) and (max_followers is None)) and(total_vids>=min_posts) and (followers_by_post>=min_follwers_to_post)):
#                 print("New9")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is None)) and((min_posts is None) and (max_posts is not None)) and((min_followers is None) and (max_followers is None)) and(total_vids<=max_posts) and (followers_by_post<=max_follwers_to_post)):
#                 print("New10")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is not None)) and((min_followers is None) and (max_followers is None)) and(total_vids<=max_posts) and (followers_by_post>=min_follwers_to_post)):
#                 print("New11")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break
#             elif(((max_follwers_to_post is not None) and (min_follwers_to_post is not None)) and((min_posts is None) and (max_posts is None)) and((min_followers is None) and (max_followers is None)) and(followers_by_post>=min_follwers_to_post and followers_by_post<=max_follwers_to_post)):
#                 print("aaya24")
#                 datas={
#                     'ChannelTitle':doc["_source"]["channelTitle"],
#                     # 'thumbnail':doc["_source"]["thumbnail"],
#                     'Subscribers':doc["_source"]["SubscriberCount"],
#                     'VideoCount':doc["_source"]["VideoCount"],
#                     'Videothumbnail':doc["_source"]["Videothumbnail"],
#                     'videoTitle':doc["_source"]["videoTitle"],
#                     'Videodescription':doc["_source"]["Videodescription"],
#                     'url':doc["_source"]["url"],
#                     'comments':doc["_source"]["comments"],
#                     'likes':doc["_source"]["likecount"],
#                     'dislikes':doc["_source"]["Dislikecount"],
#                     'views':doc["_source"]["viewcount"],
                    
#                 }
#                 total_data.append(datas)
#                 break