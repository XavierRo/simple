"""
Ma demande à chatGPT :
J'aimerais lister les fichiers d'un répertoire et en fonction de leur extension les déplacer dans un autre répertoire. Voici les répertoires de destinations :
dest_folder_type = ['AUTRES','DOC','IMG','MSG','PDF','PPT','SCRIPTS','TAB','TXT','VIDEO','ZIP']
Que me proposes tu ?
 J'aimerais améliorer le déplacement. Si dans le répertoire de destination un fichier avec le même nom existe et si ils ont la même taille il faut écraser le fichier le plus ancien.
 Si les tailles sont différentes il faut incrémenter un numéro de version dans le nom du fichier (avant l'extension).
=> TODO vérifier les histoires de date dans le cas où c'est la même taille
Remarque 11/12/2023 :
VIDEO contient également des MP3...je devrais appeler ça AUDIO_VIDEO ?.
TXT contient beaucoup de choses....

TODO Remplacer l'action de déplacement par une action générique

"""
import os
import shutil

# Répertoire source
source_folder_root = 'd:/Backup/2022/'
root_dest_folder = 'd:/Backup/CIRAD/'

# Répertoires de destination
dest_folder_types = ['AUTRES','EXE', 'DOC', 'IMG', 'EPUB','MSG', 'PDF', 'PPT', 'SCRIPTS', 'TAB', 'TXT', 'VIDEO', 'ZIP']

# Créer les répertoires de destination s'ils n'existent pas
for folder_type in dest_folder_types:
    dest_folder = os.path.join(root_dest_folder, folder_type)
    os.makedirs(dest_folder, exist_ok=True)

# Liste des extensions et leurs répertoires de destination
extensions_mapping = {
    'pdf': 'PDF',
    'eml' : 'MSG','msg' : 'MSG',
    'epub' : 'EPUB',
    'exe' : 'EXE', 'msi' : 'EXE', 'jar' : 'EXE',
    'doc': 'DOC', 'docx': 'DOC','docm': 'DOC','dotx': 'DOC','odt': 'DOC',
    'jpg': 'IMG', 'png': 'IMG','jpeg' : 'IMG','jfif' : 'IMG', 'svg' : 'IMG','gif' : 'IMG',
    'ppt' : 'PPT', 'pptx' : 'PPT', 'pptm' : 'PPT',
    'sh' : 'SCRIPTS', 'cmd' : 'SCRIPTS', 'js' : 'SCRIPTS', 'py' : 'SCRIPTS','r' : 'SCRIPTS','sql' : 'SCRIPTS',
    'java' : 'SCRIPTS',
    'txt': 'TXT', 'htm': 'TXT','html': 'TXT','xml': 'TXT','css': 'TXT','bibtex': 'TXT','log': 'TXT','ics':'TXT',
    'yml':'TXT', 'conf' : 'TXT','json':'TXT','cer' : 'TXT','md':'TXT','kml':'TXT','properties':'TXT', 'pgn' : 'TXT',
    'xls' : 'TAB', 'xlsx' : 'TAB', 'csv' : 'TAB','tsv' : 'TAB','xlsm' : 'TAB','tab' : 'TAB','ods' : 'TAB',
    'mp4' : 'VIDEO','mp3' : 'VIDEO',
    'zip' : 'ZIP','7z' : 'ZIP','gz' : 'ZIP','rar' : 'ZIP','zipx' : 'ZIP','tar' : 'ZIP','tgz' : 'ZIP'
    # Ajoutez d'autres extensions au besoin
}

def move_file(source_filepath, dest_folder, dest_filename):
    dest_filepath = os.path.join(dest_folder, dest_filename)

    # Si le fichier de destination existe
    if os.path.exists(dest_filepath):
        # Si les tailles des fichiers sont identiques
        if os.path.getsize(source_filepath) == os.path.getsize(dest_filepath):
            # Si le fichier source est plus récent, écrasez le fichier de destination
            if os.path.getmtime(source_filepath) > os.path.getmtime(dest_filepath):
                shutil.move(source_filepath, dest_filepath)
                print(f"Le fichier {dest_filename} a été écrasé.")
            else:
                print(f"Le fichier {dest_filename} existe déjà et est plus récent, rien n'a été fait.")
        else:
            # Les tailles des fichiers sont différentes, ajoutez un numéro de version
            base_name, extension = os.path.splitext(dest_filename)
            version_number = 1
            while os.path.exists(os.path.join(dest_folder, f"{base_name}_{version_number}{extension}")):
                version_number += 1

            dest_filename = f"{base_name}_{version_number}{extension}"
            dest_filepath = os.path.join(dest_folder, dest_filename)
            shutil.move(source_filepath, dest_filepath)
            print(f"Le fichier {dest_filename} a été déplacé avec un numéro de version.")
    else:
        # Le fichier de destination n'existe pas, déplacez simplement le fichier source
        shutil.move(source_filepath, dest_filepath)
        print(f"Le fichier {dest_filename} a été déplacé.")

def process_files(source_folder, dest_base_folder, extensions_mapping):
    # Liste des fichiers dans le répertoire source
    for filename in os.listdir(source_folder):
        source_filepath = os.path.join(source_folder, filename)

        # Si c'est un répertoire, traitez les fichiers à l'intérieur récursivement
        if os.path.isdir(source_filepath):
            process_files(source_filepath, dest_base_folder, extensions_mapping)
        else:
            # Obtenez l'extension du fichier
            _, file_extension = os.path.splitext(filename)
            file_extension = file_extension[1:].lower()  # Supprimez le point et mettez en minuscules

            # Trouver le répertoire de destination en fonction de l'extension
            dest_folder_type = extensions_mapping.get(file_extension, 'AUTRES')

            # Déterminez le nom du fichier dans le répertoire de destination
            dest_filename = filename

            move_file(source_filepath, os.path.join(dest_base_folder, dest_folder_type), dest_filename)

process_files(source_folder_root, root_dest_folder, extensions_mapping)

print("Terminé.")
