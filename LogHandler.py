import os
from datetime import datetime

class LogHandlerClass:

    def __init__(self, name, path = os.getcwd()):
        self.time = datetime.now()
        self.name = name + self.time.strftime("_%Y_%m_%d_%H_%M") + ".txt"
        self.path = path
        self.open_file_rw()

    def open_file_rw(self):
        try:
            self.file = open(self.name, 'w+')
        except:
            print(f"Failed to open the file")
        else:
            print("Log file is opened")

    def close_file(self):
        self.file.close()

    def find_in_file(self, offset, whence):
        self.file.seek(offset=offset, whence= whence)

    def add_line(self, text, end = "\n"):
        current_time = self.time.strftime("%Y:%m:%d:%H:%M:%S")
        try:
            self.file.write(f"{current_time}: {text}{end}")
        except:
            # TODO Handle file write error
            pass
        else:
            pass

    def read_from_file(self, num):
        return self.file.read(num)