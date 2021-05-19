from .sql.models import models
from app.base import Session
from datetime import datetime
from flask import request,jsonify,make_response
from .elasticsearch.mapping import mapping
from app.base import es
from persistance.elasticsearch.mapping.youtube_search_mapping import create_index as tuh_create_index
from persistance.elasticsearch.mapping.youtube_history_mapping import create_index as tu_create_index
from .elasticsearch import schema
class CollectionSearchDAO:
    def __init__(self, model):
        self.model = model
        

    def create(self,user_id,query):
        session = Session()
        instance = session.query(self.model).filter_by(query=query,added_by_user_id=user_id).first()
        if instance:
            session.close()
            return str(instance.id)
        else:

            new_search = self.model(query=query,added_by_user_id=user_id)
            session.add(new_search)
            
            session.commit()
            session.flush()
            session.close()    
            return str(new_search.id)
    
    def list(self, **kwargs):
        session = Session()
        result = session.query(self.model).filter_by(**kwargs)
        session.close()
        return result
    
    def get_by_id(self, id):
        session = Session()
        result =  (
            session.query(self.model)
                .filter_by(added_by_user_id=id)
                .first())
        session.close()
        return result


class CompanyCollectionSearchScheduleDAO:
    def __init__(self, model):
        self.model = model
        

    def create(self,company_id,campaign_id,schedule,
        analysis_rules_id,added_by_user_id):
        session = Session()

        instance = session.query(self.model).filter_by(company_id=company_id,campaign_id=campaign_id,collection_search_id=schedule.collection_search_id,
        network_id=schedule.network_id,analysis_rules_id=analysis_rules_id,
        added_by_user_id=added_by_user_id,is_active="T").first()

        if instance :
            session.close()
            return "200"
        else:
            new_search = self.model(company_id=company_id,campaign_id=campaign_id,collection_search_id=schedule.collection_search_id,
            network_id=schedule.network_id,analysis_rules_id=analysis_rules_id,
            added_by_user_id=added_by_user_id,is_active="T")
            session.add(new_search)
            session.commit()
            session.close()
            return "200"
    
    def get_by_id(self, id):
        session = Session()
        result = (
            session.query(self.model.company_id)
                .filter_by(company_id=id))
        session.close()
        return result

    def get_by_nid(self, id,companyid):
        session = Session()
        result = (
            session.query(self.model)
                .filter_by(network_id=id,company_id=companyid))
        session.close()
        return result

    def list(self,campaign_id,added_by_user_id):
        session = Session()
        instances = session.query(self.model).filter_by(campaign_id=campaign_id,added_by_user_id=added_by_user_id).all()
        session.close()
        return instances

    def delete(self,**kwargs):
        """ A user who has added a query only he can delete that query and network associated with it.
        """
        session = Session()
        del_network = session.query(self.model).filter_by\
            (**kwargs).first()
        if del_network:
            session.delete(del_network)
            session.commit()

        session.close()    
        return "200"
        



class SocialNetworkDAO:
    def __init__(self, model):
        self.model = model

    # def get_network_id(self,network):
    #     return (session.query(self.model.id).filter_by\
    #         (name=network))

    def get_network_id(self, name):
        session = Session()
        result = (
            session.query(self.model.id).filter_by(name=name)
        )
        session.close()
        return result

    def list(self):
        session = Session()
        result = session.query(self.model).filter_by().all()
        session.close()
        return result


class CollectionSearchScheduleDAO:
    def __init__(self, model):
        self.model = model
        

    def get_by_id(self, id):
        session = Session()
        result = (
            session.query(self.model.company_id)
                .filter_by(company_id=id)
                .first())
        session.close()
        return result

    def create(self,collection_search_id,network_id,analysis_rules_id,
        collection_frequency_in_hours,added_by_user_id,is_active):
        session = Session()
        instance = session.query(self.model).filter_by(collection_search_id=collection_search_id,network_id=network_id,
        added_by_user_id=added_by_user_id,
        analysis_rules_id=analysis_rules_id,
        collection_frequency_in_hours=collection_frequency_in_hours,is_active=is_active).first()
        if instance:
            session.close()
            return instance
        else:
            new_search = self.model(collection_search_id=collection_search_id,network_id=network_id,
            added_by_user_id=added_by_user_id,
            analysis_rules_id=analysis_rules_id,
            collection_frequency_in_hours=collection_frequency_in_hours,is_active=is_active)
            session.add(new_search)
            session.commit()
            session.flush()
            session.close()
            return new_search

    def delete(self,collection_search_id,network_id):
        session = Session()
        del_network = session.query(self.model).filter_by\
            (collection_search_id=collection_search_id,network_id=network_id).first()
        if del_network:
            session.delete(del_network)
            session.commit()
        session.close()                
        return "200"

class AnalysisRuleDAO:
    def __init__(self, model):
        self.model = model
        
    
    def view(self): 
      session = Session()  
      result = session.query(self.model).filter_by().all()
      session.close()
      return result


class YoutubeEsDAO:
    def __init__(self):
        self.network = 'youtube'
    
    def create_index(self,data,index_name):
        if not es.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            res = mapping.create_index(es,index_name=index_name)
            print(res)
            return "True"
        else:
            return "False"

    def create_user(self, data):
        if not es.indices.exists(index="youtube_user_index"):
            tuh_create_index(es, index_name='youtube_user_index')

        try:
            outcome = es.index(index="youtube_user_index", doc_type='YoutubeData', body=data, request_timeout=200)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))

    def flagged_video(self,channelid,all_words):
        res = es.search(index="youtube_user_history", size=1000, body={
        "query": { "bool": {
                    "must": [
                        {
                            "query_string": {
                            "fields": ["id"],
                            "query": channelid
                        }
                        },
                        {
                        "terms": {
                        "Videodescription": all_words
                        }
                        },
                    ],
        }
        },
        "highlight": {
            "pre_tags" : ["<b>"],
            "post_tags" : ["</b>"],
        "fields": {
            "Videodescription":{"number_of_fragments" : 0}}
    }
        }
        )
        return res

