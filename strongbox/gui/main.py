import rumps
import uvicorn
import multiprocessing
from strongbox.app.server import app
from strongbox.gui.constants import Constants


def _run_server(host: str = Constants.SERVER_HOST, port: int = Constants.SERVER_PORT):
    uvicorn.run(app, host=host, port=port, log_level="info")


class StrongBoxApp(rumps.App):
    def __init__(self, name, title=None, icon=None, template=None, menu=None):
        super().__init__(name, title=title, icon=icon, template=template, menu=menu, quit_button=None)
        self.process = multiprocessing.Process(target=_run_server)
        self.process.start()

    @rumps.clicked("Quit")
    def on_quit(self, _):
        self.process.terminate()
        rumps.quit_application()


if __name__ == "__main__":
    StrongBoxApp(Constants.APP_TITLE).run()
