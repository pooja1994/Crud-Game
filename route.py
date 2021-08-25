from app import *


def process_request(function):
    if authenticate():
        return function()
    else:
        return Response("Invalid Token", 401, mimetype='application/json')


@app.route('/app/listgames', methods=['GET'])
def get_all_games():
    def innerfunction():
        genre = request.args.get('genre')
        score = request.args.get('score')
        platform = request.args.get('platform')
        editors_choice = request.args.get('editors_choice')
        sort = request.args.get('sort')
        return jsonify({'Games': Game.get_all_games(genre, platform, score, editors_choice, sort)})

    return process_request(innerfunction)


@app.route('/app/getbytitle', methods=['GET'])
def get_game_by_title():
    def innerfunction():
        return_value = Game.get_game(request.args.get('title'))
        return jsonify(return_value)

    return process_request(innerfunction)


# route to add new movie
@app.route('/app/add', methods=['POST'])
def add_game():
    '''Function to add new movie to our database'''

    def innerfunction():
        request_data = request.get_json()  # getting data from client
        Game.add_game(request_data["id"], request_data["title"], request_data["platform"], request_data["genre"],
                      request_data["score"], request_data["editors_choice"])
        response = Response("game added", 200, mimetype='application/json')
        return response

    return process_request(innerfunction)


# route to update movie with PUT method
@app.route('/app/update/<int:id>', methods=['PUT'])
def update_game(id):
    '''Function to edit movie in our database using movie id'''

    def innerfunction():
        request_data = request.get_json()
        Game.update_game(id, request_data["title"], request_data["platform"], request_data["genre"],
                         request_data["score"], request_data["editors_choice"])
        response = Response("Game Updated", status=200, mimetype='application/json')
        return response

    return process_request(innerfunction)


# route to delete movie using the DELETE method
@app.route('/app/delete/<int:id>', methods=['DELETE'])
def remove_game(id):
    '''Function to delete movie from our database'''

    def innerfunction():
        Game.delete_game(id)
        response = Response("Movie Deleted", status=200, mimetype='application/json')
        return response

    return process_request(innerfunction)


@app.route('/app/signup', methods=['POST'])
def signup():
    json_log = request.get_json()
    user_id = json_log['user_id']
    password = json_log['password']
    User.add_user(user_id, password)
    response = Response('successfully signed up', status=200, mimetype='application/json')
    return response


@app.route('/app/login', methods=['POST'])
def login():
    json_log = request.get_json()
    user_id = json_log['user_id']
    password = json_log['password']
    token = User.login(user_id, password)
    response = Response(token, status=200, mimetype='application/json')
    return response


def authenticate():
    # get the auth token
    auth_header = request.headers.get('Authorization')

    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
            return User.authenticate(auth_token)
        except IndexError:
            return False
    else:
        return False


if __name__ == "__main__":
    app.debug = True
    app.run()
