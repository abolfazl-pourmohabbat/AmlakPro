from pathlib import PurePosixPath
import os
import tempfile

from django.core.files.base import File
from django.core.files.storage import Storage


class VercelBlobStorage(Storage):
    """Django storage backend backed by a public Vercel Blob store."""

    access = "public"

    def _client(self):
        from vercel.blob import BlobClient
        return BlobClient()

    def _save(self, name, content):
        filename = PurePosixPath(name.replace("\\", "/")).as_posix()
        content_type = getattr(content, "content_type", None) or "application/octet-stream"
        data = b"".join(content.chunks()) if hasattr(content, "chunks") else content.read()
        temp = tempfile.NamedTemporaryFile(prefix="amlakpro-upload-", suffix=".tmp", delete=False)
        try:
            temp.write(data)
            temp.close()
            with self._client() as client:
                blob = client.upload_file(
                    temp.name,
                    filename,
                    access=self.access,
                    content_type=content_type,
                )
            return blob.pathname
        finally:
            try:
                os.unlink(temp.name)
            except FileNotFoundError:
                pass

    def _open(self, name, mode="rb"):
        if "w" in mode or "+" in mode:
            raise NotImplementedError("Vercel Blob storage is read-only through Django open().")

        temp = tempfile.NamedTemporaryFile(prefix="amlakpro-blob-", suffix=".tmp", delete=False)
        temp.close()
        with self._client() as client:
            client.download_file(name, temp.name, overwrite=True)
        return File(open(temp.name, mode), name=name)

    def delete(self, name):
        if not name:
            return
        with self._client() as client:
            client.delete([name])

    def exists(self, name):
        if not name:
            return False
        try:
            with self._client() as client:
                client.head(name)
            return True
        except Exception:
            return False

    def url(self, name):
        if not name:
            return ""
        if name.startswith("http://") or name.startswith("https://"):
            return name
        try:
            with self._client() as client:
                return client.head(name).url
        except Exception:
            return ""

    def size(self, name):
        with self._client() as client:
            return client.head(name).size

    def get_available_name(self, name, max_length=None):
        # Blob uploads use add_random_suffix=True, so filenames never collide.
        return name

    def path(self, name):
        raise NotImplementedError("Vercel Blob does not expose a local filesystem path.")
