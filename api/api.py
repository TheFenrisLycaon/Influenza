import requests

from api.classes.content import Photo, Video


class PEXELS:
    def __init__(self, API_KEY):
        self.PEXELS_AUTHORIZATION = {"Authorization": API_KEY}
        self.request = None
        self.json = None
        self.page = None
        self.total_results = None
        self.page_results = None
        self.has_next_page = None
        self.has_previous_page = None
        self.next_page = None
        self.prev_page = None

    def search_photo(self, query, results_per_page=15, page=1):
        query = query.replace(" ", "+")
        url = f"https://api.pexels.com/v1/search?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def search_video(self, query, results_per_page=15, page=1):
        query = query.replace(" ", "+")
        url = f"https://api.pexels.com/videos/search?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def popular_photo(self, results_per_page=15, page=1):
        url = "https://api.pexels.com/v1/popular?per_page={}&page={}".format(
            results_per_page, page
        )
        self.__request(url)
        return None if not self.request else self.json

    def curated_photo(self, results_per_page=15, page=1):
        url = "https://api.pexels.com/v1/curated?per_page={}&page={}".format(
            results_per_page, page
        )
        self.__request(url)
        return None if not self.request else self.json

    def search_next_page(self):
        if self.has_next_page:
            self.__request(self.next_page)
        else:
            return None
        return None if not self.request else self.json

    def search_previous_page(self):
        if self.has_previous_page:
            self.__request(self.prev_page)
        else:
            return None
        return None if not self.request else self.json

    def get_photo_entries(self):
        if not self.json:
            return None
        return [Photo(json_photo) for json_photo in self.json["photos"]]

    def get_video_entries(self):
        if not self.json:
            return None
        return [Video(json_video) for json_video in self.json["videos"]]

    def __request(self, url):
        try:
            self.request = requests.get(
                url, timeout=15, headers=self.PEXELS_AUTHORIZATION
            )
            self.__update_page_properties()
        except requests.exceptions.RequestException:
            print("Request failed check your internet connection")
            self.request = None
            exit()

    def __update_page_properties(self):
        if self.request.ok:  # type: ignore
            self.json = self.request.json()  # type: ignore
            try:
                self.page = int(self.json["page"])
            except Exception:
                self.page = None
            try:
                self.total_results = int(self.json["total_results"])
            except Exception:
                self.total_results = None
            try:
                self.page_results = len(self.json["photos"])
            except Exception:
                self.page_results = None
            try:
                self.next_page = self.json["next_page"]
                self.has_next_page = True
            except Exception:
                self.next_page = None
                self.has_next_page = False
            try:
                self.prev_page = self.json["prev_page"]
                self.has_previous_page = True
            except Exception:
                self.prev_page = None
                self.has_previous_page = False
        else:
            print("Wrong response. You might have a wrong API key")
            print(self.request)
            print("API key: {}".format(self.PEXELS_AUTHORIZATION))
            self.request = None
            exit()
