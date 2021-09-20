import inspect
import sys
import webbrowser
import uvicorn
from .config import config  # NOTE: before justpy
import justpy as jp

if not config.interactive and config.reload and not inspect.stack()[-2].filename.endswith('spawn.py'):
    if config.show:
        webbrowser.open(f'http://{config.host}:{config.port}/')
    uvicorn.run('nicegui:app', host=config.host, port=config.port, lifespan='on',
                reload=True, log_level=config.uvicorn_logging_level)
    sys.exit()

def run(self, *,
        host: str = '0.0.0.0',
        port: int = 80,
        title: str = 'NiceGUI',
        favicon: str = 'favicon.ico',
        reload: bool = True,
        show: bool = True,
        uvicorn_logging_level: str = 'warning',
        ):
    if config.interactive or reload == False:  # NOTE: if reload == True we already started uvicorn above
        if show:
            webbrowser.open(f'http://{host if host != "0.0.0.0" else "127.0.0.1"}:{port}/')
        uvicorn.run(jp.app, host=host, port=port, log_level=config.uvicorn_logging_level, lifespan='on')
