
from django.db import models

# Create your models here.

class Documents(models.Model):
  id_Document = models.IntegerField(primary_key=True,null=False)
  file = models.CharField(max_length=30,null=False)
  language = models.CharField(max_length=2,null=False)
  title = models.CharField(max_length=30,null=False)
  author = models.CharField(max_length=50,null=False)
  type = models.CharField(max_length=15,choices=[('0','Original'),('1','Translation')],default='Original')

  @classmethod
  def create(cls,type,language,title,author,file):
    # document = cls(type=type,title=title,author=author,language=language,file=file)
    document = cls(type,language,title,author,file)
    return document

  def __str__(self):
    return self.type+"\n"+self.language+"\n"+self.title+"\n"+self.author+"\n"+self.file

  class Meta:
    db_table = 'documents'
    ordering = ['-type']

class Chapters(models.Model):
  id_Chapter = models.IntegerField(primary_key=True,null=False)
  id_Document = models.ForeignKey(Documents,on_delete=models.CASCADE,null=False)
  chapter = models.CharField(max_length=15,null=False)
  num = models.PositiveSmallIntegerField(null=False)

  @classmethod
  def create(cls,id_Document,chapter,num):
    # document = cls(type=type,title=title,author=author,language=language,file=file)
    document = cls(id_Document,chapter,num)
    return document

  def __str__(self):
    return self.num+": "+self.chapter

  class Meta:
    db_table = 'chapters'
    ordering = ['-id_Document','-num']

class Passages(models.Model):
  id_Passage = models.IntegerField(primary_key=True,null=False)
  id_Chapter = models.ForeignKey(Chapters,on_delete=models.CASCADE,null=False)
  passage = models.CharField(max_length=50,null=False)
  num = models.PositiveSmallIntegerField(null=False)

  def __str__(self):
    return self.num+": "+self.passage

  class Meta:
    db_table = 'passages'
    ordering = ['-id_Chapter','-num']

class Translations(models.Model):
  id_Translation = models.IntegerField(primary_key=True,null=False)
  original = models.ForeignKey(Documents,on_delete=models.CASCADE,null=False,related_name='original')
  translated = models.ForeignKey(Documents,on_delete=models.CASCADE,null=False,related_name='translated')

  def __str__(self):
    original: Documents = self.original
    translated: Documents = self.translated
    if(original and translated):
      return original.title+": "+original.language+" >> "+translated.language
    return "---"

  class Meta:
    db_table = 'translations'
    ordering = ['-original']
