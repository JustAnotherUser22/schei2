
class Pagine:

   def __init__(self):
      self.pages = []

   def add(self, description, url):
      entry = {
         "description": description,
         "path": url
      }
      self.pages.append(entry)

   def getUrlWithGivenDescription(self, description):
      toReturn = 0
      for entry in self.pages:
         if(entry["description"] == description):
            toReturn = entry["path"]
      return toReturn
   
   def IsPathInDictionary(self, path):
      for entry in self.pages:
         if(entry["path"] == path):
            return True
      return False
      