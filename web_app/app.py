from flask import Flask, render_template, jsonify, request
from game_logic import Game, LIGHT_ON, LIGHT_OFF # Import Game and constants
from ranking_utils import get_rankings, add_score # Import ranking utilities
from datetime import datetime # Import datetime

app = Flask(__name__)

# Initialize the game instance
game = Game()
server_moves_count = 0

@app.route('/')
def game_page():
    return render_template('index.html')

@app.route('/ranking')
def ranking_page():
    rankings_data = get_rankings()
    return render_template('ranking.html', rankings=rankings_data)

@app.route('/api/gamestate')
def get_gamestate():
    global server_moves_count
    return jsonify({
        'board': game.get_board(),
        'moves': server_moves_count,
        'light_on_char': LIGHT_ON,  # Send the actual character for ON
        'light_off_char': LIGHT_OFF # Send the actual character for OFF
    })

@app.route('/api/click/<int:row>/<int:col>')
def handle_click(row, col):
    global server_moves_count
    # Assuming game methods use 0-indexed row/col
    game.toggle_cell_and_neighbors(row, col)
    server_moves_count += 1
    win_status = game.check_win()
    
    if win_status:
        # If the game is won, we can save the score.
        # We can log that a win occurred.
        # print(f"Win condition met in {server_moves_count} moves. Score not saved yet.")
        pass # No longer need to print, client will prompt for name.

    return jsonify({
        'board': game.get_board(),
        'moves': server_moves_count,
        'win': win_status
    })

@app.route('/api/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    if not data or 'name' not in data or 'moves' not in data:
        return jsonify({'success': False, 'message': 'Nome ou jogadas ausentes.'}), 400
    
    player_name = data['name']
    moves_count = data['moves']
    
    # Basic validation for moves_count
    if not isinstance(moves_count, int) or moves_count <= 0:
        return jsonify({'success': False, 'message': 'Contagem de jogadas inválida.'}), 400

    current_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        add_score(player_name, moves_count, current_date_str)
        return jsonify({'success': True, 'message': 'Pontuação enviada com sucesso!'})
    except Exception as e:
        # Log the exception e for debugging
        print(f"Error submitting score: {e}")
        return jsonify({'success': False, 'message': 'Falha ao enviar pontuação devido a erro no servidor.'}), 500

@app.route('/api/reset')
def reset_game():
    global server_moves_count
    game.reset_board()
    server_moves_count = 0
    return jsonify({
        'board': game.get_board(),
        'moves': server_moves_count
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
