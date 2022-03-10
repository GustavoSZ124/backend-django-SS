
from django.conf import settings


def processFile(document, fname):
  file = open(settings.MEDIA_ROOT / fname, "r", encoding="utf-8")
  lines = file.readlines()
  file.close()

  for i in range(len(lines)):
    print(f"{i}: {lines[i]}")
  return