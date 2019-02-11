class Config():
    def __init__(self,config):
        self.r = config # raw config
        print('Config.yaml: ',self.r)
        if not self.r.get('groups'):
            self.r['groups'] = {}
    def isIn(self,group,player):
        if not self.r['groups'].get(group):
            return None, "group does not exist"
        elif player not in self.r['groups'][group]['u']:
            return False, "player is not in group"
        else:
            return True, "player is in group"
    def listGroups(self,player):
        # TODO: add inherited groups
        groups = []
        for k,v in self.r['groups'].items():
            if player in v['u']:
                groups.append(k)
        return groups
    def listPermissions(self,player):
        groups = self.listGroups(player)
        perms = []
        for i in groups:
            i = self.r['groups'][i]
            for j in i['p']:
                perms.append(j)
        return perms
    def getData(self,player):
        groups = self.listGroups(player)
        data = {}
        for i in groups:
            i = self.r['groups'][i]
            if i.get('d'):
                data = {**data,**i['d']}
        return data

    def hasPermission(self,player,perm):
        perm = perm.split('.')
        for i in self.listPermissions(player):
            i = i.split('.')
            matches = True
            for j,k in zip(i,perm):
                if j == '*':
                    pass
                elif j != k:
                    matches = False
                    break
            if matches:
                return True
        return False
