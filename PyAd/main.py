from flask_bootstrap import Bootstrap

from __init__ import create_app

app = create_app()
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    # app.run(debug=True)  # run the flask app on debug mode
 app.run(debug=True , port=5555)