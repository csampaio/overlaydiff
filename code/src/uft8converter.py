import codecs

filePath = 'apps-br\\Contacts\\res\\values-pt-rBR\\strings.csv'

def convertFile2():
    fo = codecs.open( filePath, 'rb', 'utf-8')
    uFile = codecs.open('utf8file.csv', 'wb', 'utf-8')

    line = b''
    for line in fo.readlines():    
        uFile.write(line.decode())
    fo.close()
    uFile.close()

def convertFile():
    file_path_utf8 = filePath
    file_path_ansi = "utf8file.csv"

    #open and encode the original content
    file_source = open(file_path_utf8, mode='r', encoding='utf-8', errors='ignore')
    file_content = file_source.read()
    file_source.close

    #write the UTF8 file with the encoded content
    file_target = open(file_path_ansi, mode='w', encoding='latin-1', errors='xmlcharrefreplace')
    file_target.write(file_content)
    file_target.close

convertFile()
