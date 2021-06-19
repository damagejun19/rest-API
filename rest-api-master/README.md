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



sign up api입니다. http request = POST 일 때 fullname, email, password를 데이터베이스 저장하고 password는 보안을 위해서 hash를 사용하여 저장했습니다. 저장에 성공하면 status="success", result="registered"가 출력되도록 작성하였습니다.

회원가입을 하는데 중복된 이메일로 가입을 하면 try-except구문을 이용하여 already exist email라는 메세지가 출력하도록 만들었습니다.

http request=GET 일 때 id번호와 fullname을 반환하도록 했습니다.

두번째 login API입니다.

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

http request=POST 일 때 입력한 이메일에 해당하는 fullname과 password를 불러오고 불러온 튜플의 길이가 0보다 크면 user table에 존재하는 이메일이라고 판단했고, 0이면 존재하지 않는 아이디라는 문구를 반환하게 만들었습니다. 

아이디가 존재하면 hash토큰으로 만들어진 비밀번호와 비교하여 true를 반환하면 로그인이 성공하고, 없으면 틀린 비밀번호를 출력하게 만들었습니다.

http request=GET 일 때는 로그인이 필요하다는 문구가 출력되도록 만들었습니다.

@app.route('/auth/logout')
def logout():
    session['logged_in'] = False
    return jsonify("You're logged out.")

로그아웃은 session을 종료시킴으로 로그아웃 됐다는 문구가 출력되도록 만들었습니다.

Board API는 get, post, put, delete로 나눴고 성공하면 가가 알맞는 문구가 출력되도록 만들었습니다.

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

BoardArticle API는 board_id를 입력하면 그 페이지에 있는 제목과 내용이 출력되도록 만들었고 board_article_id번호를 입력하면 해당하는 하나의 게시글의 제목과 내용이 출력되도록 만들었습니다.

class Dashboard(Resource):
    
    def get(self):
        sql = "SELECT title FROM `boardArticle`"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(status="success", result=result)

Dashboard는 boardArticle에 있는 모든 title이 출력되도록 만들었습니다.