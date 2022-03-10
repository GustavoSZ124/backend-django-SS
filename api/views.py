from django.http import HttpRequest, JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage

from api.models import Documents, Chapters, Passages, Translations

# Create your views here.

class DocumentView(View):
  def get(self, request: HttpRequest, id = -1):
    response = {}
    if(id == -1):
      try:
        documents = list(Documents.objects.filter(type='Original').values())
        response['msg'] = "Consulta Exitosa"
        response['documents'] = documents
      except Exception as e:
        print(f'Error: {e}')
        response['msg'] = "Error al consultar los documentos"
    
    return JsonResponse(response)
    
  def post(self, request: HttpRequest, id = -1):
    response = {}
    newdocument: Documents
    try:
      form = request.POST
      uploadfile = request.FILES['file']
    except Exception as e:
      print(f'Error: {e}')
      response['msg'] = "Error al leer los datos enviados"

    newdocument = Documents.create('Original',form.get('language'),form.get('title'),form.get('author'),uploadfile.name)

    if(id == -1):
      try:
        newdocument.save()
        fname = FileSystemStorage().save(f"file_{newdocument.id}.txt",uploadfile)
        print(f"File: {fname}")
        # Process File
      except Exception as e:
        print(f'Error: {e}')
        response['msg'] = "Error al guardar en la base de datos"
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
