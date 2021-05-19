from persistance.social_media_dao import collection_search_dao,company_collection_search_schedule_dao,\
                                         social_network_dao,collection_search_schedule_dao
from persistance.users_dao import user_dao,company_dao


class SearchTermService:
    def create(self,user_id,query,network,company_id,camapign_id,analysis_rule_id):
        company_fb_limit=0
        company_insta_limit=0
        company_twitter_limit=0
        company_yt_limit=0
        total_fbused=0
        network_id=0
        total_twitterused=0
        total_instaused=0
        total_ytused=0
        company_fb_used=0
        comp_id=0
        company_twitter_used=0
        company_insta_used=0
        company_yt_used=0
        networkid = social_network_dao.get_network_id(name=network)
        for nks in networkid:
            network_id=nks.id
        totalnetworks=company_collection_search_schedule_dao.get_by_nid(id=network_id,companyid=company_id).count()
        frequency = {
        "facebook":720,
        "instagram":2,
        "twitter":0,
        "youtube":720
        }
        fb_limit=company_dao.get_by_fbsid(id=company_id)
        for sm1 in fb_limit:
            company_fb_limit=sm1.facebook_limit

        insta_limit=company_dao.get_by_instagramid(id=company_id)
        for sm2 in insta_limit:
            company_insta_limit=sm2.instagram_limit

        twitter_limit=company_dao.get_by_twitterid(id=company_id)
        for sm3 in twitter_limit:
            company_twitter_limit=sm3.twitter_limit

        yt_limit=company_dao.get_by_ytid(id=company_id)
        for sm4 in yt_limit:
            company_yt_limit=sm4.youtube_limit

        total_fbused=company_dao.get_by_totalfbusedid(id=company_id)
        for data1 in total_fbused:
            company_fb_used=data1.facebook_searches_used
        
        total_twitterused=company_dao.get_by_totaltwitterusedid(id=company_id)
        for data2 in total_twitterused:
            company_twitter_used=data2.twitter_searches_used

        total_instaused=company_dao.get_by_totalinstagramusedid(id=company_id)
        for data3 in total_instaused:
            company_insta_used=data3.instagram_searches_used

        company_yt_used=company_dao.get_by_totalytusedid(id=company_id)
        for data4 in company_yt_used:
            company_yt_used=data4.youtube_searches_used
        
        if((network_id==1) and (totalnetworks <company_twitter_limit) and (company_twitter_used<=company_twitter_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_twitterusedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        elif((network_id==2) and (totalnetworks <company_insta_limit) and (company_insta_used<=company_insta_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_instausedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        elif((network_id==3) and (totalnetworks <company_yt_limit) and (company_yt_used<=company_yt_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_ytusedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        
        elif((network_id==4) and (totalnetworks <company_fb_limit) and (company_fb_used<=company_fb_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_fbusedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        else:
            return{"message":"Limit Reached"}


    def create_searches(self,user_id,query,network,company_id,camapign_id,analysis_rule_id):
        company_fb_limit=0
        company_insta_limit=0
        company_twitter_limit=0
        company_yt_limit=0
        total_fbused=0
        network_id=[]
        nwks=0
        total_twitterused=0
        total_instaused=0
        total_ytused=0
        company_fb_used=0
        comp_id=0
        company_twitter_used=0
        company_insta_used=0
        company_yt_used=0
        collection_search_id= collection_search_dao.create(user_id,query)
        for nets in network:
            nwks = social_network_dao.get_network_id(nets)
            network_id.append(nwks)
        for i in range(0, len(network_id)):
                        network_id[i] = int(network_id[i])
        for nks in network_id:
            network_id=nks.id
        totalnetworks=company_collection_search_schedule_dao.get_by_nid(id=network_id,companyid=company_id).count()
        frequency = {
        "facebook":720,
        "instagram":2,
        "twitter":0,
        "youtube":720
        }
        fb_limit=company_dao.get_by_fbsid(id=company_id)
        for sm1 in fb_limit:
            company_fb_limit=sm1.facebook_limit

        insta_limit=company_dao.get_by_instagramid(id=company_id)
        for sm2 in insta_limit:
            company_insta_limit=sm2.instagram_limit

        twitter_limit=company_dao.get_by_twitterid(id=company_id)
        for sm3 in twitter_limit:
            company_twitter_limit=sm3.twitter_limit

        yt_limit=company_dao.get_by_ytid(id=company_id)
        for sm4 in yt_limit:
            company_yt_limit=sm4.youtube_limit

        total_fbused=company_dao.get_by_totalfbusedid(id=company_id)
        for data1 in total_fbused:
            company_fb_used=data1.facebook_searches_used
        
        total_twitterused=company_dao.get_by_totaltwitterusedid(id=company_id)
        for data2 in total_twitterused:
            company_twitter_used=data2.twitter_searches_used

        total_instaused=company_dao.get_by_totalinstagramusedid(id=company_id)
        for data3 in total_instaused:
            company_insta_used=data3.instagram_searches_used

        company_yt_used=company_dao.get_by_totalytusedid(id=company_id)
        for data4 in company_yt_used:
            company_yt_used=data4.youtube_searches_used


        if((network_id==1) and (totalnetworks <company_twitter_limit) and (company_twitter_used<=company_twitter_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_twitterusedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        elif((network_id==2) and (totalnetworks <company_insta_limit) and (company_insta_used<=company_insta_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_instausedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        elif((network_id==3) and (totalnetworks <company_yt_limit) and (company_yt_used<=company_yt_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_ytusedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        
        elif((network_id==4) and (totalnetworks <company_fb_limit) and (company_fb_used<=company_fb_limit)):
            collection_search_id= collection_search_dao.create(user_id,query)
            collection_frequency_in_hours =frequency[network]
            schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
            company_dao.get_by_fbusedid(id=company_id)
            search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
            analysis_rule_id,user_id)
            return {"status":search}
        else:
            return{"message":"Limit Reached"}

        # collection_frequency_in_hours =frequency[network]
        # schedule = collection_search_schedule_dao.create(collection_search_id,network_id,analysis_rule_id,collection_frequency_in_hours,user_id,"T")
        # search=company_collection_search_schedule_dao.create(company_id,camapign_id,schedule,
        # analysis_rule_id,user_id)
        # return {"status":search}



    def list(self, user_id, campaign_id):
        network_instances = social_network_dao.list()

        collection_search_instances = collection_search_dao.list(**{"added_by_user_id":user_id})

        query_mapping = {x.id:x.query for x in collection_search_instances}
        network_mapping = {x.id:x.name for x in network_instances}

        response ={}
        company_collection_search_schedule_instances=company_collection_search_schedule_dao.list(campaign_id, user_id)

        for x in company_collection_search_schedule_instances:
            if not query_mapping[x.collection_search_id] in response:
                response[query_mapping[x.collection_search_id]] = []
            response[query_mapping[x.collection_search_id]].append(
                network_mapping[x.network_id]
            )
        return response

search_term_service = SearchTermService()