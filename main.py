from TikTokApi import TikTokApi
api = TikTokApi()
results = 10
hashtag = "funny"
trending = api.byHashtag(hashtag, count=results)
print(trending)