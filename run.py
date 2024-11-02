from app import create_app, socketio
import psycopg2

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)