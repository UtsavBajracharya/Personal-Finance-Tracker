from flask import Flask


app = Flask(__name__)

@app.get("/")
def home():
    return "Hello From Flask In Window"

if __name__ == "__main__":
    app.run(debug=True)

