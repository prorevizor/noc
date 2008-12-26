from noc.settings import config

def tt_url(self):
    if self.tt:
        return config.get("tt","url",0,{"tt":self.tt})
    else:
        return None
        
def admin_tt_url(self):
    if self.tt:
        return "<A HREF='%s'>#%s</A>"%(config.get("tt","url",0,{"tt":str(self.tt)}),str(self.tt))
    else:
        return ""
