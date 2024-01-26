import pandas as pd
import re

def extract_data(text):
    '''
    Extract person-argument variables through their syntactical features including "Interactional Role", "Gender", "Person", "Number",
    "Grammatical Function", and "Theta Role."
    '''

    pattern = r'\[(.*?)\]'
    data_in_brackets = re.findall(pattern, text)

    data_split = [item.split(',') for item in data_in_brackets]
    data_stripped = [[value.strip() for value in item] for item in data_split]

    column_names= ['Interactional Role', 'Gender', 'Person', 'Number', 'Grammatical Function', 'Theta Role']
    df = pd.DataFrame(data_stripped, columns=column_names)

    return df