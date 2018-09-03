from aiohttp import web
import jinja2
import aiohttp_jinja2
import asyncpgsa

from .routes import setup_routes


async def create_app(config: dict):
    app = web.Application()
    app['config'] = config
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('demo', 'templates')
    )
    setup_routes(app)
    app.on_startup.append(on_start_app)
    return app


async def on_start_app(app):
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(dsn=config['database_uri'])


async def on_close_app(app):
    await app['db'].close()
