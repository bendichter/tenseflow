# tenseflow
tenseflow automatically changes the tense of any English text.

<img src="static/screenshot.png" width="350">

## Features
- change to `'past'`, `'present'`, or `'future'` tense
- includes web app


## Installation

Unfortunately, the package is only compatible with python 2.7 and 3.6.

Install this package
```
git clone https://github.com/bendichter/tenseflow.git
cd tenseflow
pip install .
```
download default English SpaCy model
```
sudo python -m spacy download en
```

## Usage
Basic usage
```python
from tenseflow import change_tense

change_tense('I will go to the store.', 'past')
u'I went to the store.'
```

Run web app
```
export FLASK_APP=app.py
flask run
```

## Testing
[![Build Status](https://travis-ci.org/bendichter/tenseflow.png?branch=master)](https://travis-ci.org/bendichter/tenseflow)

To test, install pytest with `pip install pytest`, then run `pytest` from within the tenseflow directory.
