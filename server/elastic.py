from elasticsearch import AsyncElasticsearch
from settings import config

async def connect():
    client = AsyncElasticsearch(
        config["elastic"]["endpoint"],
        api_key=config["elastic"]["api_key"],
    )
    return client

# mapping = {
#     "properties": {
#             "accees_key": {"type": "text"},
#             "public_ip": {"type": "ip"},
#             "dns": {"type": "text"},
#             "json": {"type": "object"}
#         }
#     }

# async def create_index(client, index_name, mappings):
#     if not await client.indices.exists(index= index_name):
#         await client.indices.create(
#             index=index_name,
#             body={
#                 "settings": {
#                     "number_of_shards": 1,
#                     "number_of_replicas": 0
#                 },
#                 "mappings": mappings,
#             },
#         )
#         print(f"Index {index_name} created.")
#     else:
#         print(f"Index {index_name} already exists.")

async def insert_assets(client, index_name, assets):
    for asset in assets:
        await client.index(index=index_name, body=asset)

async def search_assets(client, index_name, access_key):
    query = {
        "query": {
            "match": {
                "access_key": access_key
            }
        }
    }
    result = await client.search(index=index_name, body=query)
    
    return [hit["_source"] for hit in result["hits"]["hits"]]

async def delete_assets(client, index_name, access_key):
    query = {
        "query": {
            "match": {
                "access_key": access_key
            }
        }
    }
    await client.delete_by_query(index=index_name, body=query)