class FtpConfig:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.uri = 'ftp://'+username+':'+password+'@'+host

def get_ini():
    import configparser

    config = configparser.ConfigParser()
    config.read('config.ini')

    return config

def get_config():
    ini = get_ini()

    host = ini['ftp']['host']
    port = ini['ftp']['port']
    username = ini['ftp']['username']
    password = ini['ftp']['password']

    return FtpConfig(host, port, username, password)

def create_path(path):
    import os

    if not os.path.exists(path):
        os.makedirs(path)      

def optimize(file_name, cnpj):
    from PIL import Image
    import math

    foo = Image.open(f'images\\ftp\\{cnpj}\\{file_name}')

    x, y = foo.size
    x2, y2 = math.floor(x-50), math.floor(y-20)
    foo = foo.resize((x2,y2),Image.ANTIALIAS)              

    foo.save(f'images\\optimized\\{cnpj}\\{file_name}', optimize=True, quality=30)

def printProgressBar (iteration, total, prefix = 'PROGRESSO:', suffix = 'COMPLETO', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    if iteration == total: 
        print()

import ftplib

config = get_config()

ftp = ftplib.FTP(config.host)
ftp.login(user=config.username, passwd = config.password)


ftp.cwd('/www/delivery/')
for cnpj in ftp.nlst():
    ftp.cwd(f'/www/delivery/{cnpj}/')
    images = ftp.nlst()

    create_path(f'images/optimized/{cnpj}')
    create_path('images/ftp/'+cnpj)

    print(f'[CLIENTE {cnpj}]')
    printProgressBar(0, len(images))

    i = 1
    for image in images:
        ftp.retrbinary("RETR " + image, open(f'images/ftp/{cnpj}/{image}', 'wb').write)

        optimize(image, cnpj)

        printProgressBar(i, len(images))
        i = i + 1

ftp.quit()
    
# filename = 'images\\optimized\\' + image
# with open(filename, "rb") as file:
#     ftp.storbinary(f"STOR {image}", file)