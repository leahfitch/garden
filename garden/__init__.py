from flask import Flask
import os, os.path

app = Flask("garden")
basedir = os.path.abspath(os.path.join(app.root_path, '..'))

config_file = os.path.join(basedir, 'config.py')    

if os.path.exists(config_file):
    app.config.from_pyfile(config_file)
else:
    raise Exception, "Could not find config file %s" % config_file

import model, views, helpers