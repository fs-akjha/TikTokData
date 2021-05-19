import json, os
def create_index(es_object, index_name='youtube_user_index'):
    file_path = os.path.normpath(os.getcwd())+'/persistance/elasticsearch/json/youtube-search-template.json'
    created = False
    # index settings
    with open(file_path) as f:
        settings = json.load(f)
    try:
        if not es_object.indices.exists(index_name):
            res = es_object.indices.create(
                index=index_name, body=settings)
            print(res)
        created = True
    except Exception as ex:
        print(str(ex))
        created=False
    finally:
        return created