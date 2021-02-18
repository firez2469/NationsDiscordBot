class Nation:
    def __init__(self, name, influence, leaderUser):
        self.name = name
        self.influence = influence
        self.leaderUser = leaderUser
    def addInfluence(self):
        self.influence+=1
