from flask import url_for
from garden import app


def take(iter, n):
    results = []
    for r in iter:
        results.append(r)
        if len(results) == n:
            break
    return results

def _static_url(dir, file, **kwargs):
    return url_for('static', filename='%s/%s' % (dir, file), **kwargs)

def img_url(path):
    return _static_url('img', path)
    
    
def js_url(path):
    return _static_url('js', path)
    
    
def css_url(path):
    return _static_url('css', path)


app.jinja_env.globals.update({
    'img_url': img_url,
    'js_url': js_url,
    'css_url': css_url
})