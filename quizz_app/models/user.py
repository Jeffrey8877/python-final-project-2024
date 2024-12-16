class User:
    """
    User model for database operations.
    This class doesn't store state - it's just a collection of database operations.
    """

    @staticmethod
    def create(conn, username, password, email):
        """
        Create a new user in the database.

        Args:
            conn: Database connection
            username: User's username
            password: User's password (will be stored as plaintext for now)
            email: User's email

        Returns:
            The new user's ID

        TODO: Student will implement password hashing here
        """
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
        """, (username, password, email))
        return cursor.lastrowid

    @staticmethod
    def get_by_id(conn, user_id):
        """
        Get user by their ID.

        Args:
            conn: Database connection
            user_id: The user's ID

        Returns:
            User data as a sqlite3.Row object or None if not found
        """
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    @staticmethod
    def get_by_username(conn, username):
        """
        Get user by their username.

        Args:
            conn: Database connection
            username: The username to look up

        Returns:
            User data as a sqlite3.Row object or None if not found
        """
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    @staticmethod
    def get_by_email(conn, email):
        """
        Get user by their email.

        Args:
            conn: Database connection
            email: The email to look up

        Returns:
            User data as a sqlite3.Row object or None if not found
        """
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

    @staticmethod
    def get_quiz_results(conn, user_id):
        """
        Get all quiz results for a user.

        Args:
            conn: Database connection
            user_id: The user's ID

        Returns:
            List of quiz results
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, q.title as quiz_title 
            FROM results r
            JOIN quizzes q ON r.quiz_id = q.id
            WHERE r.user_id = ?
            ORDER BY r.completed_at DESC
        """, (user_id,))
        return cursor.fetchall()

    @staticmethod
    def update_password(conn, user_id, new_password):
        """
        Update a user's password.

        Args:
            conn: Database connection
            user_id: The user's ID
            new_password: The new password (will be stored as plaintext for now)

        TODO: Student will implement password hashing here
        """
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET password = ?
            WHERE id = ?
        """, (new_password, user_id))
        conn.commit()