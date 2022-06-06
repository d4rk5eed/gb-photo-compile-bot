import os
import logging
from constants import TPL_PATH, TPL_FILENAME

def create(file_list, user_id):
    logging.info(f"Creating markdown file_list{file_list}, user_id: {user_id}")
    user_id = str(user_id)
    tpl_contents = ''
    with open(os.path.join(TPL_PATH, TPL_FILENAME)) as f:
        tpl_contents = f.read()

    markdown_content = ''
    for filename in file_list:
        markdown_content += tpl_contents.replace('FILENAME', filename)
    
    md_filepath = os.path.join(user_id, 'output.md')
    f = open(md_filepath, 'w')
    f.write(markdown_content)
    f.close()

    return md_filepath