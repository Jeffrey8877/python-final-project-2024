import sqlite3

def create_question():
    # Connect to the SQLite database
    connection = sqlite3.connect("database/quiz.db")
    cursor = connection.cursor()

    try:
        # Open the SQL script file
        with open('questions.sql', 'r') as f:
            # Read and execute the script
            sql_script = f.read()
            cursor.executescript(sql_script)
            print("Quiz database has been created successfully.")
    except FileNotFoundError:
        print("Error: The file 'questions.sql' was not found.")
    except sqlite3.Error as e:
        print(f"An error occurred with SQLite: {e}")
    finally:
        # Close the database connection
        connection.commit()
        connection.close()

if __name__ == "__main__":
    create_question()
