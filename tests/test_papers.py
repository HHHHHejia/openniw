import json

from openniw.services import papers


def test_slug():
    assert papers._slug("Attention Is All You Need!", 2017) == \
        "2017-attention-is-all-you-need"
    assert papers._slug("", None) == "nd-paper"


def test_oa_candidates_prefers_published():
    work = {
        "best_oa_location": {"pdf_url": "http://a/arxiv.pdf",
                             "version": "submittedVersion"},
        "locations": [
            {"pdf_url": "http://b/published.pdf",
             "version": "publishedVersion"},
            {"pdf_url": "http://a/arxiv.pdf", "version": "submittedVersion"},
        ],
    }
    cands = papers._oa_candidates(work)
    assert cands[0]["version"] == "publishedVersion"


def test_download_papers_manifest_and_flags(tmp_path, monkeypatch):
    fake_work = {
        "display_name": "A Great Paper on Things",
        "doi": "https://doi.org/10.1/x",
        "publication_year": 2024,
        "primary_location": {"source": {"display_name": "NeurIPS"}},
        "best_oa_location": {"pdf_url": "http://x/preprint.pdf",
                             "version": "submittedVersion"},
        "locations": [],
    }
    monkeypatch.setattr(papers, "_get",
                        lambda path, **kw: {"results": [fake_work]})
    monkeypatch.setattr(papers, "_download_pdf",
                        lambda url, dest: (dest.write_bytes(b"%PDF-fake"),
                                           True)[1])
    out = tmp_path / "sources" / "papers"
    summary = papers.download_papers(["A Great Paper on Things"], out,
                                     log=lambda *_: None)
    assert summary["downloaded"] == 1
    assert summary["preprint_only"] == 1  # submittedVersion -> flag
    manifest = json.loads((out / "manifest.json").read_text())
    assert manifest[0]["file"] == "2024-a-great-paper-on-things.pdf"
    assert (out / manifest[0]["file"]).exists()

    # idempotent: second run skips
    summary2 = papers.download_papers(["A Great Paper on Things"], out,
                                      log=lambda *_: None)
    assert summary2["downloaded"] == 1


def test_unresolved_title(tmp_path, monkeypatch):
    monkeypatch.setattr(papers, "_get", lambda path, **kw: {"results": []})
    out = tmp_path / "p"
    summary = papers.download_papers(["Nonexistent gibberish title"], out,
                                     log=lambda *_: None)
    assert summary["unresolved"] == 1 and summary["downloaded"] == 0
