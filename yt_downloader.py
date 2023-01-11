import os
import ffmpeg
import shutil
import tkinter
import tkinter.filedialog
from pathlib import Path
from pytube import Playlist, YouTube


# liens pour les tests
# playlist courte : https://www.youtube.com/playlist?list=PL6wtbJKOh3fGOVxYNrL7nRQT6wcaThm7m
# video 4k = https://www.youtube.com/watch?v=LXb3EKWsInQ&t=1s
# video 1080 = https://www.youtube.com/watch?v=6kqivnW1OBM


def introduction():
    print("""
                #########################################
                #                                       #
                #   Bienvenue dans YOUTUBE DOWNLOADER   #
                #                  par                  # 
                #               Petchorine              #
                #                                       #
                #########################################
    """)

def get_url_and_verify_integrity():
    """
    - demande l'url du clip à télécharger à l'utilisateur
    - vérifie que l'url commence bien avec "https://www.youtube.com"
        - si ok => retourne user_url
        - sinon redemande une url correcte

    Paramètres:
    ==========


    Retourne:
    =========
        user_url (str) : url du clip à télécharger
    """
    while True:
        print("\n")
        print("Copier-coller l'url de la video ou la playlist que vous souhaitez télécharger.")
        user_url = input("=> ")
        if user_url.startswith("https://www.youtube.com"):
            print("L'url est valide. Nous allons pouvoir commencer le téléchargement.")
            print("\n")
            print("Voici les clips associés à cette url :")
            print("\n")
            break
        else:
            print("Il semble qu'il y ait une erreur dans l'url. Essaye de copier à nouveau.")
            continue
    return user_url


def is_not_playlist(url):
    """
        vérifie si l'élément associé à l'url est une playlist ou un clip unique

    Paramètres:
    ==========
        url (str) : url du clip à télécharger

    Retourne:
    =========
        bool
    """
    if "playlist" not in url:
        return True
    else:
        return False


