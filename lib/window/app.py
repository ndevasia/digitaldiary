from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    print("Home route accessed")  # This will print to your terminal
    return render_template('layout.html')

if __name__ == '__main__':
    app.run(debug=True)