class YoutubeEsHistoryDAO:

    def __init__(self):
        self.network = 'youtube'
    
    def create_index(self,data,index_name):
        if not es.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            res = mapping.create_index(es,index_name=index_name)
            print(res)
            return "True"
        else:
            return "False"

    def create_user_history(self, data):
        if not es.indices.exists(index="youtube_user_history"):
            tu_create_index(es, index_name='youtube_user_history')

        try:
            outcome = es.index(index="youtube_user_history", doc_type='YoutubeDataHistory', body=data, request_timeout=30)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))

    def get_user_history(self, channelid):
        try:
            data = es.search(index="youtube_user_history", body={"query": {"match": {'id':channelid}}},size=1000)
            return data            
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))        
            return []

class YoutubeInfluencersDAO:
    def __init__(self,model):
        self.model = model
        
    def create_influencer(self,campaign_id,approved_by_user_id,social_network,social_network_user_id,post_id,created_date,modified_date):
        session = Session()
        create_infc=self.model(campaign_id=campaign_id,approved_by_user_id=approved_by_user_id,social_network=social_network,social_network_user_id=social_network_user_id,post_id=post_id,created_date=created_date,modified_date=modified_date)
        session.add(create_infc)
        session.commit()
        session.close()
        return "200"

    def remove_influencer(self,id):
        session = Session()
        result =  (
            session.query(self.model).filter_by(id=id).one()
        )
        if(result):
            session.delete(result)
            session.commit()
            session.close()                
        return "User Removed"     

    def get_by_campid(self, campaign_id):
        session = Session()
        result = (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model)
                .filter_by(campaign_id=campaign_id)
        )
        session.close()
        return result
    
    def get_channelinfcid(self, campaign_id):
        session = Session()
        result = (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model.social_network_user_id)
                .filter_by(campaign_id=campaign_id).all()
        )
        session.close()
        return result
    
class YoutubeDenialsDAO:
    def __init__(self,model):
        self.model = model
        
    
    def create_denails(self,campaign_id,denied_by_user_id,social_network,social_network_user_id,post_id,created_date,modified_date):
        session = Session()
        create_infc=self.model(campaign_id=campaign_id,denied_by_user_id=denied_by_user_id,social_network=social_network,social_network_user_id=social_network_user_id,post_id=post_id,created_date=created_date,modified_date=modified_date)
        session.add(create_infc)
        session.commit()
        session.close()
        return "200"

    def get_by_campid(self, campaign_id):
        session = Session()
        result = (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model)
                .filter_by(campaign_id=campaign_id)
        )
        session.close()
        return result
    
    def get_channeldenid(self, campaign_id):
        session = Session()
        result = (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model.social_network_user_id)
                .filter_by(campaign_id=campaign_id).all()
        )
        session.close()
        return result

class YoutubeStopWordsDAO:
    def __init__(self,model):
        self.model = model
        self.session = Session()

    def get_all_stopwords(self):
        session = Session()
        stop_words = self.session.query(self.model).all()
        # return " OR ".join([x.word for x in stop_words if " " not in x.word])
        result=[x.word for x in stop_words]
        session.close()
        return result  

class SocialNetworkUserRemovalReasonDAO:
    def __init__(self,model):
        self.model = model
        self.session = Session()

    def create_reason(self,reason,created_date,modified_date):
        session = Session()
        createreason=self.model(reason=reason,created_date=created_date,modified_date=modified_date)
        session.add(createreason)
        session.commit()
        session.close()
        return "200"
    

    def get_reason_detail_id(self,reason):
        session = Session()
        result = (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model.id)
                .filter_by(reason=reason).first()
        )
        session.close()
        return result


class SocialNetworkUserRemovalDAO:
    def __init__(self,model):
        self.model = model
        self.session = Session()
    
    def user_removal(self,social_network_id,social_network_user_id,removed_by_user_id,social_network_user_removal_reason_id,created_date,modified_date):
        session = Session()
        create_removal_user=self.model(social_network_id=social_network_id,social_network_user_id=social_network_user_id,removed_by_user_id=removed_by_user_id,social_network_user_removal_reason_id=social_network_user_removal_reason_id,created_date=created_date,modified_date=modified_date)
        session.add(create_removal_user)
        session.commit()
        session.close()
        return "200"
    

collection_search_dao = CollectionSearchDAO(models.CollectionSearch)
company_collection_search_schedule_dao =CompanyCollectionSearchScheduleDAO(models.CompanyCollectionSearchSchedule)
collection_search_schedule_dao=CollectionSearchScheduleDAO(models.CollectionSearchSchedule)
social_network_dao = SocialNetworkDAO(models.SocialNetwork)
analysis_rule_dao = AnalysisRuleDAO(models.AnalysisRule)
youtube_user_search_dao = YoutubeEsDAO()
youtube_user_search_history_dao=YoutubeEsHistoryDAO()
youtube_influencers_dao = YoutubeInfluencersDAO(models.CampaignInfluencer)
youtube_denial_dao = YoutubeDenialsDAO(models.CampaignDeniedProspect)
youtube_stop_words_dao=YoutubeStopWordsDAO(models.StopWord)
social_network_removal_user_dao=SocialNetworkUserRemovalDAO(models.SocialNetworkUserRemoval)
social_network_removal_user_reason_dao=SocialNetworkUserRemovalReasonDAO(models.SocialNetworkUserRemovalReason)