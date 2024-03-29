import os


# Списки суфіксів для сортування

list_img = ['.jpg', '.jpeg', '.png', '.svg', '.bmp', '.svg', '.gif', '.webp',
            '.tiff', '.ico', '.psd', '.eps', '.pict', '.pcx', '.cdr', '.ai', '.raw']
list_archives = ['.zip', '.gz', '.tar', '.rar', '.7z', '.dmg', '.iso']
list_videos = ['.avi', '.flv', '.wmv', '.mov', '.mp4', '.webm', '.vob', '.mpg',
               '.mpeg', '.3gp', '.mkv', '.swf', '.ifo', '.rm', '.ra', '.ram', '.m2v', '.m2p']
list_documents = ['.log', '.txt', '.doc', '.docx', '.docm', '.pdf', '.md', '.epub', '.ods', '.dotx',
                  '.odt', '.xml', '.ppt', '.pptx', '.csv', '.xls', '.xlsx', '.wpd', '.rtf', '.rtfd', '.rvg', '.dox']
list_musics = ['.aac', '.m4a', '.mp3', '.ogg', '.wav', '.wma', '.amr', '.midi', '.flac', '.alac', '.aiff',
               '.mqa', '.dsd', '.asf', '.vqf', '.3ga']
list_programs = ['.html', '.htm', '.xhtml', '.exe', '.msi',
                 '.py', '.pyw', '.apk', '.npbk', '.torrent', '.fig']


def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


def get_file_size(file_name):
    f_size = os.path.getsize(file_name)
    return convert_bytes(f_size)


def get_file_category(file_name):
    ext = os.path.splitext(file_name)[1].lower()

    if ext in list_img:
        return 'Зображення'
    elif ext in list_archives:
        return 'Архів'
    elif ext in list_videos:
        return 'Відео'
    elif ext in list_documents:
        return 'Документ'
    elif ext in list_musics:
        return 'Аудіо'
    elif ext in list_programs:
        return 'Програма'
    else:
        return 'Інше'
