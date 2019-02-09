from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from api.models import Article
from tokenizer import TokenVerifier
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'user', 'creation_date')

def verify_token(token):
    tv = TokenVerifier(token)
    return tv.verify()

def get_articles(username):
    return Article.objects.filter(user = username).order_by('-creation_date')

def get_article(username, pk):
    return get_articles(username).filter(id = pk)[0]

@csrf_exempt
def articles(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        claims = verify_token(token)
        if not claims:
            return get_400(request, 'no claims')
    except Exception as e:
        return get_401(request, 'no/bad token')
    arts = []
    for a in get_articles(claims['username']):
        arts.append(ArticleSerializer(a).data)
    return JsonResponse(status = 200, data = arts, safe = False)

@csrf_exempt
def article(request, pk = None):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        claims = verify_token(token)
        if not claims:
            return get_400(request, 'no claims')
    except:
        return get_401(request, 'no/bad token')
    m = request.method
    if m == 'POST':
        try:
            d = _json(request.body.decode('utf-8'), ['title','text'])
            a = Article()
            a.title = d['title']
            a.text = d['text']
            a.user = claims['username']
            a.save()
            return JsonResponse(status = 200, data = ArticleSerializer(a).data)
        except:
            return get_400(request)
    if m == 'PUT':
        try:
            d = _json(request.body.decode('utf-8'), ['title','text'])
            try:
                a = get_article(claims['username'], pk)
                s = 'updated'
            except:
                a = Article()
                s = 'upserted'
            a.title = d['title']
            a.text = d['text']
            a.user = claims['username']
            a.save()
            return JsonResponse(status = 200, data = ArticleSerializer(a).data)
        except:
            return get_400(request)
    if m == 'GET':
        try:
            a = get_article(claims['username'], pk)
            return JsonResponse(status = 200, data = ArticleSerializer(a).data)
        except:
            return get_404(request)
    if m == 'DELETE':
        try:
            a = get_article(claims['username'], pk)
            a.delete()
            return JsonResponse(status = 200, data = {'status': 'ok'})
        except:
            return get_400(request)
        return JsonResponse(status = 204, data = {})
    
def _json(body,keys):
    """load json and ensure all keys are present"""
    try:
        payload = json.loads(body)
        for i in keys:
            payload[i]
        return payload
    except Exception as e:
        print("parsing json failed.")
        raise e
    

def get_json_http_error(request, status,msg):
    return JsonResponse(status=status, data={
        'status': 'error',
        'error': msg
    })

@csrf_exempt
def get_404(request, msg="not fund"):
    return get_json_http_error(request, 404, msg)
@csrf_exempt
def get_400(request, msg="bad requesssst"):
    return get_json_http_error(request, 400, msg)

@csrf_exempt
def get_405(request, msg="bad meth"):
    return get_json_http_error(request, 405, msg)
@csrf_exempt
def get_401(request, msg="forsbidden"):
    return get_json_http_error(request, 401, msg)
