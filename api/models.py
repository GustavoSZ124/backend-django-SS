
from django.db import models

# Create your models here.

class Documents(models.Model):
  file = models.CharField(max_length=30,null=False)
  language = models.CharField(max_length=2,null=False)
  title = models.CharField(max_length=30,null=False)
  author = models.CharField(max_length=50,null=False)
  type = models.CharField(max_length=15,default='Original')

  @classmethod
  def create(cls,type,language,title,author,file):
    return cls(type=type,language=language,title=title,author=author,file=file)

  def __str__(self):
    return self.type+"\n"+self.language+"\n"+self.title+"\n"+self.author+"\n"+self.file

  def changes(self,other):
    res = [False]
    if(not isinstance(other, self.__class__)):
      return res
    res.append([])
    res.append([])
    for attr in vars(self).keys():
      if(attr != "_state" and attr != "id" and attr != "type"):
        if(getattr(self,attr) != getattr(other,attr)):
          res[0] = False
          res[1].append(attr)
          res[2].append(getattr(other,attr))
    return res

  class Meta:
    db_table = 'documents'
    ordering = ['-type']

class Chapters(models.Model):
  document = models.ForeignKey(Documents,on_delete=models.CASCADE,null=False)
  chapter = models.CharField(max_length=15,null=False)
  num = models.CharField(max_length=2,null=False)

  @classmethod
  def create(cls,document,chapter,num):
    return cls(document=document,chapter=chapter,num=num)

  def __str__(self):
    return self.num+": "+self.chapter

  class Meta:
    db_table = 'chapters'
    ordering = ['document','num']

class Passages(models.Model):
  chapter = models.ForeignKey(Chapters,on_delete=models.CASCADE,null=False)
  passage = models.CharField(max_length=500,null=False)
  num = models.CharField(max_length=2,null=False)

  @classmethod
  def create(cls,chapter,passage,num):
    return cls(chapter=chapter,passage=passage,num=num)

  def __str__(self):
    return self.num+": "+self.passage

  class Meta:
    db_table = 'passages'
    ordering = ['chapter','num']

class Translations(models.Model):
  original = models.ForeignKey(Documents,on_delete=models.CASCADE,null=False,related_name='original')
  translated = models.ForeignKey(Documents,on_delete=models.CASCADE,null=False,related_name='translated')

  @classmethod
  def create(cls,original,translated):
    return cls(original=original,translated=translated)

  def __str__(self):
    original: Documents = self.original
    translated: Documents = self.translated
    if(original and translated):
      return original.title+": "+original.language+" >> "+translated.language
    return "---"

  class Meta:
    db_table = 'translations'
    ordering = ['original']
