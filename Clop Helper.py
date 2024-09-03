from rumps import notification, clicked, App, quit_application
from os import makedirs, path, remove
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

monitor_path = path.expanduser("~/Library/Caches/Clop")
images_path = path.join(monitor_path, "images")

observer = None

def ensure_images_folder():
    if path.exists(images_path):
        if path.isfile(images_path):
            remove(images_path)
            makedirs(images_path)
    else:
        makedirs(images_path)

class DirectoryChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        ensure_images_folder()

def start_observer():
    global observer
    if observer is None:
        event_handler = DirectoryChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, monitor_path, recursive=False)
        observer.start()
        notification("Clop Helper", "Monitoring Started", "Now watching ~/Library/Caches/Clop.")

def stop_observer():
    """Stop the observer."""
    global observer
    if observer is not None:
        observer.stop()
        observer.join()
        observer = None
        notification("Clop Helper", "Monitoring Stopped", "Stopped watching ~/Library/Caches/Clop.")

class CaffeinaterApp(App):
    def __init__(self):
        super(CaffeinaterApp, self).__init__("Clop Helper",
                                             icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/PicturesFolderIcon.icns",
                                             quit_button=None)
        self.menu = ["Start", "Quit"]
        start_observer()
        self.is_watching = True
        self.menu["Start"].title = "Stop"

    @clicked("Start")
    def toggle_watching(self, sender):
        global observer
        if self.is_watching:
            stop_observer()
            self.is_watching = False
            sender.title = "Start"
        else:
            start_observer()
            self.is_watching = True
            sender.title = "Stop"

    @clicked("Quit")
    def quit_app(self, _):
        stop_observer()
        notification("Clop Helper", "Exiting", "Clop Helper is shutting down.")
        quit_application()

if __name__ == "__main__":
    app = CaffeinaterApp()
    app.run()
