
import re
from django.conf import settings

from api.models import Chapters, Passages

# Function to process a file and save the chapters and passages in the database
# The function receives as parameters the instance of the Documents model and the name of the file
def processFile(document, fname):
  chapters = []
  passages = []
  chapter: Chapters
  nchapter = 0
  passage: Passages
  npassage = 0
  passage_rex = re.compile("^\d+.") # Regular expression to detect passages in the file

  file = open(settings.MEDIA_ROOT / fname, "r", encoding="utf-8")
  lines = file.readlines()
  file.close()

  # Loop to process each line of the file
  # Instances of each chapter or passage are created saving them in Arrays
  for i in range(len(lines)):
    l = lines[i].rstrip()
    if(passage_rex.match(l)):
      l = passage_rex.sub("",l)
      passage = Passages.create(chapter,l,f"{nchapter}.{npassage}")
      passages.append(passage)
      npassage += 1
    elif(i != 0 and l!=""):
      chapter = Chapters.create(document,l,str(nchapter))
      chapters.append(chapter)
      nchapter += 1
  # To create database records efficiently, use the bulk_create function
  # Passing the arrays with the previously created instances
  Chapters.objects.bulk_create(chapters)
  Passages.objects.bulk_create(passages)
  return