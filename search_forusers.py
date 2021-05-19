from TikTokApi import TikTokApi
api = TikTokApi()
search_term = "Joe"
users = api.search_for_users(search_term)
print(users)