from typing import Any, Dict, List, Optional

import requests
import toml

from api.classes.content import Photo, Video


class PexelsConfigLoader:
    def __init__(self, config_file: str = "config.toml") -> None:
        self.config_file: str = config_file

    def load_config(self) -> Dict[str, Any]:
        config_data: Dict[str, Any] = toml.load(self.config_file)
        return config_data["PexelsConfig"]


class PexelsAPI:
    def __init__(self, api_key: str, config: Dict[str, Any]) -> None:
        self.api_key: str = api_key
        self.config: Dict[str, Any] = config
        self.request: Optional[requests.Response] = None
        self.json: Optional[Dict[str, Any]] = None
        self.total_results: Optional[int] = None
        self.page_results: Optional[int] = None
        self.has_next_page: Optional[bool] = None
        self.has_previous_page: Optional[bool] = None
        self.next_page: Optional[str] = None
        self.prev_page: Optional[str] = None

    def search_photo(
        self,
        query: str,
        results_per_page: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        query = query.replace(" ", "+")
        url = f"{self.config['BASE_URL']}{self.config['PHOTO_BASE_URL']}/{self.config['SEARCH_URL']}?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return self.json

    def search_video(
        self,
        query: str,
        results_per_page: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        query = query.replace(" ", "+")
        url = f"{self.config['BASE_URL']}{self.config['VIDEO_BASE_URL']}/{self.config['SEARCH_URL']}?query={query}&per_page={results_per_page}&page={page}"
        self.__request(url)
        return self.json

    def popular_photo(
        self, results_per_page: Optional[int] = None, page: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        url = f"{self.config['BASE_URL']}{self.config['PHOTO_BASE_URL']}/{self.config['POPULAR_URL']}?per_page={results_per_page}&page={page}"
        self.__request(url)
        return self.json

    def curated_photo(
        self, results_per_page: Optional[int] = None, page: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        results_per_page = results_per_page or self.config["RESULTS_PER_PAGE"]
        page = page or self.config["DEFAULT_PAGE"]
        url = f"{self.config['BASE_URL']}{self.config['PHOTO_BASE_URL']}/{self.config['CURATED_URL']}?per_page={results_per_page}&page={page}"
        self.__request(url)
        return self.json

    def search_next_page(self) -> Optional[Dict[str, Any]]:
        if self.has_next_page:
            if self.next_page is not None:
                self.__request(self.next_page)
        else:
            return None
        return self.json

    def search_previous_page(self) -> Optional[Dict[str, Any]]:
        if self.has_previous_page:
            if self.prev_page is not None:
                self.__request(self.prev_page)
        else:
            return None
        return self.json

    def get_photo_entries(self) -> Optional[List[Photo]]:
        if not self.json:
            return None
        return [Photo(json_photo) for json_photo in self.json["photos"]]

    def get_video_entries(self) -> Optional[List[Video]]:
        if not self.json:
            return None
        return [Video(json_video) for json_video in self.json["videos"]]

    def __request(self, url: Optional[str]) -> None:
        if url is not None:
            try:
                self.request = requests.get(
                    url, timeout=15, headers={"Authorization": self.api_key}
                )
                self.__update_page_properties()
            except requests.exceptions.RequestException:
                print("Request failed. Check your internet connection or API key.")
                self.request = None

    def __update_page_properties(self) -> None:
        if self.request is not None and self.request.ok:
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
