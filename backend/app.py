from sanic import Sanic
from app.db.mongo import init_mongo
from app.routes import get_api_blueprints
from app.db.config import API_VERSION

app = Sanic("launchpad-backend")

@app.listener('before_server_start')
async def setup_db(app, loop):
    await init_mongo(app)

app.blueprint(get_api_blueprints(API_VERSION))

for route in app.router.routes_all:
    print(route)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 