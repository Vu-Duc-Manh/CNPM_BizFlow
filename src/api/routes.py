from api.controllers.todo_controller import bp

def register_routes(app):
    app.register_blueprint(bp)
