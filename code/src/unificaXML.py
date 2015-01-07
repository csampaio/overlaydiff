import os
import csv
import codecs
import collections
from xmltoxls import convert
from organizaArquivo import organizeBase

def processFolder(rootDir, destFile):
    qtdXml = 0;
    totalStrings = 0
    for root, dirs, files in os.walk(rootDir, topdown=False):
        for name in files:
            path = (os.path.join(root, name))
            if (name.endswith('.xml')):
                qtdXml += 1
                print ("Processando " + path + " ...") 
                qtdStrings = convert(path, destFile)
                print ( str(qtdStrings) + " strings processadas.")
                totalStrings += qtdStrings
    print ("Quantidade de arquivos XML processados no diretório \'" + rootDir + "\': " + str(qtdXml))
    print ("Quantidade de strings processadas: " + str(totalStrings)) 

def readFileLines( path ):
    f = open(path,'r',encoding='utf-8')
    reader = csv.reader(f,delimiter=";")    
    lines = []
    for r in reader:
        lines.append(r)
    f.close()
    return lines

def findLineInList(line,baseList):
    achados = [i for i, s in enumerate(baseList) if line[3] in s]
    achado = None
    index = -1    
    for i in achados:        
        achado = baseList[i]        
        pathDir = achado[0]
        pathDir = pathDir.replace(rootDirs[prossFileIndex]['path'],'')
        pathBase = rootLine[0]
        pathBase = pathBase.replace(rootDirs[0]['path'],'')
        cPath = (pathBase == pathDir)
        cStringType = (line[1] == achado[1])
        cAttType = (line[2] == achado[2])
        cAttrValue = (line[3] == achado[3])
        cProduct = (line[4] == achado[4])
        cIndex = (line[5] == achado[5])
        cQty = (line[6] == achado[6])
        
        if (cPath and cStringType and cAttType and cAttrValue and cProduct and cIndex and cQty):            
            index = i
            break
        else:
            achado = None
    return index, achado

csvPath = 'unificacao.csv'
csvFile = codecs.open(csvPath,'w','utf-8')
writer = csv.writer(csvFile, delimiter=';', dialect='excel')

root = collections.OrderedDict()
root['id'] = 'Android'
#root['path'] = ".\\Junto\\Android_4_4_3_Padrão\\packages\\apps\\ContactsCommon"
root['path'] = ".\\Junto\\Android_4_4_3_Padrão"
rootDirs = []
rootDirs.append(root)
# root = collections.OrderedDict()
# root['id'] = 'AOSP'
# root['path'] = ".\\Junto\\AOSP-translationKOT49H\\packages\\apps\\ContactsCommon"
# rootDirs.append(root)
# root = collections.OrderedDict()
# root['id'] = 'ODM'
# root['path'] = ".\\Junto\\ODM-translation-s440\\packages\\apps\\ContactsCommon"
# rootDirs.append(root)

prossFiles = []
tempFiles = []
count = 0
for d in rootDirs:
    count += 1
    destFile = "temp" + str(count) + ".csv"
    processFolder(d['path'], destFile)
    orgFile = organizeBase(destFile)
    #prossFiles.append(orgFile)
    #tempFiles.append(destFile)

# prossFileIndex = 1
# rootLines = readFileLines(prossFiles[0])
# unionLines = []
# unionDic = []
# while prossFileIndex < len(prossFiles):
#     # Le as linhas das outras bases
#     fileLines = readFileLines(prossFiles[prossFileIndex])
#     rootLineIndex = 1
#     for rootLine in rootLines:
#         print ("processando " + str(rootLineIndex) + " de " + str(len(rootLines)))
#         dic = collections.OrderedDict()        
#         index, foundedLine = findLineInList(rootLine, fileLines)        
#         achou = 0
#         if (foundedLine is not None):
#             #print ("===============================ACHOU!=====================================")
#             iValue, value = findLineInList(rootLine,unionLines)
#             if (value is not None):
#                 newLine = value                
#             else:
#                 newLine = rootLine                
#             dic['base'] = newLine
#             dic[rootDirs[prossFileIndex]['id']] = foundedLine[7:]            
#             rootDirs[prossFileIndex]['count'] = len(foundedLine[7:])
#             newLine.extend(foundedLine[7:])
#             unionLines.append(newLine)
#             del fileLines[index]
#             achou = 1
#         if (not achou):            
#             unionLines.append(rootLine)
#             dic['base'] = rootLine
#         rootLineIndex += 1
#         unionDic.append(dic)
#     prossFileIndex+=1
# 
# #Adiciona as linhas que nao foram processadas
# for line in fileLines:
#     #line.insert(len(line)-1,'')
#     unionLines.append(line)
#     dic = collections.OrderedDict()
#     dic['base'] = line
#     unionDic.append(dic)
# 
# unionLines =[]
# for d in unionDic:
#     line = d['base']
#     keys = list(d.keys())
#     if (len(keys) > 1):
#         key = rootDirs[2]['id']
#         if (keys[1] == key):
#             i = 0
#             while i <= rootDirs[2]['count']:
#                 line.append('')
#                 i+=1
#         v = list(d.values())
#         line.extend(v[1])
#     unionLines.append(line)
#         
# writer.writerows(unionLines)

# for file in prossFiles:
#     if os.path.isfile(file):
#         os.remove(file)
# for file in tempFiles:
#     if os.path.isfile(file):
#         os.remove(file)
        
csvFile.close()
    
    
