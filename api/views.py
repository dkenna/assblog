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

@csrf_exempt
def articles(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        claims = verify_token(token)
        if not claims:
            return get_400('no claims')
    except Exception as e:
        return get_401('no/bad token')
    arts = []
    for a in Article.objects.filter(user = claims['username']).order_by('-creation_date'):
        arts.append(ArticleSerializer(a).data)
    return JsonResponse(status = 200, data = arts, safe = False)

@csrf_exempt
def article(request, pk = None):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        claims = verify_token(token)
        if not claims:
            return get_400('no claims')
    except:
        return get_401('no/bad token')
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
            return get_400()
    if m == 'PUT':
        try:
            d = _json(request.body.decode('utf-8'), ['title','text'])
            try:
                a = Article.objects.filter(user = claims['username']).filter(id = pk)[0]
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
            return get_400()
    if m == 'GET':
        try:
            a = Article.objects.filter(user = claims['username']).filter(id = pk)[0]
            return JsonResponse(status = 200, data = ArticleSerializer(a).data)
        except:
            return get_404()
    if m == 'DELETE':
        try:
            a = Article.objects.filter(user = claims['username']).filter(id = pk)[0]
            a.delete()
            return JsonResponse(status = 200, data = {'status': 'ok'})
        except:
            return get_400()
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
    
        
def get_json_http_error(status,msg):
    return JsonResponse(status=status, data={
        'status': 'error',
        'error': msg
    })

@csrf_exempt
def get_404():
    return get_json_http_error(404,"not fund")
@csrf_exempt
def get_400():
    return get_json_http_error(400, "bad requesssst")

@csrf_exempt
def get_405():
    return get_json_http_error(400, "bad meth")
@csrf_exempt
def get_401(msg="forsbidden"):
    return get_json_http_error(401, msg)
