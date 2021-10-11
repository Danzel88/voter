import uvicorn

from voter.settings import setting

uvicorn.run("voter.app:app", host=setting.server_host,
            port=setting.server_port, reload=True)
