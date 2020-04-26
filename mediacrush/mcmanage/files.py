from ..files import delete_file
from ..objects import Album, FailedFile, Feedback, File, RedisObject


def files_delete(arguments):
    hash = arguments["<hash>"]
    if hash.startswith("./"):
        hash = hash[2:]

    f = File.from_hash(hash)
    if not f:
        print(("%r is not a valid file." % hash))
        return
    delete_file(f)
    print("Done, thank you.")
