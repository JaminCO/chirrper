from flaskblog import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    #app.run(host="0.0.0.0", port=8000)
