# pylint: disable=E0401,E0611
import logging
import os

from dotenv import load_dotenv
# from models import Users
from sanic import Sanic, response
from tortoise.contrib.sanic import register_tortoise

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

env = os.environ

app = Sanic(__name__)

# app.config.DB_URL = f"{env['DB_TYPE']}://{env['DB_USER']}:{env.get('DB_PASSWD')}@{env['DB_HOST']}:3306/{env[
# 'DB_NAME']}"
app.config.DB_URL = "mysql://faucet:EFhGHHMA86ryFFxA@35.90.8.212:3306/openkey"

TORTOISE_ORM = {
    "connections": {"default": app.config.DB_URL},
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    db_url=app.config.DB_URL,
    modules={"models": ["models", "aerich.models"]}
)


# 启动时创建表

@app.route("/")
async def test(request):
    return response.json({"hello": "world"})


# @app.route("/users")
# async def get_users(request):
#     users = await Count.all()
#     return response.json(users)


if __name__ == "__main__":
    app.run(port=8080, dev=True, debug=True)

