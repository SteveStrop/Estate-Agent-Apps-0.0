import configparser

config = configparser.ConfigParser()
config.read('PyWEB.ini')
for k in config['HS']:
    print(k, ':', config['HS'][k])

print(config['HS']['password'])
