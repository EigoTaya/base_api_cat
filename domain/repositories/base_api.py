from os import access
from domain.entities.access_info import AccessInfo
import requests
import sys

class BaseApi:
    __api_url = "https://api.thebase.in/1/"


    def get_token(self, access_info):
        path = "oauth/token"
        payload = {
            'grant_type' : access_info.grant_type,
            'client_id' : access_info.client_id,
            'client_secret' : access_info.client_secret,
            'code' : access_info.code,
            'redirect_uri' : access_info.redirect_uri,
        }

        r = requests.post(self.__api_url + path, data=payload)

        # TODO エラーハンドラを賢くしたい
        if 'error' in r.json():
            print('[access token]')
            print(r.json()['error_description'])
            sys.exit()

        return r.json()['access_token']


    # start_ordered	注文日時はじめ yyyy-mm-dd または yyyy-mm-dd hh:mm:ss (任意)
    # end_ordered	注文日時おわり yyyy-mm-dd または yyyy-mm-dd hh:mm:ss (任意)
    # limit	リミット (任意 デフォルト: 20, MAX: 100)
    # offset	オフセット (任意 デフォルト: 0)
    def get_orders(self, access_info, start=None, end=None,
                    limit=100, offset=0):
        path = "orders"
        payload = {
            'limit' : limit,
            'offset' : offset,
        }
        if start is not None:
            payload['start_ordered'] = start
        if end is not None:
            payload['end_ordered'] = end

        r = requests.get(self.__api_url + path, params=payload, 
            headers={"Authorization": 'Bearer ' + access_info.access_token})

        if 'error' in r.json():
            print('[order list]データ取得できませんでした．')
            sys.exit()

        return r.json()['orders']

    def get_order_detail(self, access_info, unique_key=None):
        path = 'orders/detail/'
        if unique_key is None:
            print('[order details]ユニークキーの指定をしてください．')
            sys.exit()

        r = requests.get(self.__api_url + path + unique_key,
                headers={"Authorization": 'Bearer ' + access_info.access_token})

        r_json = r.json()
        if 'error' in r_json:
            print('[order details]注文の詳細情報が見つかりません．')
            sys.exit()

        return r_json


    def get_categories(self, access_info):
        path = 'categories'

        r = requests.post(
            self.__api_url + path,
            headers={"Authorization": 'Bearer ' + access_info.access_token}
        )

        categories = r.json()
        if 'error' in categories:
            print('[categories list]データを取得できませんでした．')
            sys.exit()

        return categories['categories']

    def get_item_cat_detail(self, access_info, item_id):
        path = 'item_categories/detail/'

        r = requests.get(self.__api_url+ path + (item_id),
                            headers={"Authorization": 'Bearer ' + access_info.access_token})

        item_cats = r.json()
        if 'error' in item_cats:
            if item_cats['error'] == 'bad_item_id':
                return {'location': 'item category', 'message': '不正なアイテムidです．'}
            else:
                print('[item categories]商品のカテゴリ情報が見つかりません．')
                sys.exit()

        return item_cats
