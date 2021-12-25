import rumps
import uvicorn
import multiprocessing
from typing import Optional

import strongbox.app.utils as utils
from strongbox.app.server import app
from strongbox.gui.constants import Constants


def _run_server(host: str = Constants.SERVER_HOST, port: int = Constants.SERVER_PORT):
    uvicorn.run(app, host=host, port=port, log_level="info")


def _input_text(title: str, message: str, label: str) -> Optional[str]:
    window = rumps.Window(message, title, ok="Ok", cancel="Cancel")
    window.default_text = label
    response = window.run()
    if response.clicked:
        return response.text


class StrongBoxApp(rumps.App):
    def __init__(self, name, title=None, icon=None, template=None, menu=None):
        super().__init__(name, title=title, icon=icon, template=template, menu=menu, quit_button=None)
        self.process = multiprocessing.Process(target=_run_server)
        self.process.start()

    @rumps.clicked("Create Profile")
    def create_profile(self, _):
        profile = _input_text("Create profile", "Enter username", "username...")
        if profile:
            password = _input_text("Create profile", "Enter password", "password...")
            if password:
                utils.create_profile(profile, password)

    @rumps.clicked("Quit")
    def quit(self, _):
        self.process.terminate()
        rumps.quit_application()


if __name__ == "__main__":
    StrongBoxApp(Constants.APP_TITLE).run()
