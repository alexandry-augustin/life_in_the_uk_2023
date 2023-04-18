import sys
import logging
import pathlib
import json

log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)

def get_questions(path):

    data_dir = pathlib.Path(path)

    # Check if path exists
    if not data_dir.exists():
        log.error("Path doesn't exists.")
        sys.exit(1)

    if not data_dir.is_dir():
        log.error("Path isn't a directory.")
        sys.exit(1)

    # Create data array
    questions = []

    for file in data_dir.rglob("*"):

        # Check whether file is a directory
        if file.is_dir():
            # Move on to next file
            continue

        if file.suffix != '.json':
            # Move on to next file
            continue

        # Load data from file
        with open(file) as f:
            data = json.load(f)

        questions.extend(data)

    return questions

def write_csv(questions, path):

    header = [ 'question', 'A', 'B', 'C', 'D', 'answer', 'comment', '\n' ]
    sep = '\t'

    with open(path, 'w') as f:

        f.write(sep.join(header))

        for q in questions:
            record = []

            f.write(sep.join([
                q['question'], 
                q['options']['A'], 
                q['options']['B'], 
                q['options']['C'] if 'C' in q['options'] else '', 
                q['options']['D'] if 'D' in q['options'] else '', 
                q['answer']['options'], 
                q['answer']['text'], 
                '\n' ]))

if __name__ == '__main__':

    questions = get_questions('../src/online/')
    write_csv(questions, '../dist/practice_questions.csv')

    log.info('{} questions processed'.format(len(questions)))