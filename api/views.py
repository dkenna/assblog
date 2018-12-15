from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from api.models import Article
from tokenizer import TokenVerifier

def verify_token(token):
    tv = TokenVerifier(token)
    return tv.verify()

@csrf_exempt
def articles(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        if not verify_token(token):
            return get_400()
    except Exception as e:
        raise e
        print('no ttoekn, disallowed')
        return get_401()
    arts = []
    for a in Article.objects.all().order_by('-creation_date'):
        arts.append({'id':a.id,'title':a.title,'text':a.text})
    return JsonResponse(status = 200, data = arts, safe = False)

@csrf_exempt
def article(request, pk = None):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        if not verify_token(token):
            return get_400()
    except:
        print('no ttoekn, disallowed')
        return get_401()
    m = request.method
    if m == 'POST':
        try:
            d = _json(request.body.decode('utf-8'), ['title','text'])
            a = Article()
            a.title = d['title']
            a.text = d['text']
            a.save()
            return JsonResponse(status = 200, data = {'status': 'ok', 'id': a.id})
        except:
            return get_400()
    if m == 'PUT':
        try:
            d = _json(request.body.decode('utf-8'), ['title','text'])
            try:
                a = Article.objects.get(id = pk)
                s = 'updated'
            except Article.DoesNotExist:
                a = Article()
                s = 'upserted'
            a.title = d['title']
            a.text = d['text']
            a.save()
            return JsonResponse(status = 200, data = {'id': a.id, 'title':a.title,'text':a.text})
        except:
            raise
            return get_400()
    if m == 'GET':
        try:
            a = Article.objects.get(id = pk)
            return JsonResponse(status = 200, data = {'id': a.id, 'title':a.title,'text':a.text})
        except:
            return get_404()
    if m == 'DELETE':
        try:
            a = Article.objects.get(id = pk)
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
