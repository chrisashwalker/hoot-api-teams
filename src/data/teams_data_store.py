from models.team import Team

def init_teams():
    return [Team(i, f'Team{i}').__dict__ for i in range(1,5)]