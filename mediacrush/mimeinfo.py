import operator
import functools

MIME_EXTENSIONS = {
    "text/plain": ["txt"],
    "image/gif": ["gif"],
    "image/jpeg": ["jpeg", "jpg"],
    "image/png": ["png"],
    "image/svg+xml": ["svg", "svgz"],
    "image/tiff": ["tif", "tiff"],
    "image/webp": ["webp"],
    "image/x-icon": ["ico"],
    "image/x-jng": ["jng"],
    "image/x-ms-bmp": ["bmp"],
    "audio/midi": ["mid", "midi", "kar"],
    "audio/mpeg": ["mp3"],
    "audio/ogg": ["ogg"],
    "audio/x-m4a": ["m4a"],
    "video/3gpp": ["3gpp", "3gp"],
    "video/mp4": ["mp4"],
    "video/mpeg": ["mpeg", "mpg"],
    "video/quicktime": ["mov"],
    "video/webm": ["webm"],
    "video/x-flv": ["flv"],
    "video/x-m4v": ["m4v"],
    "video/x-mng": ["mng"],
    "video/x-ms-asf": ["asx", "asf"],
    "video/x-ms-wmv": ["wmv"],
    "video/x-msvideo": ["avi"],
}

EXTENSIONS = functools.reduce(operator.iconcat, MIME_EXTENSIONS.values(), [])


def extension(f):
    if "." not in f:
        return None
    ext = f.rsplit(".", 1)[1].lower()
    if ext in EXTENSIONS:
        return ext
    return None


def get_mimetype(url):
    ext = extension(url) if "." in url else url
    for k, v in MIME_EXTENSIONS.items():
        if ext in v:
            return k
    return None
