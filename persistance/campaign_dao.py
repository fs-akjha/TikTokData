#campaign DAOs that interacts with database all services should use only the daos to interact with the db
from .sql.models import models
from app.base import Session
from datetime import timedelta,datetime
from sqlalchemy import and_

class CampaignDAO:
    def __init__(self, model):
        self.model = model
        

    def get_all(self):
        session = Session()
        result = session.query(self.model).all()
        session.close()
        return result

    def get_all_active_campaign(self):
        session = Session()
        result = (
            session.query(self.model)
                .filter_by(status='active')
                .all()
        )
        session.close()
        return result


    def create_campaign(self,campname,end_date,company_id,user_id):
        session = Session()
        new_campaign = self.model(name=campname,end_date=end_date\
            ,company_id=company_id,created_by_user_id=user_id)
        totalcampaigns=session.query(self.model).filter_by(company_id=company_id)
        session.add(new_campaign)
        session.commit()
        session.close()
        return "200"

    def get_campaignsby_cid(self, company_id):
        session = Session()
        result =  (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model)
                .filter_by(company_id=company_id)
        )
        session.close()
        return result
    
    def get_campaignsby_id(self, id):
        session = Session()
        result =  (                                                                                                                                                                                                                                                                                                                                                                                                
            session.query(self.model.company_id)
                .filter_by(id=id)
        )
        session.close()
        return result

    def get_by_totalinfcinc_id(self, id):
            session = Session()
            session.query(self.model).filter_by(id=id).update({'total_influencers':(self.model.total_influencers)+1})
            session.commit()
            session.close()
            return True

        
    def delete_campaign(self,id):
        session = Session()
        del_campaign = session.query(self.model).filter_by\
            (id=id).one()
        session.delete(del_campaign)
        session.commit()
        session.close()
        return "200"

    def expire_campaign(self,company_id,user_id):
        session = Session()
        expire_camp = session.query(self.model).filter(and_
        (self.model.company_id==company_id,
        self.model.created_by_user_id==user_id,self.model.end_date
        <datetime.now())).update(
            {self.model.status:'inactive'}
        )
        session.commit()
        session.close()
        return "200"

campaign_dao = CampaignDAO(models.Campaign)