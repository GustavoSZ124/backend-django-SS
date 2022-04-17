from pathlib import Path
from django.conf import settings
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage

from api.models import Documents, Chapters, Passages, Translations
from api.utils import processFile

# Create your views here.

class DocumentView(View):
  # The GET method receives an option parameter to respond to two urls
  # documents/: If the route does not have an id, the Documents table is consulted
  # and send as a response an array with all the documents
  # documents/<int:id>: if the route has an id, the specific document is consulted
  # the chapters and passages that make it up, and they are sent as a response
  # the response is in json format
  def get(self, request: HttpRequest, id = -1):
    response = {}
    if(id == -1):
      try:
        documents = list(Documents.objects.values())
        response['msg'] = "Consulta Exitosa"
        response['documents'] = documents
      except Exception as e:
        print(f'Error: {e}')
        response['msg'] = "Error al consultar los documentos"
    else:
      document: Documents = Documents.objects.get(id = id)
      chapters = Chapters.objects.filter(document = document)
      response['original'] = {'document': model_to_dict(document), 'chapters': list(chapters.values())}

      for i in range(len(chapters)):
        passages = list(Passages.objects.filter(chapter = chapters[i]).values())
        response['original']['chapters'][i]['passages'] = passages

      translations: Translations = Translations.objects.filter(original = document)
      response['translations'] = []

      for i in range(len(translations)):
        document: Documents = translations[i].translated
        chapters = Chapters.objects.filter(document = document)
        response['translations'].append({
          'document': model_to_dict(document),
          'chapters': list(chapters.values()),
        })

        for j in range(len(chapters)):
          passages = list(Passages.objects.filter(chapter = chapters[j]).values())
          response['translations'][i]['chapters'][j]['passages'] = passages

    return JsonResponse(response)
    
  # The POST method receives an optional parameter to respond to two urls
  # documents/: If the route does not have an id, a new record is created in the database
  # documents/<int:id>: if the route has id, the modified fields are checked
  # and they are updated in the database, as well as saving the new document if there is one
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
        processFile(newdocument,fname)
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
        Chapters.objects.filter(document = document).delete()
        processFile(document,fname)

    response['msg'] = "Documento Guardado"
    return JsonResponse(response)

  # The DELETE method receives as a parameter the id of the document to be deleted
  # is deleted from the database and the respective file is deleted
  def delete(self, request: HttpRequest, id):
    response = {}
    try:
      Documents.objects.filter(id = id).delete()
      file = Path(settings.MEDIA_ROOT / f"file_{id}.txt")
      if(file.exists()):
        file.unlink()
      response['msg'] = "Documento Eliminado"
    except Exception as e:
      print(f'Error: {e}')
      response['msg'] = "Error al borrar el documento"

    response['msg'] = "Documento Eliminado"
    return JsonResponse(response)
    
class TranslationView(View):
  def get(self, request: HttpRequest, id = -1):
    response = {}
    if(id == -1):
      try:
        documents = list(Documents.objects.values())
        response['msg'] = "Consulta Exitosa"
        response['documents'] = documents
      except Exception as e:
        print(f'Error: {e}')
        response['msg'] = "Error al consultar los documentos"
    else:
      translation: Translations = Translations.objects.get(translated = id)
      response['msg'] = "Consulta Exitosa"
      response['document'] = model_to_dict(translation.original)

    return JsonResponse(response)
    
  def post(self, request: HttpRequest, id = -1):
    response = {}
    newtranslation: Documents
    document: Documents
    try:
      form = request.POST
      uploadfile = request.FILES['file']
    except Exception as e:
      print(f'Error: {e}')
      response['msg'] = "Error al leer los datos enviados"

    newtranslation = Documents.create('Translation',form.get('language'),form.get('title'),form.get('author'),uploadfile.name)

    if(id == -1):
      try:
        print(f"Traduccion del documento(ID) {form.get('document')}")
        newtranslation.save()
        fname = FileSystemStorage().save(f"file_{newtranslation.id}.txt",uploadfile)
        print(f"File: {fname}")
        document = Documents.objects.get(id = form.get('document'))
        processFile(newtranslation,fname)
        translation = Translations.create(document,newtranslation)
        translation.save()
      except Exception as e:
        print(f'Error: {e}')
        response['msg'] = "Error al guardar en la base de datos"
    else:
      print(f"Id: {id}")
      document = Documents.objects.get(id = id)
      changes = document.changes(newtranslation)
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
        processFile(document,fname)

      translation: Translations = Translations.objects.get(translated = document.id)
      print(f'Translation: {translation}')
      print(f"Document: {form.get('document')}")
      translation.original = Documents.objects.get(id = form.get('document'))
      translation.save();

    return JsonResponse(response)

  def delete(self, request: HttpRequest, id):
    response = {}
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
