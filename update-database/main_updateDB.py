from sqlalchemy import create_engine
from dfs_update import Update_dfs
import configparser

configParser = configparser.RawConfigParser()
configFilePath = '/Users/chiara/PycharmProjects/WhatToWatch_GITHUB/login.config'
configParser.read(configFilePath)
user = configParser.get('dev-postgres-config', 'user')
pwd = configParser.get('dev-postgres-config', 'pwd')
host = configParser.get('dev-postgres-config', 'host')
port = configParser.get('dev-postgres-config', 'port')

engine = create_engine('postgresql+psycopg2://'+user+':'+pwd+'@'+host+':'+port+'/whattowatch')


update_dfs = Update_dfs(engine)
update_dfs.obtain_dfs()
print("All dfs created/updated")