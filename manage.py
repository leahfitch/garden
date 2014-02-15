from flask.ext.script import Manager
from garden import app
from garden.scripts import importjson

manager = Manager(app)
manager.add_command('import', importjson.ImportJSON)

if __name__ == "__main__":
    manager.run()