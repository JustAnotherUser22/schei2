
'''
carica un csv molto grande
lo scompone in file più piccoli
'''

INPUT_FILE_NAME = "D:/script/Eu.csv"
OUTPUT_FILE_NAME = "D:/script/GenAl/files/file_split_{0}.csv"
NUMBER_OF_FILE = 10


def main():
   inputFile = open(INPUT_FILE_NAME)
   outputFile = open(OUTPUT_FILE_NAME.format(0), "w")
   index = 0
   currentFileLength = 0

   totalLength = len(inputFile.readlines())
   inputFile.close()
   inputFile = open(INPUT_FILE_NAME.format(0))

   lineForFile = totalLength / 3
   
   line = inputFile.readline()
   while(line):
      currentFileLength += int(1)
      
      if(currentFileLength == lineForFile):
         currentFileLength = 0
         index += int(1)
         outputFile.close()
         outputFile = open(OUTPUT_FILE_NAME.format(index), "w")

      outputFile.write(line)

      line = inputFile.readline()


def second():
   inputFile = open(INPUT_FILE_NAME.format(0))
   
   lines = inputFile.readlines()

   totalLength = len(lines)
   inputFile.close()
   
   lineForFile = int(totalLength / NUMBER_OF_FILE)

   for i in range(0, NUMBER_OF_FILE):
      start = int(i * lineForFile)
      end = int((i+1) * lineForFile )
      fileName = OUTPUT_FILE_NAME.format(i)
      outputFile = open(fileName, "w")
      print("writing " + fileName)
      outputFile.writelines(lines[start:end])
      outputFile.close()

   print("end")

def test():
   a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   indicePrimoElementoIncluso = 1
   indiceUltimoElementoEscluso  = 4
   print(a[indicePrimoElementoIncluso:indiceUltimoElementoEscluso])

if __name__ == "__main__":
   #main()
   second()
   #test()