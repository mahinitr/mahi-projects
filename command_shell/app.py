from collections import deque

class Status:
    SUCCESS = 1
    FAILED = 0

class Message:
    DIR_EXISTS = "Directory already exists"
    FILE_EXISTS = "File already exists"
    DIR_NOT_FOUND = "Directory not found"
    INVALID_NAME = "Invalid File or Folder Name"
    CMD_NOT_FOUND = "Unrecognized command"
    INVALID_CMD = "Invalid Command"
    SUCCESS = "Success"

class Command:
    QUIT = "quit"
    PWD = "pwd"
    LS = "ls"
    MKDIR = "mkdir "
    CD = "cd "
    TOUCH = "touch "


class File:

    def __init__(self, name, contents=''):
        self.name = name
        self.contents = contents

class Dir:

    def __init__(self, name, parent):
        self.name = name
        self.files = {}
        self.sub_dirs = {}
        self.parent_dir = parent

    def addSubDirectory(self, sub_dir_name):
        if sub_dir_name in self.sub_dirs:
            return Status.FAILED, Message.DIR_EXISTS
        if len(sub_dir_name) > 100:
            return Status.FAILED, Message.INVALID_NAME
        sub_dir = Dir(sub_dir_name, self)
        self.sub_dirs[sub_dir.name] = sub_dir
        return Status.SUCCESS, Message.SUCCESS

    def addFile(self, file_name):
        if len(file_name) > 100:
            return Status.FAILED, Message.INVALID_NAME
        if file_name in self.files:
            return Status.FAILED, Message.FILE_EXISTS
        f = File(file_name)
        self.files[file_name] = f
        return Status.SUCCESS, Message.SUCCESS

    def getPath(self):
        path = ''
        temp = self
        while(temp is not None):
            path = '/' + temp.name + path
            temp = temp.parent_dir
        return path

    def ls(self, **args):
        contents = []
        if "recursive" in args and args["recursive"] == True:
            dq = deque([self])
            while(len(dq) != 0):
                t_dir = dq.popleft()
                contents.append(t_dir.getPath())
                for each in t_dir.sub_dirs:
                    contents.append(each)
                    dq.append(t_dir.sub_dirs[each])
                for each in t_dir.files:
                    contents.append(each)
        else:
            for each in self.sub_dirs:
                contents.append(each)
            for each in self.files:
                contents.append(each)
        return contents

class FileSystem:

    _instance = None

    def __init__(self, root="root"):
        self.root = Dir(root, None)

    @staticmethod
    def instance():
        if FileSystem._instance is None:
            FileSystem._instance = FileSystem()
        return  FileSystem._instance

    def mkdir(self, pwd, dir_name):
        res = pwd.addSubDirectory(dir_name)
        if res[0] == 0:
            return res[1]
        return ""

    def cd(self, pwd, dir_name):
        if dir_name == "..":
            return pwd.parent_dir, ""
        if dir_name in pwd.sub_dirs:
            return pwd.sub_dirs[dir_name], ""
        return None, Message.DIR_NOT_FOUND

    def touch(self, pwd, file_name):
        res = pwd.addFile(file_name)
        if res[0] == 0:
            return res[1]
        return ""

class CommandShell:

    def __init__(self):
        self.fs = FileSystem()
        self.pwd = self.fs.root
        self.history = []

    def start(self):
        while(1):
            cmd = raw_input().strip()
            if cmd == Command.QUIT:
                break
            self.runCommand(cmd)

    @staticmethod
    def extractCmd(s, cmd):
        i = len(cmd)
        return s[i:].strip()
            
    def runCommand(self, cmd):
        if cmd == Command.PWD:
            print self.pwd.getPath()
        elif cmd.startswith(Command.LS):
            params = CommandShell.extractCmd(cmd, Command.LS)
            if params in ["-r"]:
                params = {"recursive" : True}
            else:
                params = {}
            res = self.pwd.ls(**params)     
            for each in res:
                print each
        elif cmd.startswith(Command.MKDIR):
            dir_name = CommandShell.extractCmd(cmd, Command.MKDIR)
            res = self.fs.mkdir(self.pwd, dir_name)
            if res:
                print res
        elif cmd.startswith(Command.CD):
            dir_name = CommandShell.extractCmd(cmd, Command.CD)
            res = self.fs.cd(self.pwd, dir_name)
            if res[0]:
                self.pwd = res[0]
            else:
                print res[1]
        elif cmd.startswith(Command.TOUCH):
            file_name = CommandShell.extractCmd(cmd, Command.TOUCH)
            res = self.fs.touch(self.pwd, file_name)
            if res:
                print res
        else:
            print Message.CMD_NOT_FOUND

if __name__ == "__main__":
        cmdShell = CommandShell()
        cmdShell.start()