def show_playlist(url):
    """
    - que l'url corresponde à une playlit ou non...
      ...constitue une liste de toutes les videos (objets PyTube) associés à l'url
    - affiche le titre et la durée pour chaque vidéo

    Paramètres:
    ==========
        url (str) : url du clip à télécharger

    Retourne:
    =========
        liste d'objets Pytube
    """
    playlist_youtube_video = []
    if is_not_playlist(url) == True:
        youtube_video = YouTube(url)
        playlist_youtube_video.append(youtube_video)
    else:
        p = Playlist(url)
        for url in p.video_urls:
            youtube_video = YouTube(url)
            playlist_youtube_video.append(youtube_video) 
    
    print("Titre(s)" + (45 * ' ') + "Durée")
    print((50 * '=') + '   ' + (5 * '='))
    for youtube_video in playlist_youtube_video:
        if len(youtube_video.title) > 50:
            print(f"{youtube_video.title[:45]}...     {str(youtube_video.length//60)}.{str(youtube_video.length%60)}")
        else:
            print(youtube_video.title + ((53 - len(youtube_video.title)) * ' ') + str(youtube_video.length//60) + '.' +str(youtube_video.length%60))
    
    return playlist_youtube_video
  

def choice_audio_or_video():
    """
        demande à l'utilisateur le type de média à télécharger : 
            - video + audio
            - seulement audio

    Paramètres:
    ==========


    Retourne:
    =========
        user_choice (str) : soit "1", soit "2"
    """    
    print("\n")
    print("Tu veux télécharger le(s) clip(s) audio/vidéo ou seulement l'audio ?")
    print("   1 - le(s) clip(s) audio/vidéo")
    print("   2 - seulement l'audio")
    
    user_choice = ""
    while True:
        user_choice = input("=> ")
        if user_choice == "1":
            print("Tu as choisi de télécharger le (ou les) vidéos.")            
        elif user_choice == "2":
            print("Tu as choisi de télécharger le (ou les) audios.")
        else:
            print("Tu dois entrer soit 1, soit 2.")
            continue
        return user_choice


def resolution_choice(choice_media_type, playlist):
    """
    Si choix utilisateur == "1" (video + audio)
        demande à l'utilisateur la qualité à télécharger :
            - optimale => meilleure qualité si progressive = False
            - moyenne => meilleure qualité si progressive = True
            - minimale => plus basse qualité si progressive = True
        appelle la fonction permettant d'isoler les streams dans la qualité choisie
    Si choix utilisateur == "2" (seulement audio)
        - appelle la fonction qui pemet à l'utilisateur de choisir le dossier de téléchargement
        - appelle la fonction pour télécharger l'audio dans la meilleure qualité disponible

    Paramètres:
    ==========
        choice_media_type (str) : choix de l'utilisateur sur le type de média ("1" ou "2")
        playlist (list) : liste des objets PyTube associés à l'url

    Retourne:
    =========

    """ 
    if choice_media_type == "1":
        quality = ("qualité optimale", "qualité moyenne", "qualité minimale")
        print("\n")
        print(f"Choisis la qualité des médias à télécharger :")
        print(f"   1 - {quality[0]}")
        print(f"   2 - {quality[1]}")
        print(f"   3 - {quality[2]}")
        while True:
            user_quality_choice = input("=> ")
            if user_quality_choice == "1" or user_quality_choice == "2" or user_quality_choice == "3":
                print(f"Tu as choisi : {quality[int(user_quality_choice) - 1]}")
                print("\n")
                break
            else:
                print("Tu dois entrer 1, 2 ou 3.")
                continue
        get_resolutions_list(playlist, int(user_quality_choice))
    elif choice_media_type == "2":
        user_directory_choice = directory_choice()
        download_audio(playlist, user_directory_choice)

def directory_choice():
    """
    permet de récupérer l'adresse du dossier de téléchargement choisi par l'utilisateur
    si l'utilisateur ne choisit pas de dossier (clic sur fermeture de la fenêtre ou Annuler) 
        - dossier par défaut est le dossier où se trouve le script

    Paramètres:
    ==========
        
    Retourne:
    =========
    user_directory_choice (str) : adresse du dossier de téléchargement choisi par l'utilisateur
    """ 
    # on initialise tkinter en appelant la fonction Tk()
    racine_tk = tkinter.Tk()
    # permet de masquer la petite fenêtre supplémentaire (je ne sais pas à quoi elle sert ???)
    racine_tk.withdraw()

    print("Dans quel dossier souhaites-tu télécharger tes clips ?")
    print("Note : si tu ne vois pas la fenêtre de choix, elle peut être cachée derrière la fenêtre du script !")
    directory_name = tkinter.filedialog.askdirectory(title='Choisir un dossier')
    
    
    if len(directory_name) != 0:
        user_directory_choice = Path(directory_name)
    else:
        script_directory = os.path.realpath(__file__)
        user_directory_choice = os.path.dirname(script_directory)    
    print("Chemin complet du dossier : ", user_directory_choice)

    return user_directory_choice

def get_resolutions_list(playlist, user_quality_choice):
    """
    En fonction du choix de qualité par l'utilisateur :
        - pour la qualité optimale ("1") :
            - crée une liste triée (décroissant) de tous les clips :
                - suivant resolution pour la video + progressive = False
                - suivant abr pour l'audio 
            - crée une liste des vidéos avec seulement meilleure qualité et progressive = False)
            - crée une liste des audio avec seulement meilleure qualité disponible
            - appelle la fonction de téléchargement avec en paramètres, les listes constituées
        - pour la qualité moyenne ("2") et minimale ("3") :
            - crée une liste triée (décroissant) de tous les clips
                - suivant resolution pour la video + progressive = True
            - appelle la fonction de téléchargement avec en paramètre, la liste constituée

    Paramètres:
    ==========
    playlist (list) : liste des objets PyTube associés à l'url
    user_quality_choice (int) : choix de la qualité (1, 2 ou 3) par l'utilisateur
        
    Retourne:
    =========
    - pour la qualité optimale ("1") :
        - best_video_resolutions_list (list) : liste des streams video dans la meilleure qualité
        - best_audio_resolutions_list (list) : liste des streams audio dans la meilleure qualité
        - user_directory_choice (str) : adresse du dossier de téléchargement choisie par l'utilisateur
    - pour la qualité moyenne ("2") et minimale ("3") :
        - resolutions_list (list) : liste des streams dans la qualité demandée
        - user_directory_choice (str) : adresse du dossier de téléchargement choisie par l'utilisateur
    
    """ 
    user_directory_choice = directory_choice()
    if user_quality_choice == 1:
        video_stream_list = []
        audio_stream_list = []
        
        for clip in playlist:
            video_stream_list.append(clip.streams.filter(progressive=False, file_extension="mp4", type="video").order_by("resolution").desc())
            audio_stream_list.append(clip.streams.filter(progressive=False, file_extension="mp4", type="audio").order_by("abr").desc())
        
        best_audio_resolutions_list = []
        for idx in range(len(audio_stream_list)):
            best_audio_stream = audio_stream_list[idx][0]
            best_audio_resolutions_list.append(best_audio_stream)      
        
        best_video_resolutions_list = []
        for idx in range(len(video_stream_list)):
            best_video_stream = video_stream_list[idx][0]
            best_video_resolutions_list.append(best_video_stream)
        
        download_video(best_video_resolutions_list, user_directory_choice, list_audio=best_audio_resolutions_list) 
    else:
        video_stream_list = []
        resolutions_list = []        
        for clip in playlist:
            video_stream_list.append(clip.streams.filter(progressive=True, file_extension="mp4", type="video").order_by("resolution").desc())  
        if user_quality_choice == 2:                   
            for idx in range(len(video_stream_list)):
                medium_video_stream = video_stream_list[idx][0]
                resolutions_list.append(medium_video_stream)
        
        elif user_quality_choice == 3:
            for idx in range(len(video_stream_list)):
                lowest_video_stream = video_stream_list[idx][-1]
                resolutions_list.append(lowest_video_stream)
        download_video(resolutions_list, user_directory_choice)


def download_video(resolutions_list, user_directory_choice, list_audio=None):
    """
        En fonction du choix de qualité par l'utilisateur :
        - pour la qualité optimale ("1") :
            - crée 2 dossiers temporaires de téléchargement (audio et video) 
            - télécharge les audios et les videos
            - combine les fichiers dans la meilleure qualité disponible dans le dossier choisi
            - efface les dossiers temporaires et leur contenu
        - pour la qualité moyenne ("2") et minimale ("3") :
            - télécharge les audios et les videos dans le dossier choisi
   
    
    Paramètres:
    ==========
    - resolutions_list (list) : liste des streams video dans la resolution demandée
    - user_directory_choice (str) : adresse du dossier de téléchargement choisie par l'utilisateur
    - list_audio=None (list) : liste des streams audio dans la resolution demandée (optionnel si progressive = True)
        
    Retourne:
    =========
    
    """
    
    # TELECHARGEMENT AUDIO
    audio_temp_directory = fr"{user_directory_choice}\audio_ytdown"
    if list_audio is not None:
        for best_audio in list_audio:
            print("Téléchargement audio...")
            best_audio.download(audio_temp_directory)
            print("ok")

    video_temp_directory = fr"{user_directory_choice}\video_ytdown"  
    for stream_video in resolutions_list:
        if stream_video.is_progressive == False:     
            # TELECHARGEMENT VIDEO
            print("Téléchargement video...")            
            stream_video.download(video_temp_directory)
            print("ok")

            # COMBINAISON DES FICHIERS AUDIO ET VIDEO
            audio_filename = os.path.join(user_directory_choice, "audio_ytdown", best_audio.default_filename)
            video_filename = os.path.join(user_directory_choice, "video_ytdown", stream_video.default_filename)
            output_filename = os.path.join(user_directory_choice, stream_video.default_filename)

            print("Combinaison des fichiers...")
            ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename,
                            vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
            print("ok")
        else:
            print(f"Téléchargement...")
            stream_video.download(user_directory_choice)
            print("OK")
    
    # à la fin de l'opération de combinaison => suppr. des fichiers/dossiers temporaires audio/video
    # si les dossiers ont été crées (dans le cas qualité optimale seulement) / pas d'erreur si autre qualité choisie 
    if os.path.isdir(audio_temp_directory):
        shutil.rmtree(audio_temp_directory)
    if os.path.isdir(video_temp_directory):
        shutil.rmtree(video_temp_directory)


def download_audio(playlist_audio_to_download, user_directory_choice):
    """
    crée une liste avec les audios triés en fonction de la qualité (abr) descendante 
    télécharge les meilleures audios dans le dossier spécifié par l'utilisateur
    
    Paramètres:
    ==========
    playlist_audio_to_download (list) :
    user_directory_choice (str) :
        
    Retourne:
    =========
    
    """
    all_audio_streams = []
    print("\n")
    for clip in playlist_audio_to_download:
        audio_stream = clip.streams.filter(progressive=False, file_extension="mp4", type="audio").order_by(
        "abr").desc()
        all_audio_streams.append(audio_stream)

    for stream in all_audio_streams:
        best_stream = stream[0]
        print("Téléchargement...")
        best_stream.download(output_path = user_directory_choice)
        print("OK")


def ending():
    """
    permet de relancer un téléchargement à la suite de celui qui vient de se terminer (choix 1)
    ou
    de quitter le programme (choix 2)
    
    Paramètres:
    ==========
        
    Retourne:
    =========
    
    """
    print("\n")
    print(f"Tous les clips ont bien été téléchargés...")
    print("\n")
    print("Veux-tu télécharger autre chose ?")
    print("   1 - oui")
    print("   2 - non, je souhaite quitter le programme.")
    while True:
        user_reload_choice = input("=> ")
        if user_reload_choice == "1":
            main()
        elif user_reload_choice == "2":
            quit()
        else:
            print("Tu dois choisir soit 1, soit 2.")
            continue

    
def main():
    """
    fonction principale permettant de lancer le script
    
    Paramètres:
    ==========
        
    Retourne:
    =========
    
    """
    user_url_input = get_url_and_verify_integrity()
    is_not_playlist(user_url_input)
    playlist = show_playlist(user_url_input)
    choice_media_type = choice_audio_or_video()
    resolution_choice(choice_media_type, playlist)
    ending()

introduction()
main()







