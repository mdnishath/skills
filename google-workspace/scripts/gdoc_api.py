"""Google Docs helper.

    from gdoc_api import GDoc, create_doc
    doc_id = create_doc("My Report")
    gd = GDoc(doc_id)
    gd.get_text()                          # full plain text
    gd.append_text("New paragraph.\\n")     # add at end
    gd.insert_text(1, "Intro: ")           # insert at index 1
    gd.replace_all("old", "new")           # find & replace
    gd.append_heading("Section 2", level=1)# structured heading
    gd.insert_image(url, index=None)       # image from URL (publicly accessible)
    gd.batch_update([...])                 # raw Docs API requests
"""
from __future__ import annotations

from typing import Any

from googleapiclient.discovery import build

from gsheet_api import _ensure_creds


def create_doc(title: str) -> str:
    svc = build("docs", "v1", credentials=_ensure_creds())
    resp = svc.documents().create(body={"title": title}).execute()
    return resp["documentId"]


class GDoc:
    def __init__(self, document_id: str):
        self.id = document_id
        self.svc = build("docs", "v1", credentials=_ensure_creds())

    def get(self) -> dict:
        return self.svc.documents().get(documentId=self.id).execute()

    def title(self) -> str:
        return self.get().get("title", "")

    def get_text(self) -> str:
        """Flatten all text runs into a single string."""
        doc = self.get()
        chunks: list[str] = []
        for el in doc.get("body", {}).get("content", []):
            para = el.get("paragraph")
            if not para:
                continue
            for run in para.get("elements", []):
                tr = run.get("textRun")
                if tr:
                    chunks.append(tr.get("content", ""))
        return "".join(chunks)

    def _end_index(self) -> int:
        """Index right before the trailing newline of the document body."""
        doc = self.get()
        content = doc.get("body", {}).get("content", [])
        if not content:
            return 1
        last = content[-1]
        end = last.get("endIndex", 1)
        return max(1, end - 1)

    def append_text(self, text: str) -> dict:
        return self.batch_update([{
            "insertText": {"location": {"index": self._end_index()}, "text": text}
        }])

    def insert_text(self, index: int, text: str) -> dict:
        return self.batch_update([{
            "insertText": {"location": {"index": index}, "text": text}
        }])

    def replace_all(self, find: str, replace: str, match_case: bool = False) -> dict:
        return self.batch_update([{
            "replaceAllText": {
                "containsText": {"text": find, "matchCase": match_case},
                "replaceText": replace,
            }
        }])

    def append_heading(self, text: str, level: int = 1) -> dict:
        idx = self._end_index()
        heading_type = f"HEADING_{max(1, min(6, level))}"
        return self.batch_update([
            {"insertText": {"location": {"index": idx}, "text": text + "\n"}},
            {"updateParagraphStyle": {
                "range": {"startIndex": idx, "endIndex": idx + len(text) + 1},
                "paragraphStyle": {"namedStyleType": heading_type},
                "fields": "namedStyleType",
            }},
        ])

    def insert_image(self, uri: str, index: int | None = None) -> dict:
        if index is None:
            index = self._end_index()
        return self.batch_update([{
            "insertInlineImage": {"location": {"index": index}, "uri": uri}
        }])

    def clear(self) -> dict:
        """Delete everything except the final newline."""
        end = self._end_index()
        if end <= 1:
            return {}
        return self.batch_update([{
            "deleteContentRange": {"range": {"startIndex": 1, "endIndex": end}}
        }])

    def batch_update(self, requests: list[dict]) -> dict:
        return self.svc.documents().batchUpdate(
            documentId=self.id, body={"requests": requests}
        ).execute()
