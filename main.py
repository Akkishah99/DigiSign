"""
PDF Generator from Digital Certificate + Signed XML Data
Run: python main.py
Output: output.pdf
"""

import json
import base64
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── Raw JSON data (paste your full JSON string here or load from file) ──────
RAW_JSON = r"""{"fingerPrint":"/mLsiI6fjWasHa6AGjTB/PVmcFbdUUV6nBpbjmSWnho=","siginedCertificate":{"serialNumber":"51876627","label":"SAHIL BALDEVBHAI AMIN's Capricorn CA 2014 ID","commonName":"SAHIL BALDEVBHAI AMIN","issuerName":"Capricorn CA 2014","validFrom":"May 3, 2022 12:19:49 PM","validTill":"Mar 5, 2024 12:00:00 PM","subject":"C=IN,O=DHYEY CONSULTING SERVICES PRIVATE LIMITED,OU=Management,TelephoneNumber=b46543fd63080ef932a01ecd16eb09f8e1a191f30d02c37499a19ee58d584b02,PostalCode=390023,ST=Gujarat,SERIALNUMBER=548f2b9fee8888845b6dc5f7a7227a077e914514ba45fca63691661c437c1ced,CN=SAHIL BALDEVBHAI AMIN","keyId":"63657274696669636174652E6469676974616C34343561643635642D653333392D346332342D623835632D6231356634323530326131353100","keyStoreID":"2B1173AA00630004","keyStoreName":"ePass2003","keyStoreDisplayName":"ePass V 2.0-2B1173AA00630004(ePass2003)","subjectKeyIdentifierString":"45f393c43b7a7f4d"},"signedText":"PD94bWwgdmVyc2lvbj0iMS4wIj8+PGNhdGFsb2c+PGJvb2sgaWQ9ImJrMTAxIj48YXV0aG9yPkdhbWJhcmRlbGxhLCBNYXR0aGV3PC9hdXRob3I+PHRpdGxlPlhNTCBEZXZlbG9wZXIncyBHdWlkZTwvdGl0bGU+PGdlbnJlPkNvbXB1dGVyPC9nZW5yZT48cHJpY2U+NDQuOTU8L3ByaWNlPjxwdWJsaXNoX2RhdGU+MjAwMC0xMC0wMTwvcHVibGlzaF9kYXRlPjxkZXNjcmlwdGlvbj5BbiBpbi1kZXB0aCBsb29rIGF0IGNyZWF0aW5nIGFwcGxpY2F0aW9ucyANCiAgICAgIHdpdGggWE1MLjwvZGVzY3JpcHRpb24+PC9ib29rPjxib29rIGlkPSJiazEwMiI+PGF1dGhvcj5SYWxscywgS2ltPC9hdXRob3I+PHRpdGxlPk1pZG5pZ2h0IFJhaW48L3RpdGxlPjxnZW5yZT5GYW50YXN5PC9nZW5yZT48cHJpY2U+NS45NTwvcHJpY2U+PHB1Ymxpc2hfZGF0ZT4yMDAwLTEyLTE2PC9wdWJsaXNoX2RhdGU+PGRlc2NyaXB0aW9uPkEgZm9ybWVyIGFyY2hpdGVjdCBiYXR0bGVzIGNvcnBvcmF0ZSB6b21iaWVzLCANCiAgICAgIGFuIGV2aWwgc29yY2VyZXNzLCBhbmQgaGVyIG93biBjaGlsZGhvb2QgdG8gYmVjb21lIHF1ZWVuIA0KICAgICAgb2YgdGhlIHdvcmxkLjwvZGVzY3JpcHRpb24+PC9ib29rPjxib29rIGlkPSJiazEwMyI+PGF1dGhvcj5Db3JldHMsIEV2YTwvYXV0aG9yPjx0aXRsZT5NYWV2ZSBBc2NlbmRhbnQ8L3RpdGxlPjxnZW5yZT5GYW50YXN5PC9nZW5yZT48cHJpY2U+NS45NTwvcHJpY2U+PHB1Ymxpc2hfZGF0ZT4yMDAwLTExLTE3PC9wdWJsaXNoX2RhdGU+PGRlc2NyaXB0aW9uPkFmdGVyIHRoZSBjb2xsYXBzZSBvZiBhIG5hbm90ZWNobm9sb2d5IA0KICAgICAgc29jaWV0eSBpbiBFbmdsYW5kLCB0aGUgeW91bmcgc3Vydml2b3JzIGxheSB0aGUgDQogICAgICBmb3VuZGF0aW9uIGZvciBhIG5ldyBzb2NpZXR5LjwvZGVzY3JpcHRpb24+PC9ib29rPjxib29rIGlkPSJiazEwNCI+PGF1dGhvcj5Db3JldHMsIEV2YTwvYXV0aG9yPjx0aXRsZT5PYmVyb24ncyBMZWdhY3k8L3RpdGxlPjxnZW5yZT5GYW50YXN5PC9nZW5yZT48cHJpY2U+NS45NTwvcHJpY2U+PHB1Ymxpc2hfZGF0ZT4yMDAxLTAzLTEwPC9wdWJsaXNoX2RhdGU+PGRlc2NyaXB0aW9uPkluIHBvc3QtYXBvY2FseXBzZSBFbmdsYW5kLCB0aGUgbXlzdGVyaW91cyANCiAgICAgIGFnZW50IGtub3duIG9ubHkgYXMgT2Jlcm9uIGhlbHBzIHRvIGNyZWF0ZSBhIG5ldyBsaWZlIA0KICAgICAgZm9yIHRoZSBpbmhhYml0YW50cyBvZiBMb25kb24uIFNlcXVlbCB0byBNYWV2ZSANCiAgICAgIEFzY2VuZGFudC48L2Rlc2NyaXB0aW9uPjwvYm9vaz48Ym9vayBpZD0iYmsxMDUiPjxhdXRob3I+Q29yZXRzLCBFdmE8L2F1dGhvcj48dGl0bGU+VGhlIFN1bmRlcmVkIEdyYWlsPC90aXRsZT48Z2VucmU+RmFudGFzeTwvZ2VucmU+PHByaWNlPjUuOTU8L3ByaWNlPjxwdWJsaXNoX2RhdGU+MjAwMS0wOS0xMDwvcHVibGlzaF9kYXRlPjxkZXNjcmlwdGlvbj5UaGUgdHdvIGRhdWdodGVycyBvZiBNYWV2ZSwgaGFsZi1zaXN0ZXJzLCANCiAgICAgIGJhdHRsZSBvbmUgYW5vdGhlciBmb3IgY29udHJvbCBvZiBFbmdsYW5kLiBTZXF1ZWwgdG8gDQogICAgICBPYmVyb24ncyBMZWdhY3kuPC9kZXNjcmlwdGlvbj48L2Jvb2s+PGJvb2sgaWQ9ImJrMTA2Ij48YXV0aG9yPlJhbmRhbGwsIEN5bnRoaWE8L2F1dGhvcj48dGl0bGU+TG92ZXIgQmlyZHM8L3RpdGxlPjxnZW5yZT5Sb21hbmNlPC9nZW5yZT48cHJpY2U+NC45NTwvcHJpY2U+PHB1Ymxpc2hfZGF0ZT4yMDAwLTA5LTAyPC9wdWJsaXNoX2RhdGU+PGRlc2NyaXB0aW9uPldoZW4gQ2FybGEgbWVldHMgUGF1bCBhdCBhbiBvcm5pdGhvbG9neSANCiAgICAgIGNvbmZlcmVuY2UsIHRlbXBlcnMgZmx5IGFzIGZlYXRoZXJzIGdldCBydWZmbGVkLjwvZGVzY3JpcHRpb24+PC9ib29rPjxib29rIGlkPSJiazEwNyI+PGF1dGhvcj5UaHVybWFuLCBQYXVsYTwvYXV0aG9yPjx0aXRsZT5TcGxpc2ggU3BsYXNoPC90aXRsZT48Z2VucmU+Um9tYW5jZTwvZ2VucmU+PHByaWNlPjQuOTU8L3ByaWNlPjxwdWJsaXNoX2RhdGU+MjAwMC0xMS0wMjwvcHVibGlzaF9kYXRlPjxkZXNjcmlwdGlvbj5BIGRlZXAgc2VhIGRpdmVyIGZpbmRzIHRydWUgbG92ZSB0d2VudHkgDQogICAgICB0aG91c2FuZCBsZWFndWVzIGJlbmVhdGggdGhlIHNlYS48L2Rlc2NyaXB0aW9uPjwvYm9vaz48Ym9vayBpZD0iYmsxMDgiPjxhdXRob3I+S25vcnIsIFN0ZWZhbjwvYXV0aG9yPjx0aXRsZT5DcmVlcHkgQ3Jhd2xpZXM8L3RpdGxlPjxnZW5yZT5Ib3Jyb3I8L2dlbnJlPjxwcmljZT40Ljk1PC9wcmljZT48cHVibGlzaF9kYXRlPjIwMDAtMTItMDY8L3B1Ymxpc2hfZGF0ZT48ZGVzY3JpcHRpb24+QW4gYW50aG9sb2d5IG9mIGhvcnJvciBzdG9yaWVzIGFib3V0IHJvYWNoZXMsDQogICAgICBjZW50aXBlZGVzLCBzY29ycGlvbnMgIGFuZCBvdGhlciBpbnNlY3RzLjwvZGVzY3JpcHRpb24+PC9ib29rPjxib29rIGlkPSJiazEwOSI+PGF1dGhvcj5LcmVzcywgUGV0ZXI8L2F1dGhvcj48dGl0bGU+UGFyYWRveCBMb3N0PC90aXRsZT48Z2VucmU+U2NpZW5jZSBGaWN0aW9uPC9nZW5yZT48cHJpY2U+Ni45NTwvcHJpY2U+PHB1Ymxpc2hfZGF0ZT4yMDAwLTExLTAyPC9wdWJsaXNoX2RhdGU+PGRlc2NyaXB0aW9uPkFmdGVyIGFuIGluYWR2ZXJ0YW50IHRyaXAgdGhyb3VnaCBhIEhlaXNlbmJlcmcNCiAgICAgIFVuY2VydGFpbnR5IERldmljZSwgSmFtZXMgU2Fsd2F5IGRpc2NvdmVycyB0aGUgcHJvYmxlbXMgDQogICAgICBvZiBiZWluZyBxdWFudHVtLjwvZGVzY3JpcHRpb24+PC9ib29rPjxib29rIGlkPSJiazExMCI+PGF1dGhvcj5PJ0JyaWVuLCBUaW08L2F1dGhvcj48dGl0bGU+TWljcm9zb2Z0IC5ORVQ6IFRoZSBQcm9ncmFtbWluZyBCaWJsZTwvdGl0bGU+PGdlbnJlPkNvbXB1dGVyPC9nZW5yZT48cHJpY2U+MzYuOTU8L3ByaWNlPjxwdWJsaXNoX2RhdGU+MjAwMC0xMi0wOTwvcHVibGlzaF9kYXRlPjxkZXNjcmlwdGlvbj5NaWNyb3NvZnQncyAuTkVUIGluaXRpYXRpdmUgaXMgZXhwbG9yZWQgaW4gDQogICAgICBkZXRhaWwgaW4gdGhpcyBkZWVwIHByb2dyYW1tZXIncyByZWZlcmVuY2UuPC9kZXNjcmlwdGlvbj48L2Jvb2s+PGJvb2sgaWQ9ImJrMTExIj48YXV0aG9yPk8nQnJpZW4sIFRpbTwvYXV0aG9yPjx0aXRsZT5NU1hNTDM6IEEgQ29tcHJlaGVuc2l2ZSBHdWlkZTwvdGl0bGU+PGdlbnJlPkNvbXB1dGVyPC9nZW5yZT48cHJpY2U+MzYuOTU8L3ByaWNlPjxwdWJsaXNoX2RhdGU+MjAwMC0xMi0wMTwvcHVibGlzaF9kYXRlPjxkZXNjcmlwdGlvbj5UaGUgTWljcm9zb2Z0IE1TWE1MMyBwYXJzZXIgaXMgY292ZXJlZCBpbiANCiAgICAgIGRldGFpbCwgd2l0aCBhdHRlbnRpb24gdG8gWE1MIERPTSBpbnRlcmZhY2VzLCBYU0xUIHByb2Nlc3NpbmcsIA0KICAgICAgU0FYIGFuZCBtb3JlLjwvZGVzY3JpcHRpb24+PC9ib29rPjxib29rIGlkPSJiazExMiI+PGF1dGhvcj5HYWxvcywgTWlrZTwvYXV0aG9yPjx0aXRsZT5WaXN1YWwgU3R1ZGlvIDc6IEEgQ29tcHJlaGVuc2l2ZSBHdWlkZTwvdGl0bGU+PGdlbnJlPkNvbXB1dGVyPC9nZW5yZT48cHJpY2U+NDkuOTU8L3ByaWNlPjxwdWJsaXNoX2RhdGU+MjAwMS0wNC0xNjwvcHVibGlzaF9kYXRlPjxkZXNjcmlwdGlvbj5NaWNyb3NvZnQgVmlzdWFsIFN0dWRpbyA3IGlzIGV4cGxvcmVkIGluIGRlcHRoLA0KICAgICAgbG9va2luZyBhdCBob3cgVmlzdWFsIEJhc2ljLCBWaXN1YWwgQysrLCBDIywgYW5kIEFTUCsgYXJlIA0KICAgICAgaW50ZWdyYXRlZCBpbnRvIGEgY29tcHJlaGVuc2l2ZSBkZXZlbG9wbWVudCANCiAgICAgIGVudmlyb25tZW50LjwvZGVzY3JpcHRpb24+PC9ib29rPg==","status":"1"}"""


