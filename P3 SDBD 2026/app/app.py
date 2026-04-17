import os
import sys
import time
import engineio.async_drivers.threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Konfigurasi path untuk PyInstaller agar bisa membaca folder templates saat jadi .exe
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

app.config['SECRET_KEY'] = 'rahasia_negara'
socketio = SocketIO(app) 

# Global State Management (Penyimpanan Data In-Memory)
players = {} # Format: { session_id: {'nickname': 'Budi', 'status': 'waiting', 'time': 0} }
game_state = 'waiting' # Status: 'waiting', 'ready', 'playing', 'finished'
start_time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room')
def room():
    return render_template('room.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# --- SOCKET.IO EVENTS ---

@socketio.on('join')
def handle_join(data):
    nickname = data['nickname']
    players[request.sid] = {'nickname': nickname, 'status': 'waiting', 'time': 0}
    emit('update_players', list(players.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in players:
        del players[request.sid]
        emit('update_players', list(players.values()), broadcast=True)

@socketio.on('click_button')
def handle_click():
    global game_state, start_time
    sid = request.sid
    
    if sid not in players: return
    
    # Jika klik terlalu cepat (sebelum hijau)
    if game_state in ['waiting', 'ready'] and players[sid]['status'] == 'waiting':
        players[sid]['status'] = 'disqualified'
        emit('player_status', {'status': 'disqualified'}, to=sid)
        
    # Jika klik saat hijau
    elif game_state == 'playing' and players[sid]['status'] == 'waiting':
        reaction_time = time.time() - start_time
        players[sid]['status'] = 'finished'
        players[sid]['time'] = round(reaction_time, 3)
        emit('player_status', {'status': 'finished', 'time': players[sid]['time']}, to=sid)

@socketio.on('start_game')
def handle_start(data):
    global game_state
    if game_state != 'waiting': return # Mencegah double start
    
    wait_t = float(data['wait_time'])
    active_t = float(data['active_time'])
    
    # Reset status player
    for p in players.values():
        p['status'] = 'waiting'
        p['time'] = 0
    
    socketio.start_background_task(game_loop, wait_t, active_t)

def game_loop(wait_t, active_t):
    global game_state, start_time
    
    # Fase Siap-siap (Tombol Kuning)
    game_state = 'ready'
    socketio.emit('game_ready')
    socketio.sleep(wait_t)
    
    # Fase Mulai (Tombol Hijau)
    game_state = 'playing'
    start_time = time.time()
    socketio.emit('game_start')
    socketio.sleep(active_t)
    
    # Fase Selesai
    game_state = 'finished'
    
    # Diskualifikasi yang tidak klik sama sekali
    for sid, p in players.items():
        if p['status'] == 'waiting':
            p['status'] = 'disqualified'
            
    # Buat Leaderboard
    valid_players = [p for p in players.values() if p['status'] == 'finished']
    valid_players = sorted(valid_players, key=lambda x: x['time'])
    
    disqualified_players = [p for p in players.values() if p['status'] == 'disqualified']
    
    leaderboard = valid_players + disqualified_players
    
    socketio.emit('game_over', {'leaderboard': leaderboard, 'all_players': list(players.values())})

@socketio.on('reset_game')
def handle_reset():
    global game_state
    game_state = 'waiting'
    for p in players.values():
        p['status'] = 'waiting'
        p['time'] = 0
    emit('game_reset', broadcast=True)
    emit('update_players', list(players.values()), broadcast=True)

if __name__ == '__main__':
    print("Server berjalan! Silakan buka http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)