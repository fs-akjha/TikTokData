from TikTokApi import TikTokApi
api = TikTokApi()
results = 10
username = "therock"
trending = api.byUsername(username, count=results)
print(trending)