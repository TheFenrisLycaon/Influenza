class Photo:
    def __init__(self, json_photo):
        self.__photo = json_photo

    @property
    def id(self):
        return int(self.__photo["id"])

    @property
    def width(self):
        return int(self.__photo["width"])

    @property
    def height(self):
        return int(self.__photo["height"])

    @property
    def photographer(self):
        return self.__photo["photographer"]

    @property
    def url(self):
        return self.__photo["url"]

    @property
    def description(self):
        if self.__photo["alt"]:
            return self.__photo["alt"].lower()
        else:
            photo_description_text_in_list_form = self.url.split("/")[-2].replace(
                "-{}".format(self.id), ""
            )
            return "".join(photo_description_text_in_list_form).replace("-", " ")

    @property
    def color(self):
        return self.__photo["avg_color"]

    @property
    def original(self):
        return self.__photo["src"]["original"]

    @property
    def compressed(self):
        return self.original + "?auto=compress"

    @property
    def large2x(self):
        return self.__photo["src"]["large2x"]

    @property
    def large(self):
        return self.__photo["src"]["large"]

    @property
    def medium(self):
        return self.__photo["src"]["medium"]

    @property
    def small(self):
        return self.__photo["src"]["small"]

    @property
    def portrait(self):
        return self.__photo["src"]["portrait"]

    @property
    def landscape(self):
        return self.__photo["src"]["landscape"]

    @property
    def tiny(self):
        return self.__photo["src"]["tiny"]

    @property
    def extension(self):
        return self.original.split(".")[-1]


class Video:
    def __init__(self, json_video):
        self.__video = json_video

    @property
    def id(self):
        return int(self.__video["id"])

    @property
    def width(self):
        return int(self.__video["width"])

    @property
    def height(self):
        return int(self.__video["height"])

    @property
    def videographer(self):
        return self.__video["user"]["name"]

    @property
    def url(self):
        return self.__video["url"]

    @property
    def image_preview(self):
        return self.__video["image"]

    @property
    def description(self):
        return self.url.split("/")[-2].replace(f"-{self.id}", "").replace("-", " ")

    @property
    def duration(self):
        return self.__video["duration"]

    @property
    def highest_resolution_video(self):
        highest_resolution_video_dict = {}
        for dictionary in self.__video["video_files"]:
            if not highest_resolution_video_dict:
                highest_resolution_video_dict = dictionary
            else:
                if dictionary["width"] > highest_resolution_video_dict["width"]:
                    highest_resolution_video_dict = dictionary
        return highest_resolution_video_dict

    @property
    def highest_resolution_width(self):
        return int(self.highest_resolution_video["width"])

    @property
    def highest_resolution_height(self):
        return int(self.highest_resolution_video["height"])

    @property
    def link(self):
        return self.highest_resolution_video["link"].split("&")[0]

    @property
    def extension(self):
        return self.highest_resolution_video["file_type"].split("/")[-1]
