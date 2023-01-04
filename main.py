import os
import ffmpeg

from pytube import Playlist, YouTube


# liens pour les tests
# playlist courte : https://www.youtube.com/playlist?list=PL6wtbJKOh3fGOVxYNrL7nRQT6wcaThm7m
# video avec pleins de résolutions : https://www.youtube.com/watch?v=ExKpWKSrOPE


# url_input = "https://www.youtube.com/watch?v=iiryoHtOe7g"
# url_input = "https://www.youtube.com/playlist?list=PL6wtbJKOh3fGOVxYNrL7nRQT6wcaThm7m"


selected_resolutions = []

def get_url_and_verify_integrity():
    while True:
        print("Copier-coller l'url de la video ou la playlist que vous souhaitez télécharger.")
        user_url = input("=> ")
        if user_url.startswith("https://www.youtube.com"):
            print("url ok")
            print("\n")
            break
        else:
            print("Erreur dans l'url")
            continue
    return user_url


def playlist_or_not_playlist(url):
    if "playlist" not in url:
        return True
    else:
        return False


def show_playlist(url):
    playlist_youtube_video = []
    if playlist_or_not_playlist(url) == True:
        youtube_video = YouTube(url)
        playlist_youtube_video.append(youtube_video)
    else:
        p = Playlist(url)
        for url in p.video_urls:
            youtube_video = YouTube(url)
            playlist_youtube_video.append(youtube_video) 
    

    for youtube_video in playlist_youtube_video:
        print(f"{youtube_video.title} - {str(youtube_video.length//60)}.{str(youtube_video.length%60)}")
    
    return playlist_youtube_video
  

def choice_audio_or_video():    
    print("\n")
    print("Tu veux télécharger le fichier vidéo ou seulement l'audio ?")
    print("1 - le (ou les) fichier(s) vidéo")
    print("2 - seulement le (ou les) fichier(s) audio")
    
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


def resolution_choice(choice_media_type, playlist, user_url_input):
    if choice_media_type == "1":
        quality = ("qualité optimale", "qualité moyenne", "qualité minimale")
        print(f"""
Choisissez la qualité des médias à télécharger :
1 - {quality[0]}
2 - {quality[1]}
3 - {quality[2]}
        """)
        user_quality_choice = input("=> ")
        print(f"Tu as choisi : {quality[int(user_quality_choice) - 1]}")
    elif choice_media_type == "2":
        download_audio(playlist, user_url_input)

# url_input = "https://www.youtube.com/watch?v=iiryoHtOe7g"
# url_input = "https://www.youtube.com/playlist?list=PL6wtbJKOh3fGOVxYNrL7nRQT6wcaThm7m"

# def show_video_choice(playlist, user_url_input):
#     all_resolutions = []
#     list_of_sorted_streams = []

#     for clip in playlist:
#         list_of_sorted_streams.append(clip.streams.filter(file_extension="mp4", type="video").order_by("resolution").desc())  
#     print(list_of_sorted_streams)

#     for sort_stream in list_of_sorted_streams:
#         for resolution in sort_stream:
#             all_resolutions.append(int(resolution.resolution[:-1]))

#     resolutions = list(set(all_resolutions))
#     resolutions.sort()

#     print("\n")
#     print("Voici les résolutions disponibles :")
#     for idx, resolution in enumerate(resolutions):
#         print(f"{idx + 1} - {resolution}p")
    
#     print("\n")
#     print("Dans quelle résolution souhaites-tu télécharger ta (tes) vidéos ?")
#     print(f"Tape ton choix entre 1 et {len(resolutions)}.")
#     user_resolution_choice = input("=> ")

#     print(f"Tu as choisi la résolution suivante : {resolutions[int(user_resolution_choice) - 1]}p.")
#     print("\n")
    
#     # download_video(playlist, user_url_input)

def download_video(playlist, user_url_input):
    print(playlist)

    # POUR PLAYLIST
    if "playlist" in user_url_input:
        print("je suis une playlist video")
        p = Playlist(user_url_input)
        for url in p.video_urls:
            youtube_video = YouTube(url)
            print(youtube_video)
            # stream = youtube_video.streams.get_by_itag(itag)
            print(f"Téléchargement...")
            # stream.download()
            print("OK")
    else:
        print("je suis une video unique") 
        # POUR VIDEO UNIQUE
        youtube_video = YouTube(user_url_input)

        # appel de la méthode "on_download_progress" qui permet l'affichage de la progression
        # youtube_video.register_on_progress_callback(on_download_progress)

        for i in range(len(selected_resolutions)):
            # si resolution <= 720p alors charge la video progressive
            if resolution <= 720:
                stream = youtube_video.streams.get_by_itag(itag)
                print(f"Téléchargement...")
                stream.download()
                print("OK")
                break
            else:
                stream_video = youtube_video.streams.get_by_itag(itag)

                streams = youtube_video.streams.filter(progressive=False, file_extension="mp4",
                                                        type="audio").order_by("abr").desc()
                best_audio_stream = streams[0]

                # TELECHARGEMENT
                print("Téléchargement video...")
                stream_video.download("video")
                print("OK")

                print("Téléchargement audio...")
                best_audio_stream.download("audio")
                print("ok")

                # COMBINAISON DES FICHIERS AUDIO ET VIDEO
                audio_filename = os.path.join("audio", best_audio_stream.default_filename)
                video_filename = os.path.join("video", stream_video.default_filename)
                output_filename = stream_video.default_filename

                print("Combinaison des fichiers...")
                ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename,
                                vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
                print("ok")

                # à la fin de l'opération de combinaison => suppr. des fichiers/dossiers temporaires audio/video
                os.remove(audio_filename)
                os.remove(video_filename)
                os.rmdir("audio")
                os.rmdir("video")

                break







def download_audio(playlist_to_download, user_url_input):
    all_audio_streams = []
    
    for clip in playlist_to_download:
        audio_stream = clip.streams.filter(progressive=False, file_extension="mp4", type="audio").order_by(
        "abr").desc()
        all_audio_streams.append(audio_stream)

    if playlist_or_not_playlist(user_url_input) == False:
        for stream in all_audio_streams:
            best_stream = stream[0]
            print("Téléchargement...")
            # TODO : je ne sais pas encore comment spécifier mon dossier de téléchargement
            # sans doute avec le module os
            # best_stream.download()
            print("OK")
    else:
        best_stream = all_audio_streams[0][0]
        print("Téléchargement...")
        # best_stream.download()
        print("OK")


def main():
    user_url_input = get_url_and_verify_integrity()
    playlist_or_not_playlist(user_url_input)
    playlist = show_playlist(user_url_input)
    choice_media_type = choice_audio_or_video()
    resolution_choice(choice_media_type, playlist, user_url_input)

main()



'''



# TO DO : affiche l'évolution du chargement dans des progress bar et labels
# note : marche pour l'instant uniquement dans le terminal
def on_download_progress(self, stream, chunk, bytes_remaining):
    # octets qu'on a déjà téléchargés
    bytes_downloaded = stream.filesize - bytes_remaining
    # pourcentage des octets déjà téléchargés
    percent = int(bytes_downloaded * 100 / stream.filesize)

    print(percent)
    print(f"Progression du téléchargement: {percent}% - {bytes_remaining}")

    # TO DO : afficher l'évolution de la progress bar de chargement et du label
    # ids.progress_stream_value.value = percent
    # ids.progress_stream_label.text = f"{str(percent)}%"

    # TO DO : si playlist alors afficher l'évolution de la progress bar (+label) du nbre de videos restant à charger



'''