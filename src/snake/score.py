class Score:
    def __init__(self):
        self.score: int = 0
        self.hiscore: int = 0

    def increase_score(self):
        self.score += 1
        if self.score > self.hiscore:
            self.hiscore = self.score

    def reset_score(self):
        self.score = 0
