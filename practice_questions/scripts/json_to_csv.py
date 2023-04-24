import sys
import logging
import pathlib
import json

log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)

def check_path(path):

    # Check if path exists
    if not path.exists():
        log.error("Path '{}' doesn't exists.".format(path))
        sys.exit(1)

    # Check if path is a directory
    if not path.is_dir():
        log.error("Path '{}' isn't a directory.".format(path))
        sys.exit(1)

def get_questions(path):

    path = pathlib.Path(path)

    check_path(path)

    # Create data array
    questions = []

    for file in path.rglob("*"):

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

        # Add path to questions
        for question in data:
            question['path'] = str(file)

        questions.extend(data)

    return questions

def write_csv(
    questions, 
    path, 
    write_header=False):

    header = [ 'question', 'A', 'B', 'C', 'D', 'answer', 'comment', 'path', '\n' ]
    sep = '\t'

    with open(path, 'w') as f:

        if write_header:
            f.write(sep.join(header))

        for q in questions:
            record = []
            
            # print(pathlib.Path(q['path']).parts)

            f.write(sep.join([
                q['question'], 
                q['options']['A'], 
                q['options']['B'], 
                q['options']['C'] if 'C' in q['options'] else '', 
                q['options']['D'] if 'D' in q['options'] else '', 
                q['answer']['options'], 
                q['answer']['text'], 
                q['path'], 
                '\n' ]))

if __name__ == '__main__':

    questions = get_questions('../src/online/')
    
    log.info('{} questions processed'.format(len(questions)))

    output_path = pathlib.Path('../dist/')
    check_path(output_path)
    write_csv(questions, output_path / 'practice_questions.csv')
