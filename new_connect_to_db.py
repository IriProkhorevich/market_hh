import psycopg2
try:
    connection = psycopg2.connect(
        host="localhost",
        port="5433",
        database="data",
        user="postgres",
        password="good"
    )

    # Создание курсора для выполнения операций с базой данных
    cursor = connection.cursor()
    query =  "SELECT version()"
    cursor.execute(query)
    print(f"Server version: {cursor.fetchone()}")

    # Здесь вы можете выполнять запросы к базе данных
    # Например, cursor.execute("YOUR_SQL_QUERY")

except Exception as error:
    print(f"Ошибка при подключении к PostgreSQL: {error}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")