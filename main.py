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
    print("\n")
    
    user_choice = ""
    while True:
        user_choice = input("=> ")
        if user_choice == "1":
            print("Tu as choisi de télécharger le (ou les) vidéos")            
        elif user_choice == "2":
            print("Tu as choisi de télécharger le (ou les) audios")
        else:
            print("Tu dois entrer soit 1, soit 2.")
            continue
        return user_choice


def resolution_choice(user_res_choice, playlist, user_url_input):
    if user_res_choice == "1":
        # TODO : Je suis rendu à afficher les résolutions videos
        # show_video_choice()







        print("VIDEO")
    elif user_res_choice == "2":
        download_audio(playlist, user_url_input)


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
    user_res_choice = choice_audio_or_video()
    resolution_choice(user_res_choice, playlist, user_url_input)

main()

'''
def show_video_choice(url):
    youtube_video = YouTube(url)
    streams = youtube_video.streams.filter(file_extension="mp4", type="video").order_by(
            "resolution").desc()

    # dans une liste "all_resolutions", récupère pour chaque objet PyTube (résolution, is_progressive, itag
    all_resolutions = []
    for stream in streams:
        # dans PyTube, la résolution est un str => supprime le "p" et convertit en int
        stream_resolution = int(stream.resolution[:-1])
        all_resolutions.append((stream_resolution, stream.is_progressive, stream.itag))

    # dans une liste "selected_resolutions" => ajoute seulement résolutions voulues
    # si "<= 720p" alors ajoute les videos "progressives" plus rapides à charger (limité aux videos <= 720p)
    # si "> 720" alors ajoute les videos "adaptatives"
    # TO DO : il peut y avoir plusieurs fois la même résolution mais avec différents codecs...
    # ...supprimer les doublons ou les garder en affichant le codec à côté
    for i in range(len(all_resolutions)):
        if (all_resolutions[i][0] > 720) or (all_resolutions[i][0] <= 720 and all_resolutions[i][1]):
            selected_resolutions.append(all_resolutions[i])


def download_video(self, instance):
    # TO DO : amélioration du code pour ne pas toujours répéter cette url
    url = url_input.text

    itag = 0
    resolution = 0

    # sélectionne la résolution correspondant à index de la checkbox active
    for i in range(len(tab_ck)):
        if tab_ck[i].active:
            itag = selected_resolutions[i][2]
            resolution = selected_resolutions[i][0]

    # TO DO : Voir comment je gère la résolution de chaque vidéo dans une playlist
    # POUR PLAYLIST
    if "playlist" in url:
        print("je suis une playlist video")
        p = Playlist(url)
        for url in p.video_urls:
            youtube_video = YouTube(url)
            stream = youtube_video.streams.get_by_itag(itag)
            print(f"Téléchargement...")
            # stream.download()
            print("OK")
    else:
        # POUR VIDEO UNIQUE
        youtube_video = YouTube(url)

        # appel de la méthode "on_download_progress" qui permet l'affichage de la progression
        youtube_video.register_on_progress_callback(on_download_progress)

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