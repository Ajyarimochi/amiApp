from django.shortcuts import render
from django.http import HttpResponse
from .models import Coupon #Couponクラスをインポート
from django.db.models import Q
import json

def coupon(request): 

    coupons = [] #複数のレコードを辞書型として格納するための配列を用意
    if 'coupon_store' in request.GET: #リクエストパラメータで店舗を指定された場合の処理
        coupon_store = request.GET['coupon_store']
        #data = Coupon.objects.filter(store=coupon_store) #リクエストされた店舗と全店で使えるクーポンを取得
        data = Coupon.objects.filter(Q(store=coupon_store) | Q(store='全店')) #リクエストされた店舗と全店で使えるクーポンを取得
    else: #リクエストパラメータが無い場合は全てのクーポンを返す
        data = Coupon.objects.all()

    for record in data: #for文を使い1レコードずつ辞書型に変換
        params = {
            'coupon_code':str(record.code), #個々のレコードはdata型なのでString型にキャストする
            'coupon_benefits':str(record.benefit),
            'coupon_explanation':str(record.explanation),
            'coupon_store':str(record.store),
            'coupon_start':str(record.start),
            'coupon_deadline':str(record.deadline),
            'coupon_status':str(record.status),
            }
        coupons.append(params) #辞書型にしたレコードを配列に格納

    json_str = json.dumps(coupons, ensure_ascii=False, indent=2) #辞書型にした複数のレコードを格納した配列を渡す
    return HttpResponse(json_str)
