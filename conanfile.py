
import os.path
import shutil

import conans
from conans import tools


class GzipDownloader:

    def __init__(self, base_name, url, md5_sum):
        self._base_name = base_name
        self._url = url
        self._md5_sum = md5_sum
        self._gzip_name = "{}.tar.gz".format(self._base_name)

    def _get_gzip_path(self, folder):
        return os.path.join(folder, self._gzip_name)

    def get_extracted_directory(self, folder):
        return os.path.join(folder, self._base_name)

    def _confirm_valid_gzip_file_or_download(self, folder):
        gzip_path = self._get_gzip_path(folder)
        if os.path.exists(gzip_path):
            try:
                tools.check_md5(gzip_path, self._md5_sum)
                return gzip_path
            except BaseException:
                os.remove(gzip_path)

        tools.download(self._url, gzip_path)
        tools.check_md5(gzip_path, self._md5_sum)
        return gzip_path

    def _clean_extracted_directory(self, folder):
        extracted_directory = self.get_extracted_directory(folder)
        if os.path.exists(extracted_directory):
            shutil.rmtree(extracted_directory)

    def download(self, folder):
        gzip_path = self._confirm_valid_gzip_file_or_download(folder)
        self._clean_extracted_directory(folder)
        tools.unzip(gzip_path)


class BasicSdl(conans.ConanFile):
    name = "sdl2_image"
    version = "b_2.0.5"
    license = ""
    author = ""
    description = "A basic version of the SDL2 image library"

    settings = "os", "compiler", "build_type", "arch"

    requires = (
        "basic-sdl2/b_2.0.9@TimSimpson/testing",
    )

    options = {
        "bmp": [True, False],
        "fPIC": [True, False],
        "gif": [True, False],
        "imageio": [True, False],
        "jpg": [True, False],
        "lbm": [True, False],
        "pcx": [True, False],
        "png": [True, False],
        "pnm": [True, False],
        "shared": [True, False],
        "svg": [True, False],
        "tga": [True, False],
        "tif": [True, False],
        "webp": [True, False],
        "xcf": [True, False],
        "xpm": [True, False],
        "xv": [True, False],
    }
    default_options = {
        "bmp": True,
        "fPIC": True,
        "gif": True,
        "imageio": False,
        "jpg": True,
        "lbm": True,
        "pcx": True,
        "png": True,
        "pnm": True,
        "shared": False,
        "svg": True,
        "tga": True,
        "tif": True,
        "webp": True,
        "xcf": True,
        "xpm": True,
        "xv": True,
    }

    _gzip_downloader = GzipDownloader(
        base_name='SDL2_image-2.0.5',
        url="https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.5.tar.gz",
        md5_sum="f26f3a153360a8f09ed5220ef7b07aea"
    )

    def source(self):
        self._gzip_downloader.download(self.source_folder)

    def build(self):
        src = self._gzip_downloader.get_extracted_directory(self.source_folder)
        with tools.chdir(self.build_folder):
            atools = conans.AutoToolsBuildEnvironment(self)
            atools.configure(configure_dir=src)
            atools.make()
            atools.install()

    def package(self):
        built_packages = os.path.join(self.build_folder, "package")
        self.copy("*", src=built_packages)

    def package_info(self):
        self.cpp_info.name = "sdl2_image"
        self.cpp_info.libs = ["SDL2_image"]
        self.cpp_info.includedirs.append(os.path.join("include", "SDL2"))
