
class Movie:
    def __init__(self, title: str, year: int):
        self.title = title
        self.year = year

class TVShow:
    def __init__(self, title: str, year: int):
        self.title = title
        self.year = year

class TVSeason:
    def __init__(self, show: TVShow, season: int):
        self.show = show
        self.season = season

class TVEpisode:
    def __init__(self, season: TVSeason, episode: int, title: str = None):
        self.show = season.show
        self.season = season
        self.episode = episode
        self.title = title