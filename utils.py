

import os
import requests
import time
import zipfile


def send_to_dogbin(text):
    if not isinstance(text, bytes):
        text = text.encode()
    post = requests.post("https://del.dog/documents", data=text)
    try:
        return "https://del.dog/" + post.json()["key"]
    except JSONDecodeError:
        return html.escape(post.text)


def pretty_size(size):
    units = ['B', 'KB', 'MB', 'GB']
    unit = 0
    while size >= 1024:
        size /= 1024
        unit += 1
    return '%0.2f %s' % (size, units[unit])


def get_flag(code):
    offset = 127462 - ord('A')
    return chr(ord(code[0]) + offset) + chr(ord(code[1]) + offset)


def escape_markdown(text):
    text = text.replace('[', '\[')
    text = text.replace('_', '\_')
    text = text.replace('*', '\*')
    text = text.replace('`', '\`')

    return text

def backup_sources(output_file=None):
    ctime = int(time.time())

    if isinstance(output_file, str) and not output_file.lower().endswith('.zip'):
        output_file += '.zip'

    fname = output_file or 'backup-{}.zip'.format(ctime)

    with zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED) as backup:
        for folder, _, files in os.walk('.'):
            for file in files:
                if file != fname and not file.endswith('.pyc') and '.heroku' not in folder.split('/'):
                    backup.write(os.path.join(folder, file))

    return fname
