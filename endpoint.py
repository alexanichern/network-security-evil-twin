from app import app

stored_paths = {}
created_functions = {}

def createEndPoint(path, methods, rate_limit, accept_function):
    if path in stored_paths or path in created_functions:
        print("path already exists")
        return

    stored_paths[path] = {"addresses": {}}
    created_functions[path] = {
        "rate_limit": rate_limit,
        "accept_function": accept_function
    }

    app.add_api_route(path, accept_function, methods=methods)

