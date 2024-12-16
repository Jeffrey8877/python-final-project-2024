class Quiz:
    """
    Quiz model for database operations.
    Handles quiz creation, retrieval, and result management.
    """

    @staticmethod
    def create(conn, title, description, time_limit=None):
        """
        Create a new quiz.

        Args:
            conn: Database connection
            title: Quiz title
            description: Quiz description
            time_limit: Time limit in minutes (optional)

        Returns:
            The new quiz's ID
        """
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO quizzes (title, description, time_limit)
            VALUES (?, ?, ?)
        """, (title, description, time_limit))
        return cursor.lastrowid

    @staticmethod
    def add_question(conn, quiz_id, question_text, correct_answer, options):
        """
        Add a question to a quiz.

        Args:
            conn: Database connection
            quiz_id: ID of the quiz
            question_text: The question itself
            correct_answer: The correct answer (a, b, c, or d)
            options: Dictionary with keys 'a', 'b', 'c', 'd' containing answer choices
        """
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions 
            (quiz_id, question_text, correct_answer, option_a, option_b, option_c, option_d)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (quiz_id, question_text, correct_answer,
              options['a'], options['b'], options['c'], options['d']))

    @staticmethod
    def get_by_id(conn, quiz_id):
        """
        Get quiz by ID, including all its questions.

        Args:
            conn: Database connection
            quiz_id: The quiz ID

        Returns:
            Quiz data with questions or None if not found
        """
        cursor = conn.cursor()
        # Get quiz details
        cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
        quiz = cursor.fetchone()

        if quiz:
            # Get all questions for this quiz
            cursor.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,))
            quiz = dict(quiz)  # Convert to regular dictionary
            quiz['questions'] = cursor.fetchall()
            return quiz
        return None

    @staticmethod
    def get_all(conn):
        """
        Get all quizzes with basic info (no questions).

        Args:
            conn: Database connection

        Returns:
            List of all quizzes
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT q.*, COUNT(DISTINCT qn.id) as question_count 
            FROM quizzes q 
            LEFT JOIN questions qn ON q.id = qn.quiz_id 
            GROUP BY q.id
        """)
        return cursor.fetchall()

    @staticmethod
    def grade_submission(conn, quiz_id, user_answers):
        """
        Grade a quiz submission.

        Args:
            conn: Database connection
            quiz_id: The quiz ID
            user_answers: Dictionary of question_id: selected_answer

        Returns:
            Score as a percentage
        """
        cursor = conn.cursor()
        cursor.execute("SELECT id, correct_answer FROM questions WHERE quiz_id = ?", (quiz_id,))
        questions = cursor.fetchall()

        if not questions:
            return 0

        correct = 0
        total = len(questions)

        for question in questions:
            question_id = str(question['id'])  # Convert to string to match form data
            if (question_id in user_answers and
                    user_answers[question_id] == question['correct_answer']):
                correct += 1

        return (correct / total) * 100

    @staticmethod
    def save_result(conn, user_id, quiz_id, score):
        """
        Save a quiz result.

        Args:
            conn: Database connection
            user_id: The user's ID
            quiz_id: The quiz ID
            score: The score achieved
        """
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO results (user_id, quiz_id, score)
            VALUES (?, ?, ?)
        """, (user_id, quiz_id, score))