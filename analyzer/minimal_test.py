print("Test 1")

from flask import Flask
print("Test 2")

app = Flask(__name__)
print("Test 3")

@app.route('/')
def home():
    return "Hello"

print("Test 4")

if __name__ == '__main__':
    print("Test 5")
    app.run(port=8080)
    print("Test 6") 