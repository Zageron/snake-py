import pygame

from .score import Score


class ScoreView:
    def __init__(self, score: Score, font):
        self.score_string: str = None
        self.score_text_render = None

        self.font = font
        self.score: Score = score

        self.update_score_text()

    def update_score_text(self):
        self.score_string = str(self.score.score) + " / " + str(self.score.hiscore)
        self.score_text_render = self.font.render(
            self.score_string, True, pygame.Color(200, 200, 200)
        )

    def render(self, screen, size):
        screen.blit(
            self.score_text_render,
            self.score_text_render.get_rect(
                centerx=size[0] / 1.07, centery=size[1] / 14
            ),
        )
