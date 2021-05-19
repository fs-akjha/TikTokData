from TikTokApi import TikTokApi
api = TikTokApi()
search_term = "Little Bus"
music = api.search_for_music(search_term)
print(music)