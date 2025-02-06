from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # debug=True means server will re-run whenever there's changes to the Python code