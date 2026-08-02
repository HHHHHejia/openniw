import io


def test_intake_roundtrip(client, case_dir):
    r = client.get("/api/intake").json()
    assert r["intake"] == {} and r["files"] == []
    payload = {"links": {"scholar_url": "https://scholar.google.com/x"},
               "basics": {"position": "Postdoc", "degree": "PhD",
                          "field": "ML", "in_us": True}}
    ok = client.put("/api/intake", json={"intake": payload})
    assert ok.status_code == 200
    again = client.get("/api/intake").json()
    assert again["intake"]["basics"]["degree"] == "PhD"
    assert (case_dir / "intake.json").exists()


def test_upload_lands_in_sources(client, case_dir):
    r = client.post("/api/intake/upload",
                    files={"file": ("My CV (final).pdf",
                                    io.BytesIO(b"%PDF-cv"), "application/pdf")})
    assert r.status_code == 200
    name = r.json()["name"]
    assert (case_dir / "sources" / name).read_bytes() == b"%PDF-cv"
    # second upload with the same name never clobbers
    r2 = client.post("/api/intake/upload",
                     files={"file": ("My CV (final).pdf",
                                     io.BytesIO(b"%PDF-v2"), "application/pdf")})
    assert r2.json()["name"] != name
    assert len(client.get("/api/intake").json()["files"]) == 2


def test_upload_rejects_traversal_and_empty(client, case_dir):
    r = client.post("/api/intake/upload",
                    files={"file": ("../../evil.sh", io.BytesIO(b"x"),
                                    "text/plain")})
    assert r.status_code == 200
    assert r.json()["name"] == "evil.sh"
    assert (case_dir / "sources" / "evil.sh").exists()
    assert not (case_dir.parent / "evil.sh").exists()
    bad = client.post("/api/intake/upload",
                      files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")})
    assert bad.status_code == 422


def test_intake_step_registered():
    from openniw import ui_session
    from openniw.cli import STEPS
    assert "intake" in STEPS
    assert "sources/*" in ui_session.FILES_OWNED["intake"]
