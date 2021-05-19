#TODO campaign related Views that would call the camapign service to resolve the request  - campaign management


from app import app
from campaign.service import campaign_service
from flask import request

@app.route("/campaigns")
def data():
    result = campaign_service.list_campaign()
    return result


@app.route("/create-campaigns",methods = ['POST'])
def create():
    if request.method == "POST":
        campname=request.json['campname']
        end_date=request.json['end_date']
        company_id = request.json['company_id']
        user_id = request.json['user_id']
        result = campaign_service.create_campaign(campname,end_date,company_id\
        ,user_id)
        return result

@app.route("/delete-campaigns/<id>",methods=['DELETE'])
def delete(id):
    result = campaign_service.delete_campaign(id)
    return result

@app.route("/expire-campaigns",methods=['POST'])
def expire():
    company_id = request.json['company_id']
    user_id = request.json['user_id']
    result = campaign_service.expire_campaign(company_id,user_id)
    return result
