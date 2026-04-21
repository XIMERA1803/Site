import sqlite3

class DataBase:
    def __init__(self, path="db.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()

    def change_project(self, id, name, description, photo, url):
        self.cur.execute(
            """UPDATE projects 
            SET title=?, description=?, image=?, url=? 
            WHERE ID = ?""", 
            (name, description, photo, url, id,)
        )
        self.conn.commit()

    def select_all(self):
        result = self.cur.execute("SELECT * FROM projects").fetchall()
        return result

    def create_project(self, name, description, photo, url):
        self.cur.execute(
            """
            INSERT INTO 
            projects (title, description, image, url) 
            VALUES (?, ?, ?, ?);
            """, 
            (name, description, photo, url)
        )
        self.conn.commit()

    def delete_project(self, id):
        sql = f"DELETE FROM projects WHERE id = {id}"
        self.cur.execute(sql)
        self.conn.commit()

    def get_photo_id(self, id):
        select_photo = self.cur.execute(
            f"SELECT image FROM projects WHERE id = {id}"
        ).fetchall()
        return select_photo[0][0]


class UserDB:
    def __init__(self, path="db.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()

    def get_user_by_username(self, username):
        res = self.cur.execute(
            f"SELECT * FROM users WHERE username = {username}"
        ).fetchone()

        return res

