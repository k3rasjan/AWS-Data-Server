from aiohttp import web
from database.models import AWSCredentials, Companies
from .elastic import connect, insert_assets, search_assets, delete_assets

routes = web.RouteTableDef()

@routes.get('/status')
async def status(request):
    return web.Response(text="OK", status=200)


@routes.post('/add_credentials')
async def add_creds(request):
    try:
        data = await request.json()
    except:
        return web.Response(text="Invalid data", status=400)

    access_key = data['access_key']
    secret_key = data['secret_key']
    company_id = data['company_id']

    if not all([access_key, secret_key, company_id]):
        return web.Response(text="Missing data", status=400)
    
    if not await Companies.filter(id=company_id).exists():
        return web.Response(text="Company not found", status=404)

    await AWSCredentials.create(
        access_key=access_key,
        secret_key=secret_key,
        company_id=company_id
    )

    # Fetch assets from AWS

    predefined_data = [
        {
            "access_key": f"{access_key}",
            "public_ip": "192.1.1.1",
            "public_name": "aws1test.eu-central-1.aws.com",
            "json_info": {
                "asdas":"sadas"
            }
        }
    ]

    # Store assets in Elasticsearch
    client = await connect()
    await insert_assets(client, "cloud_assets", predefined_data)

    await client.close()

    return web.Response(text="Credentials added", status=200)


@routes.post('/remove_credentials')
async def remove_creds(request):
    try:
        data = await request.json()
    except:
        return web.Response(text="Invalid data", status=400)

    company_id = data['company_id']

    if not company_id:
        return web.Response(text="Missing data", status=400)
    
    if not await Companies.filter(id=company_id).exists():
        return web.Response(text="Company not found", status=404)
    
    creds = await AWSCredentials.filter(company_id=company_id).all()

    client = await connect()

    for cred in creds:
        await delete_assets(client, "cloud_assets", cred.access_key)
    
    await client.close()

    await AWSCredentials.filter(company_id = company_id).delete()
    return web.Response(text="Credentials removed", status=200)


@routes.get('/get_assets')
async def get_assets(request):
    try:
        data = await request.json()
    except:
        return web.Response(text="Invalid data", status=400)

    company_id = data['company_id']

    if not company_id:
        return web.Response(text="Missing data", status=400)
    
    if not await Companies.filter(id=company_id).exists():
        return web.Response(text="Company not found", status=404)
    
    creds = await AWSCredentials.filter(company_id=company_id).all()

    client = await connect()
    assets = []
    for cred in creds:
        asset = await search_assets(client, "cloud_assets", cred.access_key)
        assets.extend(asset)

    await client.close()

    return web.json_response({"assets": assets}, status=200)