import zipfile
import io


def test_health_and_token_guard(client):
    assert client.get("/api/health").json()["ok"] is True
    bad = client.get("/api/health", headers={"X-OpenNIW-Token": "wrong"})
    assert bad.status_code == 403


def test_spec_has_filing_address_and_62_fields(client):
    spec = client.get("/api/forms/spec").json()
    keys = [f["key"] for s in spec["sections"] for f in s["fields"]]
    assert len(keys) == 62
    # premium=True + MA employer -> Elgin premium lockbox
    assert spec["filing_address"]["key"] == "elgin_premium"


def test_answers_roundtrip_and_409(client):
    got = client.get("/api/forms/answers").json()
    v = got["version"]
    body = {"answers": {**got["answers"], "beneficiary.ssn": "111111111"},
            "base_version": v, "edited_keys": ["beneficiary.ssn"]}
    ok = client.put("/api/forms/answers", json=body)
    assert ok.status_code == 200 and ok.json()["version"] >= v
    stale = client.put("/api/forms/answers", json=body)  # same old version
    assert stale.status_code == 409


def test_edited_keys_clear_ai_marks(client, case_dir):
    import json
    (case_dir / "forms" / "answers.meta.json").write_text(json.dumps(
        {"ai_keys": ["beneficiary.ssn", "employment.soc_code"]}))
    got = client.get("/api/forms/answers").json()
    client.put("/api/forms/answers", json={
        "answers": got["answers"], "base_version": got["version"],
        "edited_keys": ["beneficiary.ssn"]})
    meta = client.get("/api/forms/answers").json()["meta"]
    assert meta["ai_keys"] == ["employment.soc_code"]
    assert meta["edited_keys"] == ["beneficiary.ssn"]


def test_verified_keys_clear_ai_marks(client, case_dir):
    import json
    (case_dir / "forms" / "answers.meta.json").write_text(json.dumps(
        {"ai_keys": ["beneficiary.dob", "employment.soc_code"]}))
    got = client.get("/api/forms/answers").json()
    client.put("/api/forms/answers", json={
        "answers": got["answers"], "base_version": got["version"],
        "verified_keys": ["beneficiary.dob"]})
    meta = client.get("/api/forms/answers").json()["meta"]
    assert meta["ai_keys"] == ["employment.soc_code"]
    assert "beneficiary.dob" in meta["verified_keys"]


def test_fill_i140_and_pdf(client, case_dir):
    import pytest
    if not (case_dir / "forms" / "blank" / "i-140.pdf").exists():
        pytest.skip("vendored i-140.pdf missing")
    r = client.post("/api/forms/fill/i-140")
    assert r.status_code == 200
    report = r.json()["report"]
    assert report["filled"] > 30
    pdf = client.get("/api/forms/filled/i-140/pdf")
    assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")
    # XFA layer must be stripped so Adobe renders AcroForm values
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(pdf.content))
    acro = reader.trailer["/Root"].get("/AcroForm")
    assert acro is None or "/XFA" not in acro.get_object()
    fields = reader.get_fields()
    assert any((f.get("/V") or "") == "Doe" for f in fields.values())
    listed = client.get("/api/forms/filled").json()["filled"]
    assert any(f["form_code"] == "i-140" for f in listed)


def test_package_zip(client, case_dir):
    (case_dir / "documents").mkdir()
    (case_dir / "documents" / "pes.md").write_text("# PES\n\nHello.")
    r = client.get("/api/forms/package")
    assert r.status_code == 200
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    names = zf.namelist()
    assert "README.txt" in names
    assert "documents/pes.docx" in names
    readme = zf.read("README.txt").decode()
    assert "Premium I-140" in readme  # premium answers -> premium lockbox
    assert (case_dir / "package" / "openniw-package.zip").exists()


def test_citations_review_roundtrip(client, case_dir):
    import json
    (case_dir / "citations").mkdir()
    (case_dir / "citations" / "scored.json").write_text(json.dumps([
        {"key": "10.1/abc", "citing_title": "A study", "score": 7,
         "quote": "we build upon Doe et al."}]))
    r = client.get("/api/citations/review").json()
    assert r["scored"][0]["score"] == 7 and r["selection"] == {}
    ok = client.put("/api/citations/selection", json={
        "selection": {"10.1/abc": {"selected": True, "note": "great"}},
        "base_version": r["version"]})
    assert ok.status_code == 200
    again = client.get("/api/citations/review").json()
    assert again["selection"]["10.1/abc"]["selected"] is True
    stale = client.put("/api/citations/selection", json={
        "selection": {}, "base_version": r["version"]})
    assert stale.status_code == 409


def test_done_finalizes_sentinel(client, case_dir):
    r = client.post("/api/done", json={"summary": {"fields_edited": 4}})
    assert r.status_code == 200
    from openniw import ui_session
    from openniw.casefolder import CaseFolder
    code, sent = ui_session.status(CaseFolder(case_dir))
    assert code == ui_session.DONE
    assert sent["summary"]["fields_edited"] == 4
    assert "ai_keys_remaining" in sent["summary"]


def test_state_endpoint(client):
    st = client.get("/api/state").json()
    assert "Stage: IV Forms" in st["state_md"]
