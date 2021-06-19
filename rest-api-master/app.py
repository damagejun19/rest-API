import pymysql
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


from flask import jsonify
from flask import request
from flask import session

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

app = Flask(__name__)
api = Api(app)


db = pymysql.connect(
        user = 'son',
        passwd = '111111',
        host = '127.0.0.1',
        port = 3306,
        db = 'testdb',
        charset = 'utf8'
    )
cursor = db.cursor()


app.config.from_mapping(SECRET_KEY='dev')

parser.add_argument('id')
parser.add_argument('fullname')
parser.add_argument('email')
parser.add_argument('password')

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
        if request.method=='POST':
                try:
                        args = parser.parse_args()
                        sql = "INSERT INTO `user` (`fullname`, `email`, `password`) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (args['fullname'], args['email'], generate_password_hash(args['password'])))
                        db.commit()

                        return jsonify(status="success", result="registered")
                except:
                        return jsonify(result="already exist email")
        else:
                sql = "SELECT id, fullname FROM `user`"
                cursor.execute(sql)
                result = cursor.fetchall()

                return jsonify(status="success", result=result)


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
                args = parser.parse_args()
                sql = "SELECT fullname, password FROM `user` WHERE email=%s"
                cursor.execute(sql, args['email'])
                result = cursor.fetchall()
                if len(result) > 0:
                        if check_password_hash(result[0][1], args['password']):
                                session['logged_in'] = True
                                return jsonify(status="success", result="Welcome")
                        else:
                                return jsonify(status="Login Failed", result="Incorrect password")

                else:
                        return jsonify(status="Login Failed", result="A matching ID cannot be found.")
        else:
                return jsonify("Login is required")


@app.route('/auth/logout')
def logout():
        session['logged_in'] = False
        return jsonify("You're logged out.")


parser = reqparse.RequestParser()
parser.add_argument("id")
parser.add_argument("name")


class Board(Resource):
        def get(self):
                sql = "SELECT id, name FROM `board`"
                cursor.execute(sql)
                result = cursor.fetchall()
                return jsonify(status="success", result=result)

        def post(self):
                args = parser.parse_args()
                sql = "INSERT INTO `board` (`name`) VALUES (%s)"
                cursor.execute(sql, (args['name']))
                db.commit()

                return jsonify(status="success", result={"name": args["name"]})

        def put(self):
                args = parser.parse_args()
                sql = "UPDATE `board` SET name = %s WHERE `id` = %s"
                cursor.execute(sql, (args['name'], args["id"]))
                db.commit()

                return jsonify(status="success", result={"id": args["id"], "name": args["name"]})

        def delete(self):
                args = parser.parse_args()
                sql = "DELETE FROM `board` WHERE `id` = %s"
                cursor.execute(sql, (args["id"],))
                db.commit()

                return jsonify(status="success", result={"id": args["id"]})


parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('content')
parser.add_argument('board_id')


class BoardArticle(Resource):
        def get(self, board_id=None, board_article_id=None):
                if board_article_id:
                        sql = "SELECT id, title, content FROM `boardArticle` WHERE `id`=%s"
                        cursor.execute(sql, (board_article_id,))
                        result = cursor.fetchone()
                else:
                        sql = "SELECT id, title, content FROM `boardArticle` WHERE `board_id`=%s"
                        cursor.execute(sql, (board_id,))
                        result = cursor.fetchall()

                return jsonify(status="success", result=result)

        def post(self, board_id=None):
                args = parser.parse_args()
                sql = "INSERT INTO `boardArticle` (`title`, `content`, `board_id`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (args['title'], args['content'], args['board_id']))
                db.commit()

                return jsonify(status="success", result={"title": args["title"]})

        def put(self, board_id=None, board_article_id=None):
                args = parser.parse_args()
                sql = "UPDATE `boardArticle` SET title = %s, content = %s WHERE `id` = %s"
                cursor.execute(sql, (args['title'], args["content"], args["id"]))
                db.commit()

                return jsonify(status="success", result={"title": args["title"], "content": args["content"]})

        def delete(self, board_id=None, board_article_id=None):
                args = parser.parse_args()
                sql = "DELETE FROM `boardArticle` WHERE `id` = %s"
                cursor.execute(sql, (args["id"],))
                db.commit()

                return jsonify(status="success", result={"id": args["id"]})



class Dashboard(Resource):
        def get(self):
                sql = "SELECT title FROM `boardArticle`"
                cursor.execute(sql)
                result = cursor.fetchall()
                return jsonify(status="success", result=result)




# API Resource 라우팅을 등록!
api.add_resource(Board, '/board')
api.add_resource(BoardArticle, '/board/<board_id>', '/board/<board_id>/<board_article_id>')
api.add_resource(Dashboard, '/dashboard')
if __name__ == '__main__':
        app.run()