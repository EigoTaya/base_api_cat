# %%
from operator import index
import pandas as pd
from pandas import json_normalize
import copy
import os
import PySimpleGUI as sg

from domain.entities.access_info import AccessInfo
from domain.repositories.base_api import BaseApi
from domain.interfaces.gui import GUI
from utils.file_io import FileRepo

file_repo = FileRepo()
gui = GUI()
api_repo = BaseApi()

# %%
# guiを表示させて，認証コードや日付を入力
input = gui.display_gui()
info = AccessInfo(file_repo.resource_path('db/setting.json'))
# info = AccessInfo('./db/setting.json')
info.code = input['code']

# %%
# アクセストークン取得
result = {'orders': []}
info.access_token = api_repo.get_token(access_info=info)

# 注文情報の取得
orders = api_repo.get_orders(access_info=info, start=input['start'], end=input['end'])
for order in orders:
    details = api_repo.get_order_detail(access_info=info, unique_key=order['unique_key'])

    # 個々の注文商品を別行に分離
    d = details['order']

    order_items = d['order_items']
    del d['order_items']
    for order_item in order_items:
        for key in order_item:
            d[key] = order_item[key]
        result['orders'].append(copy.deepcopy(d))

# カテゴリ情報取得
categories = api_repo.get_categories(access_info=info)

# %%
# カテゴリと商品を対応付け
for order in result['orders']:
    item_cats = api_repo.get_item_cat_detail(access_info=info, item_id=str(order['item_id']))

    if 'message' in item_cats:
        print('[warning]' + item_cats['message'])
        continue

    if len(item_cats['item_categories']) >= 2:
        print('[warning] 商品カテゴリが複数付与されています')

    if len(item_cats['item_categories']) == 0:
        print('[warning] カテゴリが付与されていない商品が存在します')
        continue

    category_id = item_cats['item_categories'][0]['category_id']

    for category in categories:
        if category['category_id'] == category_id:
            order['category_name'] = category['name']
            break

# %%
col_names = ['category_name', 'order_receiver.last_name', 'order_receiver.first_name',
'order_receiver.prefecture', 'order_receiver.address', 'order_receiver.address2',
'tel', 'remark', 'title', 'price', 'amount', 'item_total', 'consumption_tax_rate', 'delivery_date', 'delivery_time_zone', 'ordered']


# if not os.path.exists(file_repo.resource_path('outputs')):
#     os.mkdir(file_repo.resource_path('outputs'))

# all出力
df = json_normalize(result['orders'])
df = df.loc[:, col_names]
df['ordered_date'] = pd.to_datetime(df['ordered'], unit='s')
# df.to_csv(file_repo.resource_path('outputs/all.csv'), encoding='shift-jis', index=False)
df.to_csv(input['filepath'] + '/all.csv', encoding='shift-jis', index=False)

# カテゴリごとに出力
valid_categories = df['category_name'].dropna().unique().tolist()
for c in valid_categories:
    df_tmp = df[df['category_name'] == c]
    # df_tmp.to_csv(file_repo.resource_path('./outputs/' + str(c) + '.csv'), encoding='shift-jis', index=False)
    df_tmp.to_csv(input['filepath'] + '/' + str(c) + '.csv', encoding='shift-jis', index=False)

# print(file_repo.resource_path('outputs/all.csv'))

# %%
