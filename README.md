# flask_require

This is a simple library to help you write cleaner flask code.

## Installation

```bash
pip install git+https://github.com/ivario123/flask_require
```

## Usage

```python
from flask import Flask,request
import require

app = Flask(__name__)

@app.route('/')
@require.fields(request)
def index(name):
    return 'Hello, %s!' % name

if __name__ == '__main__':
    app.run()
```

## Usage of admin

```python
from flask import Flask,request
from require import fields, admin

app = Flask(__name__)

@app.route('/')
@fields(request)
def index(name):
    return 'Hello, %s!' % name

@app.route('/admin')
@admin()
def admin():
    return 'Hello, admin!'

def callback():
    print('Hello, callback!')

@app.route('/admin_with_callback')
@admin(callback)
def admin_with_callback():
    return 'Hello, admin with callback!'
```
