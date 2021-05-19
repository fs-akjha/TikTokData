#TODO Campaign service, all the business logic are all defined here and uses the DAO to fetch relevent data from DB

from persistance.campaign_dao import campaign_dao
from persistance.users_dao import user_dao,company_dao,message_dao,batch_dao
from .serializers import campaign_schema, campaigns_schema

class CampaignService:
    def list_campaign(self):
        all_campaigns = campaign_dao.get_all_active_campaign()
        result = campaigns_schema.dump(all_campaigns)
        return {"campaign": result}

    def create_campaign(self,campname,end_date,company_id,user_id):
        company_campaignlimit=0
        total_campaignused=0
        company_campaign_used=0
        all_campaigns = campaign_dao.get_all_active_campaign()
        result = campaigns_schema.dump(all_campaigns)
        totalcampaigns=campaign_dao.get_campaignsby_cid(company_id=company_id).count()
        totalcompanies=company_dao.get_by_id(id=company_id).count()
        campaign_result=company_dao.get_by_campaignsid(id=company_id)
        for data1 in campaign_result:
            company_campaignlimit=data1.campaign_limit
        total_campaignused=company_dao.get_by_totalcampaignsid(id=company_id)
        for data3 in total_campaignused:
            company_campaign_used=data3.campaigns_used
        if((totalcampaigns<company_campaignlimit) and (company_campaign_used <=company_campaignlimit)):
            company_dao.get_by_campaignusedid(id=company_id)
            create_camp = campaign_dao.create_campaign(campname,end_date,company_id,user_id)
            return {"status":create_camp}
        else:
            return{"message":"Campaign Limit Reached"}

    def delete_campaign(self,id):
        companyid=campaign_dao.get_campaignsby_id(id=id)
        comp_id=0
        for cid in companyid:
            comp_id=cid.company_id
        company_dao.delete_campaignusedid(id=comp_id)
        delete_camp = campaign_dao.delete_campaign(id)
        return {"status":"200"}

    def expire_campaign(self,company_id,user_id):
        expire_camp = campaign_dao.expire_campaign(company_id,user_id)
        return {"status":expire_camp}


campaign_service = CampaignService()