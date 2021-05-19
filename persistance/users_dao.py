from .sql.models import models
from app.base import Session


class UserDAO:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        session = Session()
        result = session.query(self.model).all()
        session.close()
        return result

    def get_by_username(self, username):
        session = Session()
        result = (
            session.query(self.model)
                .filter_by(get_by_username=username)                                                                                                                                                                                                                                                                                                                                                                                                
                .first()
        )
        session.close()
        return result

    def get_by_id(self, id):
        session = Session()
        result =  (
            session.query(self.model)
                .filter_by(id=id)
                .first()
        )
        session.close()
        return result

    def get_by_cid(self, company_id):
        session = Session()
        result =  (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model)
                .filter_by(company_id=company_id)
        )
        session.close()
        return result


    def get_by_email(self, email_address):
        session = Session()
        result =  (
            session.query(self.model)
                .filter_by(email_address=email_address)
                .first()
        )
        session.close()
        return result


    def create_new_user(self,email_address,hashed_password,name,role,created_date,modified_date,company_id):
        session = Session()
        new_user = self.model(email_address=email_address,hashed_password=hashed_password,name=name,role=role,created_date=created_date,modified_date=modified_date,company_id=company_id)
        session.add(new_user)
        session.commit()
        session.close()
        return "200"

    def get_all_company(self):
        session = Session()
        result =  session.query(self.model).all()
        session.close()
        return result

class CompanyDAO:
    def __init__(self, model):
        self.model = model

    def get_all_company(self):
        session = Session()
        result =  session.query(self.model).all()
        session.close()
        return result

    def create_new_company(self,name,seat_limit,campaign_limit,facebook_limit,instagram_limit,twitter_limit,youtube_limit,created_date,modified_date,added_by_user_id):
        session = Session()
        create_company=self.model(name=name,seat_limit=seat_limit,campaign_limit=campaign_limit,facebook_limit=facebook_limit,instagram_limit=instagram_limit,twitter_limit=twitter_limit,youtube_limit=youtube_limit,created_date=created_date,modified_date=modified_date,added_by_user_id=added_by_user_id)
        session.add(create_company)
        session.commit()
        session.close()
        return "200"

    def get_by_id(self, id):
        session = Session()
        result =  (
            session.query(self.model).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_seatsid(self, id):
        session = Session()
        result =  (
            session.query(self.model.seat_limit).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_fbsid(self, id):
        session = Session()
        result =  (
            session.query(self.model.facebook_limit).filter_by(id=id)
        )
        session.close()
        return result
    
    def get_by_instagramid(self, id):
        session = Session()
        result =  (
            session.query(self.model.instagram_limit).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_twitterid(self, id):
        session = Session()
        result =  (
            session.query(self.model.twitter_limit).filter_by(id=id)
        )
        session.close()
        return result
    
    def get_by_ytid(self, id):
        session = Session()
        result =  (
            session.query(self.model.youtube_limit).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_totalseatsid(self, id):
        session = Session()
        result =  (
            session.query(self.model.seats_used).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_totalfbusedid(self, id):
        session = Session()
        result =  (
            session.query(self.model.facebook_searches_used).filter_by(id=id)
        )

    def get_by_totalinstagramusedid(self, id):
        session = Session()
        result =  (
            session.query(self.model.instagram_searches_used).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_totaltwitterusedid(self, id):
        session = Session()
        result =  (
            session.query(self.model.twitter_searches_used).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_totalytusedid(self, id):
        session = Session()
        result =  (
            session.query(self.model.youtube_searches_used).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_seatusedid(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'seats_used':(self.model.seats_used)+1})
            session.commit()
            session.close()
            return True

    def get_by_fbusedid(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'facebook_searches_used':(self.model.facebook_searches_used)+1})
            session.commit()
            session.close()
            return True

    def get_by_twitterusedid(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'twitter_searches_used':(self.model.twitter_searches_used)+1})
            session.commit()
            session.close()
            return True

    def get_by_instausedid(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'instagram_searches_used':(self.model.instagram_searches_used)+1})
            session.commit()
            session.close()
        
            return True

    def get_by_ytusedid(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'youtube_searches_used':(self.model.youtube_searches_used)+1})
            session.commit()
            session.close()
        
            return True
    

    def get_by_campaignusedid(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'campaigns_used':(self.model.campaigns_used)+1})
            session.commit()
            session.close()
        
            return True

    def delete_campaignusedid(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'campaigns_used':(self.model.campaigns_used)-1})
            session.commit()
            session.close()
        
            return True

    def get_by_campaignsid(self, id):
        session = Session()    
        result =  (
            session.query(self.model.campaign_limit).filter_by(id=id)
        )
        session.close()
        return result

    def get_by_totalcampaignsid(self, id):
        session = Session()
        result =  (
            session.query(self.model.campaigns_used).filter_by(id=id)
        )
        session.close()
        return result


class MessageDAO:
    def __init__(self, model):
        self.model = model

    def get_all_messages(self):
        session = Session()
        result =  session.query(self.model).all()
        session.close()
        return result

    def create_new_message(self,campaign_id,created_by_user_id,message_template,created_date,modified_date):
        session = Session()
        create_messages=self.model(campaign_id=campaign_id,created_by_user_id=created_by_user_id,message_template=message_template,created_date=created_date,modified_date=modified_date)
        session.add(create_messages)
        session.commit()
        session.close()
        
        return "200"

class BatchDAO:
    def __init__(self, model):
        self.model = model
        

    def get_all_batches(self):
        session = Session()
        # return session.query(self.model).join(models.MarketplaceInvitation).all()
        result =  session.query(self.model).all()
        session.close()
        return result

    def create_new_batch(self,created_by_user_id,batch_status,send_date,subject,created_date,modified_date,desired_batch_size):
        session = Session()
        create_batches=self.model(created_by_user_id=created_by_user_id,batch_status=batch_status,send_date=send_date,subject=subject,created_date=created_date,modified_date=modified_date,desired_batch_size=desired_batch_size)
        session.add(create_batches)
        session.commit()
        session.close()
        
        return "200"

user_dao = UserDAO(models.User)
company_dao=CompanyDAO(models.Company)
message_dao=MessageDAO(models.CampaignMessageTemplate)
batch_dao=BatchDAO(models.MarketplaceInvitationBatch)