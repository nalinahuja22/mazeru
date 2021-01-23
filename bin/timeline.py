# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

class Cut:
    def __init__(self, vfile, itime, otime):
        self.vfile = vfile
        self.itime = itime
        self.otime = otime

class Timeline:
    def __init__(self, adata, vdata):
        self.adata = adata
        self.vdata = vdata

    def render(self):
        pass