# ── Colour palette ───────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1B3A6B")
MID_BLUE    = colors.HexColor("#2B5EA7")
LIGHT_BLUE  = colors.HexColor("#EAF1FB")
ACCENT      = colors.HexColor("#F0A500")
GREY_TEXT   = colors.HexColor("#555555")
WHITE       = colors.white
GREEN       = colors.HexColor("#2E7D32")


# ── Styles ───────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    custom = {
        "DocTitle": ParagraphStyle(
            "DocTitle", parent=base["Title"],
            fontSize=22, textColor=WHITE, alignment=TA_CENTER,
            spaceAfter=6, fontName="Helvetica-Bold"
        ),
        "DocSubtitle": ParagraphStyle(
            "DocSubtitle", parent=base["Normal"],
            fontSize=10, textColor=colors.HexColor("#CCDDFF"),
            alignment=TA_CENTER, spaceAfter=4
        ),
        "SectionHeading": ParagraphStyle(
            "SectionHeading", parent=base["Heading1"],
            fontSize=13, textColor=DARK_BLUE,
            spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold",
            borderPad=4
        ),
        "FieldLabel": ParagraphStyle(
            "FieldLabel", parent=base["Normal"],
            fontSize=9, textColor=GREY_TEXT, fontName="Helvetica-Bold"
        ),
        "FieldValue": ParagraphStyle(
            "FieldValue", parent=base["Normal"],
            fontSize=9, textColor=colors.black, fontName="Helvetica",
            wordWrap="CJK"
        ),
        "BookTitle": ParagraphStyle(
            "BookTitle", parent=base["Normal"],
            fontSize=10, textColor=DARK_BLUE, fontName="Helvetica-Bold"
        ),
        "BookBody": ParagraphStyle(
            "BookBody", parent=base["Normal"],
            fontSize=8.5, textColor=GREY_TEXT, leading=13
        ),
        "StatusOK": ParagraphStyle(
            "StatusOK", parent=base["Normal"],
            fontSize=10, textColor=GREEN, fontName="Helvetica-Bold",
            alignment=TA_CENTER
        ),
        "FooterNote": ParagraphStyle(
            "FooterNote", parent=base["Normal"],
            fontSize=7.5, textColor=colors.HexColor("#888888"),
            alignment=TA_CENTER
        ),
    }
    return custom


