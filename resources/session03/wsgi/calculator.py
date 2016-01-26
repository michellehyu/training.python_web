import re


def resolve_path(path):
    urls = [(r'^$', welcome),
            (r'^add/(\d+)/(\d+)$', add),
            (r'^subtract/(\d+)/(\d+)$', subtract),
            (r'^divide/(\d+)/(\d+)$', divide),
            (r'^multiply/(\d+)/(\d+)$', multiply)]
    
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    # we get here if no url matches
    raise NameError

def welcome():
    return "<h1>welcome</h1>"

def multiply(v1, v2):
    r = int(v1) * int(v2)
    return "<h1>result from multiplication: %d</h1>" %r

def add(v1, v2):
    r = int(v1) + int(v2)
    return "<h1>result from addition: %d</h1>" % r  

def subtract(v1, v2):
    r = int(v1) - int(v2)
    return "<h1>result from subtraction: %d</h1>" % r

def divide(v1, v2):
    r = int(v1) / int(v2)
    return "<h1>result from division: %d</h1>" % r

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
