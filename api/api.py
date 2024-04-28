# main_script.py
import requests
import toml

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

        self.load_config()

    def load_config(self):
        config_data = toml.load("config.toml")
        
        self._base_url = config_data["PexelsConfig"]["BASE_URL"]
        self._photo_base_url = config_data["PexelsConfig"]["PHOTO_BASE_URL"]
        self._video_base_url = config_data["PexelsConfig"]["VIDEO_BASE_URL"]
        self._search_url = config_data["PexelsConfig"]["SEARCH_URL"]
        self._popular_url = config_data["PexelsConfig"]["POPULAR_URL"]
        self._curated_url = config_data["PexelsConfig"]["CURATED_URL"]

        self.results_per_page = config_data["PexelsConfig"]["RESULTS_PER_PAGE"]
        self.default_page = config_data["PexelsConfig"]["DEFAULT_PAGE"]

    def search_photo(self, query, results_per_page=None, page=None):
        results_per_page = results_per_page or self.results_per_page
        page = page or self.default_page
        query = query.replace(" ", "+")
        url = f"{self._base_url}{self._photo_base_url}/{self._search_url}?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def search_video(self, query, results_per_page=None, page=None):
        results_per_page = results_per_page or self.results_per_page
        page = page or self.default_page
        query = query.replace(" ", "+")
        url = f"{self._base_url}{self._video_base_url}/{self._search_url}?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def popular_photo(self, results_per_page=None, page=None):
        results_per_page = results_per_page or self.results_per_page
        page = page or self.default_page
        url = f"{self._base_url}{self._photo_base_url}/{self._popular_url}?per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def curated_photo(self, results_per_page=None, page=None):
        results_per_page = results_per_page or self.results_per_page
        page = page or self.default_page
        url = f"{self._base_url}{self._photo_base_url}/{self._curated_url}?per_page={results_per_page}&page={page}"
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
