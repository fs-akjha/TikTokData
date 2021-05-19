from TikTokApi import TikTokApi
api = TikTokApi()
search_term = "funny"
hashtags = api.search_for_hashtags(search_term)
print(hashtags)