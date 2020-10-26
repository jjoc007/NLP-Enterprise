from neomodel import config

try:
    #config.DATABASE_URL = f'bolt://{neo4j_username_parameter}:{neo4j_password_parameter}@{neo4j_endpoint_parameter}'
    config.DATABASE_URL = f'bolt://neo4j:123456@localhost:7687'
except  Exception as e:
    print(e)
