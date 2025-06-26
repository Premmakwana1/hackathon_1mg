from sanic import Sanic
from app.db.mongo import init_mongo
from app.routes import v1_blueprints

app = Sanic("launchpad-backend")

@app.listener('before_server_start')
async def setup_db(app, loop):
    await init_mongo(app)

app.blueprint(v1_blueprints)

for route in app.router.routes_all:
    print(route)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 