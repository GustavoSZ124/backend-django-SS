from django.http import HttpRequest, JsonResponse
from django.views import View

# Create your views here.

class DocumentView(View):
  def get(self, request: HttpRequest, id = -1):
    response = {}
    response['msg'] = "Mensaje"
    return JsonResponse(response)
    
  def post(self, request: HttpRequest, id = -1):
    response = {}
    response['msg'] = "Mensaje"
    return JsonResponse(response)

  def delete(self, request: HttpRequest):
    response = {}
    response['msg'] = "Mensaje"
    return JsonResponse(response)
    
class TranslationView(View):
  def get(self, request: HttpRequest, id = -1):
    response = {}
    response['msg'] = "Mensaje"
    return JsonResponse(response)
    
  def post(self, request: HttpRequest, id = -1):
    response = {}
    response['msg'] = "Mensaje"
    return JsonResponse(response)

  def delete(self, request: HttpRequest):
    response = {}
    response['msg'] = "Mensaje"
    return JsonResponse(response)
