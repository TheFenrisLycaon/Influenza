import toml

from api import api

SECRETS = toml.load("./secrets.toml")

def get_content_type():
    """
    Returns the type of video
    """
    ...


def get_content_text():
    """
    Returns the text to be put onto a video
    """
    ...

def download_all_videos():
    ...


def get_videos():
    """
    Makes request to Pexels
    Parses the videos
    Parses the hightest quality of a random video
    Downloads the video
    """
    p = api.PEXELS(API_KEY=SECRETS.get("API_KEYS", {}).get("pexels", ""))

    p.search_video("drone nature")
    print("Total results: ", p.total_results)
    
    k = p.get_video_entries()

    k = k if k else []

    for video in k:
        print(video.link)
    
    download_all_videos()
    


def main():
    get_content_type()
    get_content_text()
    get_videos()

    

if __name__ == "__main__":
    main()