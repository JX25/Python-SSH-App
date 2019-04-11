class File:
    name = ""
    mtime = 0

    def __init__(self,name,mtime):
        self.name = name
        self.mtime = mtime


    def is_older(self,second_file):
        if self.mtime >= second_file.mtime:
            return False
        else:
            return True