import csv
import codecs
import collections

def readFileLines( path ):
    f = codecs.open(path,'r',encoding='utf-8')
    reader = csv.reader(f,delimiter=";")    
    lines = []
    for r in reader:
        lines.append(r)
    f.close()
    return lines

def writeFileLines( path, lines ):
    fileName = 'org_' + path
    f = codecs.open(fileName,'a',encoding='utf-8')
    writer = csv.writer(f,delimiter=";")    
    writer.writerows(lines)
    f.close()
    return fileName

def organizeBase2(filePath):
    organizedLines = []    
    linesBase = readFileLines(filePath)
    linesSearch = linesBase
    print(filePath)
    for line in linesBase:
        iFounds = [i for i, s in enumerate(linesSearch) if line[3] in s]
        for i in iFounds:
            print(i,linesSearch[i])
        if len(iFounds) == 0:
            print('----------------',line,'------------------')

def organizeBase(filePath):    
    organizedLines = []    
    lines = readFileLines(filePath)
    print(len(lines))
    iBase = 0
    usados = []
    values = []
    for line in lines:
        if (iBase in usados):            
            continue
        #newLine = line
        dic = collections.OrderedDict()
        dic['base'] = line
        iFounds = [i for i, s in enumerate(lines) if line[3] in s]
        for i in iFounds:    
            if ((i > iBase) and (i < len(lines)) and (not i in usados)):
                cProduct = (lines[iBase][4] == lines[i][4])
                cIndex = (lines[iBase][5] == lines[i][5])
                cQty = (lines[iBase][6] == lines[i][6])
                if (cProduct and cIndex and cQty):                                 
                    print('Achei')
                    folder = lines[i][0]
                    s = folder.find('values')
                    e = folder.find('\\',s+1)
                    folder = folder[s:e]
                    if (not folder in values):
                        values.append(folder)
                    dic[folder] = lines[i][7]
                    usados.append(iBase)                 
                    usados.append(i)
                    break
        organizedLines.append(dic)
        iBase += 1
    newLines = []
    lines[0].extend(values) 
    print('orga', len(organizedLines))       
    for item in organizedLines:        
        line = item['base']
        for v in values:
            if v in item.keys():
                line.append(item[v])
            else:
                line.append('')
        newLines.append(line)
    notUseds = [usados not in enumerate(lines)]
    for i in notUseds:
        print(lines[i])
        newLines.append(lines[i])
    return writeFileLines(filePath,newLines)
    
    
#organizeBase2('temp1.csv')
