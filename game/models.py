from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    white_player = models.ForeignKey(User, related_name='white_games', on_delete=models.CASCADE)
    black_player = models.ForeignKey(User, related_name='black_games', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    game_state = models.TextField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    current_turn = models.CharField(max_length=5, default='white')
    is_finished = models.BooleanField(default=False)
    winner = models.ForeignKey(User, related_name='won_games', null=True, blank=True, on_delete=models.SET_NULL)
    is_bot_game = models.BooleanField(default=False)

    def __str__(self):
        return f'Game between {self.white_player.username} and {self.black_player.username}'

class Move(models.Model):
    game = models.ForeignKey(Game, related_name='moves', on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name='moves', on_delete=models.CASCADE)
    from_square = models.CharField(max_length=2)
    to_square = models.CharField(max_length=2)
    piece = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.player.username} moved {self.piece} from {self.from_square} to {self.to_square}'