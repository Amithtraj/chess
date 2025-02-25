from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Game, Move
from django.contrib.auth.models import User
from .chess_bot import ChessBot
from .chess_logic import ChessGame

def home(request):
    return render(request, 'game/home.html')

@login_required
def new_game(request):
    if request.method == 'POST':
        game_type = request.POST.get('game_type')
        if game_type == 'bot':
            game = Game.objects.create(
                white_player=request.user,
                black_player=request.user,  # Temporarily use same user for bot games
                is_bot_game=True
            )
        else:
            opponent_id = request.POST.get('opponent')
            opponent = get_object_or_404(User, id=opponent_id)
            game = Game.objects.create(
                white_player=request.user,
                black_player=opponent
            )
        return redirect('play_game', game_id=game.id)  # Redirect to the game page
    players = User.objects.exclude(id=request.user.id)
    return render(request, 'game/new_game.html', {'players': players})

@login_required
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        'game': game,
        'is_player_turn': (
            (game.current_turn == 'white' and request.user == game.white_player) or
            (game.current_turn == 'black' and not game.is_bot_game)
        )
    }
    return render(request, 'game/play.html', context)

@login_required
def make_move(request, game_id):
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        if game.is_finished:
            return JsonResponse({'error': 'Game is already finished'}, status=400)
        
        # Verify it's the player's turn
        if (game.current_turn == 'white' and request.user != game.white_player) or \
           (game.current_turn == 'black' and not game.is_bot_game and request.user != game.black_player):
            return JsonResponse({'error': 'Not your turn'}, status=400)

        # Process the move using ChessGame logic
        chess_game = ChessGame(game.game_state)
        from_square = request.POST.get('from')
        to_square = request.POST.get('to')

        # Additional validation for piece ownership
        piece = chess_game.get_piece_at(from_square)
        if not piece:
            return JsonResponse({'error': 'No piece at selected square'}, status=400)
        
        is_white_piece = piece.isupper()
        if (game.current_turn == 'white' and not is_white_piece) or \
           (game.current_turn == 'black' and is_white_piece):
            return JsonResponse({'error': 'Cannot move opponent\'s piece'}, status=400)

        # Validate and make the move
        move_result = chess_game.make_move(from_square, to_square)
        if move_result['status'] == 'error':
            return JsonResponse({'error': move_result['message']}, status=400)

        # Create move record
        Move.objects.create(
            game=game,
            player=request.user,
            from_square=from_square,
            to_square=to_square,
            piece=move_result['piece']
        )

        # Update game state
        game.game_state = move_result['game_state']
        game.current_turn = move_result['current_turn']
        
        # Check for game end conditions
        if move_result['is_checkmate']:
            game.is_finished = True
            game.winner = request.user
            game.save()
            return JsonResponse({'status': 'success', 'is_checkmate': True})

        game.save()

        # If it's a bot game and it's the bot's turn, make the bot move
        if game.is_bot_game and game.current_turn == 'black':
            bot = ChessBot()
            bot.set_board(game.game_state)
            bot_move = bot.get_best_move()
            
            if bot_move:
                Move.objects.create(
                    game=game,
                    player=game.black_player,
                    from_square=bot_move['from'],
                    to_square=bot_move['to'],
                    piece=bot_move['piece']
                )
                
                game.game_state = bot_move['game_state']
                game.current_turn = 'white'
                
                if bot_move['is_checkmate']:
                    game.is_finished = True
                    game.winner = game.black_player
                
                game.save()
                
                return JsonResponse({
                    'status': 'success',
                    'game_state': bot_move['game_state'],
                    'current_turn': bot_move['current_turn'],
                    'bot_move': bot_move,
                    'is_checkmate': bot_move['is_checkmate'],
                    'is_check': bot_move['is_check'],
                    'is_stalemate': bot_move['is_stalemate'],
                    'is_insufficient_material': bot_move['is_insufficient_material']
                })

        return JsonResponse({
            'status': 'success',
            'game_state': move_result['game_state'],
            'current_turn': move_result['current_turn'],
            'is_check': move_result['is_check'],
            'is_checkmate': move_result['is_checkmate'],
            'is_stalemate': chess_game.board.is_stalemate(),
            'is_insufficient_material': chess_game.board.is_insufficient_material()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
