from app import app
from waitress import serve

if __name__ == '__main__':
    app.run(debug=True)   # development server
    # serve(app, host='0.0.0.0', port=5000) # deploy server
    