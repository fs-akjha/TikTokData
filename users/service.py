from persistance.users_dao import user_dao,company_dao,message_dao,batch_dao
from .serializers import user_schema, users_schema,companies_schema,company_schema,message_schema,messages_schema,batch_schema,batches_schema

class UserService:
    def list_users(self):
        all_users = user_dao.get_all()
        result = users_schema.dump(all_users)
        return ({'users':result})

    def filtered_users(self,email_address):
        user=user_dao.get_by_email(email_address)
        return user

    def filtered_users_id(self,id):
        userid=user_dao.get_by_id(id)
        result = users_schema.dump(userid)
        return result

    def filtered_users_by_cid(self,company_id):
        cuserid=user_dao.get_by_cid(company_id)
        result = users_schema.dump(cuserid)
        return ({'users':result})


    def create_user(self,email_address,hashed_password,name,role,created_date,modified_date,company_id):
        company_seatlimit=0
        totalusers=0
        company_seats_used=0
        total_seatsused=0
        totalusers=user_dao.get_by_cid(company_id=company_id).count()
        totalcompanies=company_dao.get_by_id(id=company_id).count()
        seat_result=company_dao.get_by_seatsid(id=company_id)
        for data1 in seat_result:
            company_seatlimit=data1.seat_limit
        total_seatsused=company_dao.get_by_totalseatsid(id=company_id)
        for data3 in total_seatsused:
            company_seats_used=data3.seats_used
        if((totalusers<company_seatlimit) and (company_seats_used <=company_seatlimit)):
            company_dao.get_by_seatusedid(id=company_id)
            create_user = user_dao.create_new_user(email_address,hashed_password,name,role,created_date,modified_date,company_id)
            return {"status":create_user}
        else:
            return{"message":"Seat Limit Reached"}

class CompanyService:
    def list_companies(self):
        all_companies=company_dao.get_all_company()
        result=companies_schema.dump(all_companies)
        return ({'users':result})
    
    def create_company(self,name,seat_limit,campaign_limit,facebook_limit,instagram_limit,twitter_limit,youtube_limit,created_date,modified_date,added_by_user_id):
        create_company=company_dao.create_new_company(name,seat_limit,campaign_limit,facebook_limit,instagram_limit,twitter_limit,youtube_limit,created_date,modified_date,added_by_user_id)
        return {"status":create_company}

    def show_one_company(self,id):
        companyid=company_dao.get_by_id(id)
        result = companies_schema.dump(companyid)
        return ({'users':result})

class MessageService:
    def create_message_template(self,campaign_id,created_by_user_id,message_template,created_date,modified_date):
        create_message=message_dao.create_new_message(campaign_id,created_by_user_id,message_template,created_date,modified_date)
        return {"status":create_message}

    def list_messages(self):
        all_messages=message_dao.get_all_messages()
        result=messages_schema.dump(all_messages)
        return ({'data':result})


class BatchService:
    def list_batches(self):
        all_batches=batch_dao.get_all_batches()
        result=batches_schema.dump(all_batches)
        return ({'data':result})

    def create_batch(self,created_by_user_id,batch_status,send_date,subject,created_date,modified_date,desired_batch_size):
        create_batches=batch_dao.create_new_batch(created_by_user_id,batch_status,send_date,subject,created_date,modified_date,desired_batch_size)
        return {"status":create_batches}

user_service = UserService()
company_service=CompanyService()
message_service=MessageService()
batch_service=BatchService()