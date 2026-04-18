"""Google Slides helper.

    from gslide_api import GSlide, create_presentation
    pres_id = create_presentation("My Deck")
    gs = GSlide(pres_id)
    gs.list_slides()                          # [{id, index, title}, ...]
    gs.add_slide(layout="TITLE_AND_BODY")     # returns slide id
    gs.delete_slide(slide_id)
    gs.add_text_box(slide_id, "Hello", x=100, y=100, w=400, h=60)
    gs.replace_all("{{name}}", "World")       # find & replace across whole deck
    gs.add_image(slide_id, url, x=50, y=120, w=300, h=200)
    gs.duplicate_slide(slide_id)
    gs.batch_update([...])                    # raw Slides API requests
"""
from __future__ import annotations

import uuid
from typing import Any

from googleapiclient.discovery import build

from gsheet_api import _ensure_creds


SLIDE_LAYOUTS = [
    "BLANK", "CAPTION_ONLY", "TITLE", "TITLE_AND_BODY", "TITLE_AND_TWO_COLUMNS",
    "TITLE_ONLY", "SECTION_HEADER", "SECTION_TITLE_AND_DESCRIPTION",
    "ONE_COLUMN_TEXT", "MAIN_POINT", "BIG_NUMBER",
]


def create_presentation(title: str) -> str:
    svc = build("slides", "v1", credentials=_ensure_creds())
    resp = svc.presentations().create(body={"title": title}).execute()
    return resp["presentationId"]


class GSlide:
    def __init__(self, presentation_id: str):
        self.id = presentation_id
        self.svc = build("slides", "v1", credentials=_ensure_creds())

    def get(self) -> dict:
        return self.svc.presentations().get(presentationId=self.id).execute()

    def title(self) -> str:
        return self.get().get("title", "")

    def list_slides(self) -> list[dict]:
        pres = self.get()
        out = []
        for i, s in enumerate(pres.get("slides", [])):
            out.append({
                "id": s.get("objectId"),
                "index": i,
                "layout": (s.get("slideProperties") or {}).get("layoutObjectId"),
            })
        return out

    def add_slide(self, layout: str = "BLANK", index: int | None = None) -> str:
        slide_id = f"s_{uuid.uuid4().hex[:12]}"
        req: dict[str, Any] = {
            "createSlide": {
                "objectId": slide_id,
                "slideLayoutReference": {"predefinedLayout": layout},
            }
        }
        if index is not None:
            req["createSlide"]["insertionIndex"] = index
        self.batch_update([req])
        return slide_id

    def delete_slide(self, slide_id: str) -> dict:
        return self.batch_update([{"deleteObject": {"objectId": slide_id}}])

    def duplicate_slide(self, slide_id: str) -> str:
        new_id = f"s_{uuid.uuid4().hex[:12]}"
        self.batch_update([{
            "duplicateObject": {"objectId": slide_id, "objectIds": {slide_id: new_id}}
        }])
        return new_id

    def add_text_box(
        self,
        slide_id: str,
        text: str,
        x: float = 50,
        y: float = 50,
        w: float = 400,
        h: float = 60,
    ) -> str:
        box_id = f"tb_{uuid.uuid4().hex[:12]}"
        self.batch_update([
            {"createShape": {
                "objectId": box_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": w, "unit": "PT"},
                             "height": {"magnitude": h, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "PT"},
                },
            }},
            {"insertText": {"objectId": box_id, "text": text}},
        ])
        return box_id

    def add_image(
        self,
        slide_id: str,
        url: str,
        x: float = 50,
        y: float = 50,
        w: float = 300,
        h: float = 200,
    ) -> str:
        img_id = f"img_{uuid.uuid4().hex[:12]}"
        self.batch_update([{
            "createImage": {
                "objectId": img_id,
                "url": url,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": w, "unit": "PT"},
                             "height": {"magnitude": h, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "PT"},
                },
            }
        }])
        return img_id

    def replace_all(self, find: str, replace: str, match_case: bool = False) -> dict:
        return self.batch_update([{
            "replaceAllText": {
                "containsText": {"text": find, "matchCase": match_case},
                "replaceText": replace,
            }
        }])

    def batch_update(self, requests: list[dict]) -> dict:
        return self.svc.presentations().batchUpdate(
            presentationId=self.id, body={"requests": requests}
        ).execute()
