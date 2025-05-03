import mysql.connector
from mysql.connector import pooling

# Configure a connection pool
pool = pooling.MySQLConnectionPool(
    pool_name="AntiEvilTwin",
    pool_size=10,
    host="localhost",
    user="user",               
    password="pass",  
    database="evil_twin_db"    
)


def get_connection():
    return pool.get_connection()


def setup_tables():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                IpAddress VARCHAR(45) PRIMARY KEY,
                Reputation INT DEFAULT 0
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RecordedLimitThresholds (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                IpAddress VARCHAR(45),
                RecordedAt DATETIME,
                FOREIGN KEY (IpAddress) REFERENCES User(IpAddress)
            );
        """)

        conn.commit()
        #print("Tables created (if not existing).")
    except Exception as e:
        #print("Error creating tables:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    setup_tables()

