def find_file_name(text):
    '''
    This script finds the file name of a stringself.

    input:
        text, a string.
    output:
        file_name, a string.
    '''

    file_name = str()

    for i in text:
        if i != '.':
            file_name += i
        else:
            break

    return(file_name)
