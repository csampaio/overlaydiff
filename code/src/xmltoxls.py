# -*- coding: <utf-8> -*-
from xml.dom import minidom
import csv
import collections
import codecs
import os

def fillLine(values):
    line = collections.OrderedDict()    
    line['path'] = values[0]
    line['String Type'] = values[1]
    line['Attribute Type'] = values[2]
    line['Attribute Value'] = values[3]
    line['length'] = values[4]
    line['product'] = values[5]
    line['quantity'] = values[6]
    text = values[7]    
    line['Text'] = text.decode().replace('&quot;','')
    #columnname
    #dimen
    #integers
    #dimensions
    #styles
    
    #product
    return line

def convert( srcPath, destPath ):
    xmlPath = srcPath
    #xmlPath = 'apps-br\\Contacts\\res\\values-pt-rBR\\strings.xml'
    #xmlPath = 'apps-en\\Contacts\\res\\values\\strings.xml'
    destFile = codecs.open(destPath,'a','utf-8')
    csvFile = csv.writer(destFile, delimiter=';', dialect='excel')
    tree = minidom.parse(srcPath)
    root = tree.getElementsByTagName('resources')
    root = root[0]
    itemNum = 0

    line = collections.OrderedDict()

    line['path'] = xmlPath
    line['String Type'] = ''
    line['Attribute Type'] = ''
    line['Attribute Value'] = ''
    line['product'] = ''
    line['index'] = ''
    line['quantity'] = ''
    line['Text'] = ''

    lines = []
    if ( os.stat(destPath).st_size <= 0):
        keys = list(line.copy().keys())
        csvFile.writerow(keys)
    for child in root.childNodes:
        #itemNum += 1
        itemNum = 0
        if (child.nodeName == 'string'):
            if (not child.hasChildNodes):            
                line = fillLine([xmlPath,child.nodeName,'name',child.getAttribute('name'), child.getAttribute('product'),itemNum,'-',child.toxml()])
            else:
                text = b''
                for value in child.childNodes:                
                    text += value.toxml().encode()
                line = fillLine([xmlPath,child.nodeName,'name',child.getAttribute('name'), child.getAttribute('product'),itemNum,'-',text])
                
            lines.append(line)
        elif ((child.nodeName == 'string-array') or (child.nodeName == 'plurals')):
            childIndex = 1       
            for item in child.childNodes:
                text = b''
                qty = '-'                
                if (item.nodeName != '#text'):                    
                    for value in item.childNodes:                
                        text += value.toxml().encode()
                        if (child.nodeName == 'plurals'):
                            qty = item.getAttribute('quantity')
                if (text != b''):                        
                    line = fillLine([xmlPath,child.nodeName,'name',child.getAttribute('name'), child.getAttribute('product'),childIndex,qty,text])                    
                    childIndex += 1
                    lines.append(line)
        #else:
            #print (child.tag, child.attrib, child.text) 
            #print (child)
    for line in lines:
        value = list(line.copy().values())
        csvFile.writerow(value)    
    destFile.close()
    return len(lines)

#n = convert('.\\apps-br\\Contacts\\res\\values-pt-rBR\\strings.xml','teste.csv')
#print (n)