# ── Helpers ──────────────────────────────────────────────────────────────────
def kv_table(rows: list[tuple], styles: dict) -> Table:
    """Renders a two-column key-value table."""
    data = [
        [Paragraph(k, styles["FieldLabel"]),
         Paragraph(str(v), styles["FieldValue"])]
        for k, v in rows
    ]
    t = Table(data, colWidths=[4.5 * cm, 12 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, LIGHT_BLUE]),
    ]))
    return t


def header_block(title: str, subtitle: str, styles: dict) -> list:
    """Blue banner header."""
    banner = Table(
        [[Paragraph(title, styles["DocTitle"])],
         [Paragraph(subtitle, styles["DocSubtitle"])]],
        colWidths=[17 * cm]
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    return [banner, Spacer(1, 0.4 * cm)]


def section_heading(text: str, styles: dict) -> list:
    rule = HRFlowable(width="100%", thickness=1.5, color=MID_BLUE, spaceAfter=4)
    return [Paragraph(text, styles["SectionHeading"]), rule]


def parse_books(signed_text_b64: str) -> list[dict]:
    """Decode base64 → XML → list of book dicts."""
    # Fix padding if needed
    pad = len(signed_text_b64) % 4
    if pad:
        signed_text_b64 += "=" * (4 - pad)
    xml_bytes = base64.b64decode(signed_text_b64)
    raw = xml_bytes.decode("utf-8", errors="replace")

    # Strip XML-DSig <Signature> block so only book elements remain
    sig_idx = raw.find("<Signature ")
    if sig_idx != -1:
        raw = raw[:sig_idx] + "</catalog>"

    # Ensure root element is closed
    if not raw.strip().endswith("</catalog>"):
        # Forcefully close any open book tag, then catalog
        if raw.rfind("</book>") < raw.rfind("<book"):
            raw += "</book>"
        raw += "</catalog>"

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        # Fallback: wrap fragment and try again
        raw_inner = raw.replace('<?xml version="1.0"?>', "")
        raw_inner = raw_inner.replace("<catalog>", "").replace("</catalog>", "")
        root = ET.fromstring(f"<catalog>{raw_inner}</catalog>")

    books = []
    for book in root.findall("book"):
        books.append({
            "id":           book.get("id", ""),
            "author":       book.findtext("author", ""),
            "title":        book.findtext("title", ""),
            "genre":        book.findtext("genre", ""),
            "price":        book.findtext("price", ""),
            "publish_date": book.findtext("publish_date", ""),
            "description":  " ".join((book.findtext("description", "") or "").split()),
        })
    return books


# ── Page decorators ──────────────────────────────────────────────────────────
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"Page {doc.page}")
    canvas.setStrokeColor(colors.HexColor("#CCCCCC"))
    canvas.line(2 * cm, 1.6 * cm, A4[0] - 2 * cm, 1.6 * cm)
    canvas.restoreState()


