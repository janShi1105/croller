from flask import Flask, abort
from flask_restful import Api, Resource, reqparse

from db import Film

app = Flask(__name__)

api = Api(app)

class FilmItem(Resource):
    def get(self, film_id):
        try:
            film = Film.get(Film.film_id == film_id)
        except Film.DoesNotExist:
            abort(404, description="Film not found.")

        return film.to_dict()

class FilmList(Resource):

    ITEMS_PER_PAGE = 5

    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('page', type=int, default=1)
        super().__init__(*args, **kwargs)

    def get(self):
        args = self.parser.parse_args()

        films = Film.select().order_by(Film.film_id).paginate(args['page'], self.ITEMS_PER_PAGE)

        return [film.to_dict() for film in films]

api.add_resource(FilmItem, '/film/<int:film_id>')
api.add_resource(FilmList, '/films')

if __name__ == '__main__':
    app.run(debug=False)

        