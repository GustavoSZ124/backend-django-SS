from pathlib import Path
from django.conf import settings
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
    else:
      document = Documents.objects.get(id = id)
      changes = document.changes(newdocument)
      print(f"changes: {changes}")
      if(not changes[0]):
        for i,val in enumerate(changes[2]):
          setattr(document,changes[1][i],val)
          print(f'attr list: {changes[1]}')
          print(f'update document: {document}')
          document.save(update_fields=changes[1])

      fpath = Path(settings.MEDIA_ROOT / f"file_{id}.txt")
      if(uploadfile.size != 0 and fpath.exists()):
        fpath.unlink()
        fname = FileSystemStorage().save(f"file_{document.id}.txt",uploadfile)
        print(f"File: {fname}")
        # Process File
    return JsonResponse(response)

  def delete(self, request: HttpRequest, id):
    response = {}
    response['msg'] = "Mensaje"

    try:
      Documents.objects.filter(id = id).delete()
      file = Path(settings.MEDIA_ROOT / f"file_{id}.txt")
      if(file.exists()):
        file.unlink()
      response['msg'] = "Documento Eliminado"
    except Exception as e:
      print(f'Error: {e}')
      response['msg'] = "Error al borrar el documento"

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
