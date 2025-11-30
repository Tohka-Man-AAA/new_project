import sqlite3
from config import DATABASE

skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Telegram'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]

class DB_Manager:
    def __init__(self, database):
        self.database = database # имя базы данных
        
    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute('CREATE TABLE projects(project_id INTEGER PRIMARY KEY, user_id INTEGER, project_name TEXT NOT NULL, description TEXT, url TEXT, status_id INTEGER, FOREIGN KEY(status_id) REFERENCES statuses(status_id))')
            con.execute('CREATE TABLE statuses(status_id INTEGER PRIMARY KEY, status_name TEXT)')
            con.execute('CREATE TABLE project_skills(project_id INTEGER, skill_id INTEGER, FOREIGN KEY(project_id) REFERENCES projects(project_id), FOREIGN KEY(skill_id) REFERENCES skills(skill_id))')
            con.execute('CREATE TABLE skills(skills_id INTEGER PRIMARY KEY, skill_name TEXT)')
            con.commit()


    def __executemany(self, sql, data):
        con = sqlite3.connect(self.database)
        with con:
            con.executemany(sql,data)
            con.commit()

    def __select_data(self, sql, data=tuple()):
        con = sqlite3.connect(self.database)
        with con:
            cur = con.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)

    






if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
