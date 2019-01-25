import time
from PySide2 import QtCore
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class QWatcher(QtCore.QObject):
    image_signal = QtCore.Signal(str)

    def __init__(self, image_dir, parent=None):
        super(QWatcher, self).__init__(parent)
        self.observer = Observer()
        self.image_dir = image_dir
        self.status = True


    def run(self):
        try:
            event_handler = Handler(self.image_signal)
            self.observer.schedule(event_handler, self.image_dir)
            self.observer.start()
            while self.status:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

    def stop(self):
        self.status = False

class Handler(FileSystemEventHandler):

    def __init__(self, sig, parent=None):
        super(Handler, self).__init__()
        self.signal = sig
        # print('Init Handler')

    # @staticmethod
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            self.signal.emit(event.src_path)

        # elif event.event_type == 'modified':
        #     # Taken any action here when a file is modified.
        #     print "Received modified event - %s." % event.src_path


if __name__ == '__main__':
    w = QWatcher('/Users/blakez/Documents/TestingGUI/testImageDir/')
    w.run()





# class QWatcher(QtCore.QObject):
#
#     def __init__(self, parent=None):
#         super(QWatcher, self).__init__(parent)
#
#         # Create a gui object.
#         # self.gui = Window()
#         self.image_signal = QtCore.pyqtSignal(str)
#
#         # Create a new worker thread and start observing
#         self.createWorkerThread()
#
#         # Make any cross object connections.
#         self._connectSignals()
#
#         self.gui.show()
#
#     def createWorkerThread(self):
#
#         # Setup the worker object and the worker_thread.
#         self.worker = Watcher()
#         self.worker_thread = QtCore.QThread()
#         self.worker.moveToThread(self.worker_thread)
#         self.worker_thread.start()
#         self.worker.run()
#
#         # Connect any worker signals
#         self.worker.signalStatus.connect(self.gui.updateStatus)
#         # self.gui.button_start.clicked.connect(self.worker.startWork)
