import pathlib
import mimetypes
from io import BytesIO
from urllib import request
from urllib.parse import urlparse
from urllib.request import Request
from functools import cached_property

class Download(BytesIO):
    def __init__(self, url, *, max_size=0):
        super().__init__()

        headers = {
            'User-Agent': 'ABBY 9001'
        }

        self.request = request.urlopen(Request(url, headers=headers))
        self.max_size = max_size

        file_path = pathlib.Path(urlparse(url).path)
        self.name = file_path.name
        self.suffix = file_path.suffix
        self.mime = self.request.info().get_content_type()

        if not self.suffix:
            self.suffix = mimetypes.guess_extension(self.mime)

            if self.suffix == '.jpe': # mimetypes fix
                self.suffix = '.jpeg'

            self.name = self.name + self.suffix

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.request.close()
        self.close()

    def get(self, chunk_size: int = 4096):
        file_size = 0
        
        while True:
            file_size += chunk_size

            if file_size > self.max_size > 0:
                raise IOError('file size exceeds limit')

            if chunk := self.request.read(chunk_size):
                super().write(chunk)
            else:
                break

        self.seek(0)

    @cached_property
    def is_media(self):
        return any((x in self.mime for x in {'video', 'image', 'audio'}))

    @cached_property
    def is_image(self):
        return 'image' in self.mime

    @cached_property
    def is_video(self):
        return 'video' in self.mime or 'image/gif' in self.mime
