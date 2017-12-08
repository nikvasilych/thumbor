from thumbor.result_storages.fingerprint_file_storage import Storage as FingerPrintFileStroreage
from thumbor.result_storages.joined_path_file_storage import JoinedPathFileStorageMixin


class Storage(JoinedPathFileStorageMixin, FingerPrintFileStroreage):
    """
    joined_path_file_storage + fingerprint_file_storage
    """
    pass
