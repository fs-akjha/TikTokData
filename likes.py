from TikTokApi import TikTokApi
api = TikTokApi()
username = "jw_anderson"
results = 30
liked_list = api.userLikedbyUsername(username, count=results)
print(liked_list)