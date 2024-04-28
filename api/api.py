import requests
import toml

from api.classes.content import Photo, Video


class PexelsConfigLoader:
    def __init__(self, config_file="config.toml"):
        self.config_file = config_file

    def load_config(self):
        config_data = toml.load(self.config_file)
        return config_data["PexelsConfig"]


class PexelsAPI:
    def __init__(self, api_key, config):
        self.api_key = api_key
        self.config = config
        self.request = None
        self.json = None
        self.total_results = None
        self.page_results = None
        self.has_next_page = None
        self.has_previous_page = None
        self.next_page = None
        self.prev_page = None

    def search_photo(self, query, results_per_page=None, page=None):
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        query = query.replace(" ", "+")
        url = f"{self.config['BASE_URL']}{self.config['PHOTO_BASE_URL']}/{self.config['SEARCH_URL']}?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def search_video(self, query, results_per_page=None, page=None):
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        query = query.replace(" ", "+")
        url = f"{self.config['BASE_URL']}{self.config['VIDEO_BASE_URL']}/{self.config['SEARCH_URL']}?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def popular_photo(self, results_per_page=None, page=None):
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        url = f"{self.config['BASE_URL']}{self.config['PHOTO_BASE_URL']}/{self.config['POPULAR_URL']}?per_page={results_per_page}&page={page}"
        self.__request(url)
        return None if not self.request else self.json

    def curated_photo(self, results_per_page=None, page=None):
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        url = f"{self.config['BASE_URL']}{self.config['PHOTO_BASE_URL']}/{self.config['CURATED_URL']}?per_page={results_per_page}&page={page}"
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
                url, timeout=15, headers={"Authorization": self.api_key}
            )
            self.__update_page_properties()
        except requests.exceptions.RequestException:
            print("Request failed. Check your internet connection or API key.")
            self.request = None

    def __update_page_properties(self):
        if self.request.ok:
            self.json = self.request.json()
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
            print("Wrong response. You might have a wrong API key.")
            self.request = None
