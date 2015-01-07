'''
Created on 28/04/2014

@author: Claudio Sampaio
'''
import os
import codecs
import csv
from xml.dom import minidom
import collections

class Base(object):
    '''
    class que trata os arquivos de localizacao de uma Base
    '''
    root = ''    
    resFiles = []
    allStringsList = []
    allHeaders =[]
    debug = 0

    def __init__(self, root):
        '''
        Constructor
        '''
        self.root = root          
    
    def getXmlFromFolders(self, folderPath):
        '''
        Pega uma lista de caminhos dos arquivos .xml contidos na Pasta
        '''
        if self.debug : print('getXmlFromFolders(self, folderPath)')
        xmlList = []
        for root, dirs, files in os.walk(folderPath, topdown=False):
            for name in files:
                path = (os.path.join(root, name))
                if (name.endswith('.xml')):
                    xmlList.append(path)
        return xmlList
    
    def listResFolders(self):
        '''
        Retorna uma lista do diretorio Res do path da base
        '''
        if self.debug : print('listResFolders(self)')
        resList = []
        for root, dirs, files in os.walk(self.root, topdown=False):
            for name in dirs:
                if (name == 'res'):
                    path = (os.path.join(root, name))
                    resList.append(path)                    
        return resList
    
    def createResDic(self, res):
        '''
        cria um objeto dicionario que contem o caminho para o res e o caminho para os arquivos XML em cada linguagem do res
        return dic{'path': path do res, 'valueX' : lista de path dos arquivos .xml que estao nas pastas de linguagem valueX, ...'valueN' : lista de path dos arquivos .xml que estao nas pastas de linguagem valueN,} 
        '''
        if self.debug : print('createResDic(self, res)')
        resDic = dict()
        langDirs = os.listdir(res)
        resDic['path'] = res
        langList = []
        for dirLang in langDirs:
            if os.path.isfile(res+'\\'+dirLang):
                continue
            xmlList = self.getXmlFromFolders(res + '\\' + dirLang)
            langList.append(dirLang)            
            resDic[dirLang] = xmlList
        resDic['languages'] = langList
        return resDic
    
    def createFileFromRes(self):
        '''
        Cria um arquivo unico com as strings de uma lingua na pasta res
        '''
        if self.debug : print('createFileFromRes(self)')
        resList = self.listResFolders()
        iRes = 1
        for item in resList:            
            print('Resource: ' + item + ' ' + str(iRes) + ' de ' + str(len(resList)))
            iRes += 1
            resDic = self.createResDic(item)
            keys = resDic['languages']
            print('Linguas: ' + ', '.join(keys))            
            for key in keys:
                csvFiles = []
                fileList = resDic.get(key)
                print('Convertendo arquivos XML de ' + key)                
                for file in fileList:
                    print('Xml: ' + file)
                    csvPath = self.convertXmltoCsv(file)
                    if csvPath != '':
                        csvFiles.append(csvPath)            
                langDic = dict()
                langDic['xml'] = fileList
                langDic['csv'] = csvFiles
                resDic[key] = langDic
            resDic['folder'] = item.replace(self.root + '\\','').replace('\\','.')            
            self.mergeCsvFiles(resDic)
            
            print('\n')
            self.resFiles.append(resDic)
        
    
    def createCsvDic(self,language, item):        
        '''
        Cria um dicionario de item do xml para ser escrito no csv
        '''
        if self.debug : print('createCsvDic(self,language, item)')
        csvDicList =[]
        if (item.nodeName == 'string'):
            csvDic = self.createStringItem(item,language)
            csvDicList.append(csvDic)
        elif ((item.nodeName == 'string-array') or (item.nodeName == 'plurals')):
            csvDic = self.createArrayItem(item, language)
            csvDicList.extend(csvDic)
        return csvDicList
    
    def createStringItem(self, item, language):
        '''    
        Cria um dicionario de csv para um item de string do xml
        '''
        if self.debug : print('createStringItem(self, item, language)')
        if (not item.hasChildNodes):            
                text = item.toxml()
        else:
            text = ''
            for value in item.childNodes:                
                text += value.toxml()
        
        csvDic = collections.OrderedDict()
        csvDic['path'] = ''
        csvDic['String Type'] = item.nodeName
        csvDic['Attribute Type'] = 'name'
        csvDic['Attribute Value'] = item.getAttribute('name')
        csvDic['product'] = item.getAttribute('product')
        csvDic['index'] = 0
        csvDic['quantity'] = '-'
        csvDic[language] = text.replace('&quot;', '')
        return csvDic
    
    
    def createArrayItem(self, item, language):
        '''
        Cria uma lista de dicionario de csv para cada linha de string-array e plurals do xml
        '''
        if self.debug : print('createArrayItem(self, item, language)')
        index = 1
        csvDicList = []
        for node in item.childNodes:
            text = ''
            qty = '-'                
            if (node.nodeName != '#text' and node.nodeName != '#comment'):                    
                for value in node.childNodes:
                    text += value.toxml()
                if (item.nodeName == 'plurals'):                    
                    qty = node.getAttribute('quantity')                        
                csvDic = collections.OrderedDict()
                csvDic['path'] = ''
                csvDic['String Type'] = item.nodeName
                csvDic['Attribute Type'] = 'name'
                csvDic['Attribute Value'] = item.getAttribute('name')
                csvDic['product'] = item.getAttribute('product')
                csvDic['index'] = index
                csvDic['quantity'] = qty
                csvDic[language] = text.replace('&quot;', '')
                csvDicList.append(csvDic)
                index += 1
        return csvDicList
        
    
    def parserXml(self, xmlPath):
        '''
        Faz o parser do xml e retorna uma lista de itens csv
        '''
        if self.debug : print('parserXml(self, xmlPath)')
        sPos = xmlPath.find('values')
        ePos = xmlPath.find('\\',sPos+1)
        language = xmlPath[sPos:ePos]
        tree = minidom.parse(xmlPath)
        nodes = tree.getElementsByTagName('resources')
        root = nodes[0]
        csvList = []
        for child in root.childNodes:
            csvDicList = self.createCsvDic(language, child)
            csvList.extend(csvDicList)
        
        return csvList
    

    def convertXmltoCsv(self,xmlPath):
        '''
        Converte arquivo XML em arquivo csv e salva na pasta res
        '''
        if self.debug : print('convertXmltoCsv(self,xmlPath)')
        csvList = self.parserXml(xmlPath)
        csvPath = ''
        if len(csvList) > 0 :
            sPos = xmlPath.find('values')
            csvPath = xmlPath[:sPos]
            csvPath += xmlPath[sPos:].replace('\\','.').replace('.xml','.csv')
            fCsv = codecs.open(csvPath,'w','utf-8')
            writer = csv.writer(fCsv, delimiter=';', dialect='excel')
            header = list(csvList[0].keys())
            writer.writerow(header)
            for csvItem in csvList:
                csvItem['path'] = xmlPath
                values = list(csvItem.values())
                writer.writerow(values)
            fCsv.close()
            
        return csvPath
        
    def mergeCsvFiles(self, resDic):
        '''
        Consolida os arquivos .csv de uma pasta res em um unico arquivo
        '''
        resDic = self.loadCSVFiles(resDic)        
        filenames = self.getFiles(resDic)
        languages = resDic['languages']
        languages.sort()
        for file in filenames:
            unicList = []
            header = []
            for lang in languages:
                m = next((dictio for dictio in resDic[lang]['csvList'] if dictio['filename'] == file),None)
                if m is not None:
                    unicList, header = self.compareLists(unicList, header, lang, m)                    
            filename = resDic['folder'] + '.' + file.replace('.csv','')
            filename += '.unificado.csv'
            self.saveUnifiedFile(filename, unicList, header)
            self.allStringsList.extend(unicList);
            if header not in self.allHeaders:
                for h in header:
                    if h not in self.allHeaders:
                        self.allHeaders.append(h)

    def compareLists(self,unicList,header, lang, dic):
        if len(unicList) < 1:
            header = dic['header']
            unicList = dic['rows']            
        else:
            print(list(dic.keys()))
            for item in unicList:
                key,value = self.extractResDic(lang, item, dic['rows'])
                if (key is not None) and (value is not None):
                    item[key] = value
            for h in dic['header']:
                if h not in header:
                    header.append(h)
            unicList.extend(dic['rows'])
        return unicList, header

    def getFiles(self, resDic):
        files = []
        for lang in resDic['languages']:            
            for value in resDic[lang]['csvList']:
                filename = value['filename']
                if not filename in files:
                    files.append(filename)
        return files

    def extractResDic(self, lang, resDic,dicList):
        '''
        Procura o resDic na lista e caso encotre retorna o header e o valor e exclui o item encontrado da lista
        '''
        newKey = None
        newValue = None
        matches = [dictio for dictio in dicList if self.compareLine(resDic,dictio)]
        for m in matches:
            index = dicList.index(m)
            #header = list(m.keys())
            #print(header)
            #pos = len(header) - 1
            #newKey = header[pos]
            newKey = lang
            newValue = m[newKey]            
            del dicList[index]
            text = newKey + ': ' + newValue
            print(text.encode('utf-8','ignore'))
        return newKey, newValue
        

    def saveUnifiedFile(self, filename, lines, header):
        filename = self.root + '\\' + filename
        print(filename)
        f = codecs.open(filename, 'w', 'utf-8')
        writer = csv.DictWriter(f,header,delimiter=';',dialect='excel')
        writer.writeheader();
        writer.writerows(lines)
        f.close()
                        
                            
    def compareLine(self,refDic, dic):
        attValue = dic['Attribute Value'] == refDic['Attribute Value']
        strType = dic['String Type'] == refDic['String Type']
        attrType = dic['Attribute Type'] == refDic['Attribute Type'] 
        product = dic['product'] == refDic['product'] 
        index = dic['index'] == refDic['index'] 
        qty = dic['quantity'] == refDic['quantity']     
        return attValue and strType and attrType and product and index and qty
                        
        
        #matches = filter(lambda d: d['Attribute Value'] == 'oma_download_content_not_supported' and d['product'] == 'tablet', csvList1)
        
        
    def loadCSVFiles(self, resDic):
        langList = resDic['languages']
        for lang in langList:
            csvFiles = resDic[lang]['csv']
            csvList = []
            for file in csvFiles:
                csvDic = self.readCSVRows(file)
                csvList.append(csvDic)
            resDic[lang]['csvList'] = csvList
        return resDic
                
                
    def readCSVRows(self,file):
        f = codecs.open(file, 'r', 'utf-8')
        reader = csv.DictReader(f,delimiter=';', dialect='excel')
        csvDic = dict()
        csvDic['filename'] = os.path.split(file)[1].split('.')[1]
        csvDic['header'] = reader.fieldnames
        rowList = []
        for row in reader:
            rowList.append(row)
        csvDic['rows'] = rowList
        f.close()
        return  csvDic    
        
                    
base = Base('.\\Junto\\ODM-translation-s440')
#csv1 = '.\\Junto\\ODM-translation-s440\\packages\\providers\\DownloadProvider\\ui\\res\\values.mtk_strings.csv'
#csv2 = '.\\Junto\\ODM-translation-s440\\packages\\providers\\DownloadProvider\\ui\\res\\values-en-rUS.mtk_strings.csv'
base.createFileFromRes()
print('Todos os Strings')
base.saveUnifiedFile('todos.csv',base.allStringsList, base.allHeaders)
#for file in base.resFiles:
#    print(file)

          
