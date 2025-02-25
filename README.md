# Chess Game Web Application

A modern, interactive chess game web application built with Django, featuring both player vs player and player vs computer gameplay modes.

## Features

- Real-time chess gameplay with an intuitive user interface
- Player vs Player mode for challenging friends
- Player vs Computer mode with AI opponent
- Move validation and game state tracking
- Beautiful, responsive chessboard interface
- Move history tracking
- Undo move functionality
- Game state notifications (check, checkmate, stalemate)
- User authentication system

## Technologies Used

- Backend: Django (Python web framework)
- Frontend: HTML, CSS, JavaScript
- Chess Logic: chess.js
- Chessboard UI: chessboard.js
- Styling: Bootstrap 5
- Database: SQLite

## Setup Instructions

1. Clone the repository
2. Install Python 3.x if not already installed
3. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install django
   ```
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```
7. Visit http://localhost:8000 in your web browser

## How to Play

1. Register an account or log in
2. Click "Start New Game" on the home page
3. Choose game mode:
   - Play Against Computer: Challenge the AI opponent
   - Play Against Player: Challenge another player
4. Make moves by either:
   - Dragging and dropping pieces
   - Clicking the piece and then clicking the destination square
5. Use the move history panel to track game progress
6. The status bar shows current game state and whose turn it is

## Game Features

### Move Validation
- Legal move checking
- Check and checkmate detection
- Stalemate detection
- Insufficient material detection

### User Interface
- Responsive design that works on both desktop and mobile
- Clear game status indicators
- Move history panel
- Highlighted squares for selected pieces
- Undo move option for players

### AI Opponent
- Computer player for single-player games
- Automated responses to player moves

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.