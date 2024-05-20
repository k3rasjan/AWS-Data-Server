from aiohttp import web
from server.routes import routes
from tortoise.contrib.aiohttp import register_tortoise
from settings import config

# Server 
app = web.Application()

# Database connection

db_data = config['database']
db_url = f"mysql://{db_data['user']}:{db_data['password']}@{db_data['host']}:{db_data['port']}/{db_data['database']}"

register_tortoise(
    app,
    db_url=db_url,
    modules={'models': ['database.models']},
    generate_schemas=True
)

app.add_routes(routes)
web.run_app(app)