# ── Main builder ─────────────────────────────────────────────────────────────
def build_pdf(output_path: str = "output.pdf"):
    data  = json.loads(RAW_JSON)
    cert  = data["siginedCertificate"]
    fp    = data["fingerPrint"]
    status = "VALID" if data.get("status") == "1" else "INVALID"
    books = parse_books(data["signedText"])

    styles = build_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.5 * cm,
    )

    story = []

    # ── Cover header ────────────────────────────────────────────────────────
    story += header_block(
        "Digital Signature Certificate Report",
        "Capricorn CA 2014  |  Class 3 Organisation Certificate",
        styles
    )

    # ── Certificate status badge ────────────────────────────────────────────
    status_color = GREEN if status == "VALID" else colors.red
    badge = Table([[Paragraph(f"Certificate Status: {status}", ParagraphStyle(
        "badge", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
        alignment=TA_CENTER
    ))]],  colWidths=[17 * cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), status_color),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(badge)
    story.append(Spacer(1, 0.5 * cm))

    # ── Certificate identity ─────────────────────────────────────────────────
    story += section_heading("1.  Certificate Identity", styles)
    story.append(kv_table([
        ("Common Name",    cert["commonName"]),
        ("Serial Number",  cert["serialNumber"]),
        ("Label",          cert["label"]),
        ("Issuer",         cert["issuerName"]),
        ("Valid From",     cert["validFrom"]),
        ("Valid Until",    cert["validTill"]),
    ], styles))
    story.append(Spacer(1, 0.4 * cm))

    # ── Subject details ──────────────────────────────────────────────────────
    story += section_heading("2.  Subject / Organisation Details", styles)
    subject_parts = {}
    for part in cert.get("subject", "").split(","):
        if "=" in part:
            k, _, v = part.partition("=")
            subject_parts[k.strip()] = v.strip()

    subject_rows = [
        ("Country (C)",       subject_parts.get("C", "")),
        ("Organisation (O)",  subject_parts.get("O", "")),
        ("Dept / Unit (OU)",  subject_parts.get("OU", "")),
        ("State (ST)",        subject_parts.get("ST", "")),
        ("Postal Code",       subject_parts.get("PostalCode", "")),
    ]
    story.append(kv_table(subject_rows, styles))
    story.append(Spacer(1, 0.4 * cm))

    # ── Key & hardware info ──────────────────────────────────────────────────
    story += section_heading("3.  Key & Hardware Token Information", styles)
    story.append(kv_table([
        ("Key Store ID",       cert["keyStoreID"]),
        ("Key Store Name",     cert["keyStoreName"]),
        ("Key Store Display",  cert["keyStoreDisplayName"]),
        ("Subject Key ID",     cert["subjectKeyIdentifierString"]),
        ("Key ID (truncated)", cert["keyId"][:40] + "…"),
    ], styles))
    story.append(Spacer(1, 0.4 * cm))

    # ── Fingerprint ──────────────────────────────────────────────────────────
    story += section_heading("4.  Document Fingerprint (SHA-256)", styles)
    story.append(kv_table([("Fingerprint", fp)], styles))
    story.append(Spacer(1, 0.4 * cm))

    # ── Book catalogue (new page) ─────────────────────────────────────────────
    story.append(PageBreak())
    story += header_block("Signed Book Catalogue", "Extracted from the Digitally Signed XML Payload", styles)

    # Summary table
    summary_data = [["#", "Book ID", "Title", "Author", "Genre", "Price ($)"]]
    for i, b in enumerate(books, 1):
        summary_data.append([
            str(i), b["id"], b["title"][:28],
            b["author"], b["genre"], b["price"]
        ])

    summary_table = Table(
        summary_data,
        colWidths=[0.8*cm, 1.4*cm, 5.5*cm, 4*cm, 2.2*cm, 1.8*cm],
        repeatRows=1
    )
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  9),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8.5),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BLUE]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.6 * cm))

    # Detailed book cards
    story += section_heading("Book Descriptions", styles)
    for b in books:
        card_data = [[
            Paragraph(f"{b['id']}  –  {b['title']}", styles["BookTitle"]),
            Paragraph(f"<b>{b['genre']}</b>  |  ${b['price']}  |  {b['publish_date']}", styles["BookBody"]),
        ]]
        card_data.append([
            Paragraph(f"Author: {b['author']}", styles["BookBody"]),
            Paragraph(b["description"], styles["BookBody"]),
        ])
        card = Table(card_data, colWidths=[5.5 * cm, 11.2 * cm])
        card.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, 0),  LIGHT_BLUE),
            ("GRID",         (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
            ("SPAN",         (0, 0), (0, 0)),   # no span — just layout
        ]))
        story.append(card)
        story.append(Spacer(1, 0.2 * cm))

    # ── Footer note ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC")))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "This PDF was auto-generated from a digitally signed XML payload. "
        "Certificate issued by Capricorn Identity Services Pvt Ltd, India.",
        styles["FooterNote"]
    ))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"[✓] PDF saved → {output_path}")


if __name__ == "__main__":
    build_pdf("output.pdf")
