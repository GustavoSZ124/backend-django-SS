
import re
from django.conf import settings

from api.models import Chapters, Passages

def processFile(document, fname):
  chapter: Chapters
  nchapter = 0
  passage: Passages
  npassage = 0
  passage_rex = re.compile("^\d+.")

  file = open(settings.MEDIA_ROOT / fname, "r", encoding="utf-8")
  lines = file.readlines()
  file.close()

  for i in range(len(lines)):
    l = lines[i].rstrip()
    if(passage_rex.match(l)):
      l = passage_rex.sub("",l)
      passage = Passages.create(chapter,l,f"{nchapter}.{npassage}")
      passage.save()
      npassage += 1
    elif(i != 0 and l!=""):
      chapter = Chapters.create(document,l,str(nchapter))
      chapter.save()
      nchapter += 1
      
  return