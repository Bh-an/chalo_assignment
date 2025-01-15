from api.app import create_app
from api.app.utils.config import Config

config = Config()
app = create_app(config)

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST_ADDRESS, port=config.API_PORT, use_reloader=True)