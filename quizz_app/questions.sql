delete from sqlite_sequence where name='quizzes';
delete from sqlite_sequence where name='questions';

-- First insert the quiz
INSERT INTO quizzes (id, title, description, time_limit)
VALUES (
    1,
    'Python Basics Quiz',
    'Test your knowledge of Python fundamentals',
    15  -- 15 minutes time limit
);

-- Then insert questions for this quiz
-- We'll use last_insert_rowid() to get the quiz_id we just created
INSERT INTO questions (quiz_id, question_text, correct_answer, option_a, option_b, option_c, option_d)
VALUES
(1,
'What is the output of print(type([]))?',
'<class ''list''>',
'<class ''list''>',
'<class ''array''>',
'<class ''tuple''>',
'<class ''set''>'
),
(1,
'Which of these is not a Python built-in data type?',
'array',
'list',
'tuple',
'dict',
'array'
),
(1,
'What does the len() function return for a string "Python"?',
'6',
'5',
'6',
'7',
'4'
);

-- Quiz Test
INSERT INTO quizzes (id, title, description, time_limit)
VALUES (
    2,
    'Test1',
    'Test',
    15  -- 15 minutes time limit
);

-- Then insert questions for this quiz
-- We'll use last_insert_rowid() to get the quiz_id we just created
INSERT INTO questions (quiz_id, question_text, correct_answer, option_a, option_b, option_c, option_d)
VALUES
(2,
'Correct Answer is 1',
'1',
'1',
'2',
'3',
'4'
),
(2,
'Correct Answer is 2',
'2',
'1',
'2',
'3',
'4'
),
(2,
'Correct Answer is 3',
'3',
'1',
'2',
'3',
'4'
);