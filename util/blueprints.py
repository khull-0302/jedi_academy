import routes


def register_blueprint(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.lightsaber)
    app.register_blueprint(routes.master)
    app.register_blueprint(routes.padawan)
    app.register_blueprint(routes.species)
    app.register_blueprint(routes.temple)
    app.register_blueprint(routes.user)
    app.register_blueprint(routes.course)
    
    