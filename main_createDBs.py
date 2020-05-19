from sqlalchemy import create_engine
from dfs_update import Update_dfs

engine = create_engine('postgresql+psycopg2://dev_postgres:dasquee@localhost:5434/whattowatch')


update_dfs = Update_dfs(engine)
update_dfs.obtain_dfs()
print("All dfs updated")