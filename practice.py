import sqlalchemy.dialects.postgresql as pg_dialects

# 查看所有可用的PostgreSQL驱动
print("可用驱动:", pg_dialects.dialect.import_db_drivers())