class Config:
    home_dir = ""
    remote_dir = ""
    address = ""
    port = 22
    username = ""
    mode = ""
    ignore = []

    def __init__(self,config):
        if config == None:
            print("Cannot create config")
        else:
            self.home_dir = config["local_directory"]
            self.remote_dir = config["remote_directory"]
            self.address = config["server_address"]
            self.port = config["port"]
            self.username = config["username"]
            self.mode = config["mode"]
            self.ignore = config["ignore"]


