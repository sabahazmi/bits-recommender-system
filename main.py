from fastapi import FastAPI
from recommend import Recommend

app = FastAPI(docs_url="/api_doc", redoc_url=None)


@app.get("/bits/popular/")
def get_recommendations():
    try:
        print('Popularity Based')
        recommended = Recommend.popular_recommend()
        return {'data': recommended}
    except:
        return {'data': 'Error ❗❗❗'}

@app.get("/bits/user/{user_id}")
def get_recommendations(user_id: int):
    try:
        print('User Based')
        recommended = Recommend.user_based_recommend(user_id)
        return {'data': recommended}
    except:
        print('User not found, popularity called')
        recommended = Recommend.popular_recommend()
        return {'data': recommended}


@app.get("/bits/item/{bits_id}")
def get_recommendations(bits_id: int):
    try:
        print('Item Based')
        recommended = Recommend.item_based_recommend(bits_id)
        return {'data': recommended}
    except:
        print('Item not found, popularity called')
        recommended = Recommend.popular_recommend()
        return {'data': recommended}
