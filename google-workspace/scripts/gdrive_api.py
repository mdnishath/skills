"""Google Drive helper — file-level operations across the user's entire Drive.

Works for any mime type: Sheets, Docs, Slides, PDFs, images, Office files, etc.

Usage:
    from gdrive_api import GDrive
    gd = GDrive()
    gd.list_files()                              # all files, newest first
    gd.list_files(mime="document")               # shortcut for Docs
    gd.find("my report")                         # search by title
    gd.get_metadata(file_id)
    gd.download(file_id, "local.pdf")            # binary
    gd.export(file_id, "pdf", "report.pdf")      # Google-native → pdf/docx/xlsx
    gd.upload("local.xlsx", parent_folder=None)  # upload a file
    gd.create_folder("My Folder")
    gd.move(file_id, folder_id)
    gd.rename(file_id, "new name")
    gd.delete(file_id)                           # to trash
    gd.share(file_id, email, role="writer")      # add a collaborator
"""
from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Iterable

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from gsheet_api import _ensure_creds  # reuse the same OAuth token


MIME_SHORT = {
    "spreadsheet": "application/vnd.google-apps.spreadsheet",
    "document":    "application/vnd.google-apps.document",
    "presentation":"application/vnd.google-apps.presentation",
    "folder":      "application/vnd.google-apps.folder",
    "pdf":         "application/pdf",
    "form":        "application/vnd.google-apps.form",
    "drawing":     "application/vnd.google-apps.drawing",
}

EXPORT_FORMATS = {
    # Google-native mime → preferred export MIME
    "spreadsheet": {
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "csv":  "text/csv",
        "pdf":  "application/pdf",
    },
    "document": {
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "pdf":  "application/pdf",
        "txt":  "text/plain",
        "html": "text/html",
    },
    "presentation": {
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "pdf":  "application/pdf",
    },
    "drawing": {
        "png": "image/png",
        "pdf": "application/pdf",
        "svg": "image/svg+xml",
    },
}


class GDrive:
    def __init__(self):
        self.svc = build("drive", "v3", credentials=_ensure_creds())

    # ---- listing & search ----

    def list_files(
        self,
        mime: str | None = None,
        parent: str | None = None,
        limit: int = 50,
        include_trashed: bool = False,
    ) -> list[dict]:
        parts = []
        if mime:
            m = MIME_SHORT.get(mime, mime)
            parts.append(f"mimeType='{m}'")
        if parent:
            parts.append(f"'{parent}' in parents")
        if not include_trashed:
            parts.append("trashed=false")
        q = " and ".join(parts) if parts else None
        resp = self.svc.files().list(
            q=q,
            fields="files(id,name,mimeType,modifiedTime,size,webViewLink,parents,owners(emailAddress))",
            pageSize=limit,
            orderBy="modifiedTime desc",
        ).execute()
        return resp.get("files", [])

    def find(self, name: str, exact: bool = False, mime: str | None = None) -> list[dict]:
        op = "=" if exact else "contains"
        parts = [f"name {op} '{name}'", "trashed=false"]
        if mime:
            m = MIME_SHORT.get(mime, mime)
            parts.append(f"mimeType='{m}'")
        resp = self.svc.files().list(
            q=" and ".join(parts),
            fields="files(id,name,mimeType,modifiedTime,webViewLink)",
            pageSize=50,
            orderBy="modifiedTime desc",
        ).execute()
        return resp.get("files", [])

    def get_metadata(self, file_id: str) -> dict:
        return self.svc.files().get(
            fileId=file_id,
            fields="id,name,mimeType,modifiedTime,size,webViewLink,parents,owners,description",
        ).execute()

    # ---- download / export ----

    def download(self, file_id: str, dest_path: str) -> str:
        req = self.svc.files().get_media(fileId=file_id)
        with io.FileIO(dest_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        return dest_path

    def export(self, file_id: str, fmt: str, dest_path: str) -> str:
        """Export Google-native file (Docs/Sheets/Slides) as pdf/docx/xlsx/etc."""
        meta = self.get_metadata(file_id)
        native = meta["mimeType"].split(".")[-1]  # spreadsheet / document / presentation
        mime = EXPORT_FORMATS.get(native, {}).get(fmt)
        if not mime:
            raise ValueError(f"Cannot export {native!r} to {fmt!r}. Options: {list(EXPORT_FORMATS.get(native,{}).keys())}")
        req = self.svc.files().export_media(fileId=file_id, mimeType=mime)
        with io.FileIO(dest_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        return dest_path

    # ---- upload / create ----

    def upload(self, local_path: str, parent_folder: str | None = None, title: str | None = None) -> str:
        body = {"name": title or Path(local_path).name}
        if parent_folder:
            body["parents"] = [parent_folder]
        media = MediaFileUpload(local_path, resumable=True)
        resp = self.svc.files().create(body=body, media_body=media, fields="id,name").execute()
        return resp["id"]

    def upload_as_google_sheet(self, local_xlsx: str, title: str | None = None, parent_folder: str | None = None) -> str:
        """Upload an xlsx and convert it to a native Google Sheet."""
        body = {
            "name": title or Path(local_xlsx).stem,
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }
        if parent_folder:
            body["parents"] = [parent_folder]
        media = MediaFileUpload(local_xlsx, resumable=True,
                                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        resp = self.svc.files().create(body=body, media_body=media, fields="id").execute()
        return resp["id"]

    def create_folder(self, name: str, parent: str | None = None) -> str:
        body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent:
            body["parents"] = [parent]
        resp = self.svc.files().create(body=body, fields="id").execute()
        return resp["id"]

    # ---- modify ----

    def rename(self, file_id: str, new_name: str) -> None:
        self.svc.files().update(fileId=file_id, body={"name": new_name}).execute()

    def move(self, file_id: str, new_parent: str) -> None:
        # Get current parents to remove
        meta = self.svc.files().get(fileId=file_id, fields="parents").execute()
        old_parents = ",".join(meta.get("parents", []))
        self.svc.files().update(
            fileId=file_id,
            addParents=new_parent,
            removeParents=old_parents,
            fields="id,parents",
        ).execute()

    def delete(self, file_id: str, permanent: bool = False) -> None:
        if permanent:
            self.svc.files().delete(fileId=file_id).execute()
        else:
            self.svc.files().update(fileId=file_id, body={"trashed": True}).execute()

    def restore(self, file_id: str) -> None:
        self.svc.files().update(fileId=file_id, body={"trashed": False}).execute()

    def copy(self, file_id: str, new_title: str | None = None, parent: str | None = None) -> str:
        body = {}
        if new_title:
            body["name"] = new_title
        if parent:
            body["parents"] = [parent]
        resp = self.svc.files().copy(fileId=file_id, body=body, fields="id").execute()
        return resp["id"]

    # ---- sharing (requires additional Drive scope — prompt user to re-auth if denied) ----

    def share(self, file_id: str, email: str, role: str = "writer", notify: bool = True, message: str | None = None) -> None:
        """role: 'reader' / 'commenter' / 'writer' / 'owner'."""
        body = {"type": "user", "role": role, "emailAddress": email}
        kwargs = {"fileId": file_id, "body": body, "sendNotificationEmail": notify}
        if message:
            kwargs["emailMessage"] = message
        self.svc.permissions().create(**kwargs).execute()

    def list_permissions(self, file_id: str) -> list[dict]:
        resp = self.svc.permissions().list(
            fileId=file_id, fields="permissions(id,type,role,emailAddress,displayName)"
        ).execute()
        return resp.get("permissions", [])
