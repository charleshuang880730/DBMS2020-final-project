import sqlite3

class Handler():

    def __init__(self):
        self.conn = sqlite3.connect('DBproject.db') 
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def insert(self, S_NO, C_NO):
        sql = """INSERT INTO 選課資料表 VALUES (?, ?)"""
        self.cursor.execute(sql, (S_NO, C_NO))

    def delete(self, S_NO, C_NO):
        sql = """Delete FROM 選課資料表 WHERE 學號 = ? AND 課程代碼=?"""
        self.cursor.execute(sql, (S_NO, C_NO))

    def query(self, S_NO):
        sql = """SELECT 學號, 課程名稱, c.課程代碼, 學分數, 上課時間, 上課地點,
                 (SELECT 系名 FROM 系所資料表 WHERE 系所資料表.系代碼 = c.系所代碼)系名,
                 (SELECT 姓名 FROM 教師資料表 WHERE 教師資料表.教師代碼 = c.教師代碼)授課教師
                 FROM 課程資料表 AS c
                 INNER JOIN 選課資料表 AS t on c.課程代碼 = t.課程代碼
                 WHERE t.學號 = ?"""
        result = self.cursor.execute(sql, (S_NO,))
        return result.fetchall()
    
    def query_class(self, condition, D_NO):
        sql = """SELECT 課程名稱, 課程代碼, t.姓名, 類別, 學分數, 上課地點, 上課時間
                 FROM 課程資料表 AS c
                 LEFT JOIN 教師資料表 AS t on c.教師代碼 = t.教師代碼"""
        
        where_clause = """ WHERE 課程名稱 = ? OR c.系所代碼 = ? OR 姓名 = ?"""
        if condition or D_NO:
            result = self.cursor.execute(sql+where_clause, (condition, D_NO, condition))
        else:
            result = self.cursor.execute(sql)
        return result.fetchall()
        
    def query_user(self, S_NO):
        sql = """SELECT 姓名 FROM 學生資料表 WHERE 學號 = ?"""
        result = self.cursor.execute(sql, (S_NO,))
        return result.fetchone()

