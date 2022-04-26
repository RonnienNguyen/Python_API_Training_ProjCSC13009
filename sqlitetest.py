
import sqlite3
conn = sqlite3.connect('customer.db')
c = conn.cursor()

c.execute("INSERT INTO users VALUES ('PHUC', 'NGUYEN', 'ndtphuclqd1306@gmail.com')")
# c.execute("""CREATE TABLE users (
#                 first_name text,
#                 last_name text,
#                 email text)""")
conn.commit()
conn.close()