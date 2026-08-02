import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]


def test_benchmark_inputs_roundtrip(client, case_dir):
    r = client.get("/api/benchmark/inputs").json()
    assert r["inputs"] == {} and r["version"] == 0
    payload = {"category": "NIW", "field": "Computer Science & AI",
               "citations": 350,
               "computed": {"percentile_among_approved": 62, "sample_n": 512}}
    ok = client.put("/api/benchmark/inputs", json={"inputs": payload})
    assert ok.status_code == 200
    again = client.get("/api/benchmark/inputs").json()
    assert again["inputs"]["computed"]["percentile_among_approved"] == 62
    assert (case_dir / "benchmark.json").exists()


def test_benchmark_dataset_shape():
    p = REPO / "frontend" / "public" / "benchmark-data.json"
    assert p.exists(), "run scripts/export_benchmark.py"
    d = json.loads(p.read_text())
    assert d["columns"] == ["ym", "category", "field",
                            "citations", "publications"]
    assert len(d["cases"]) > 7000
    assert "NIW" in d["categories"]
    assert "survivor" in d["source"].lower() or "Approved" in d["source"]
    # de-identified: rows are pure numbers
    assert all(isinstance(v, int) for v in d["cases"][0])
    # no raw narrative fields anywhere
    assert set(d.keys()) == {"generated", "source", "ym0", "categories",
                             "fields", "columns", "cases"}


def test_benchmark_step_registered():
    from openniw import ui_session
    from openniw.cli import STEPS
    assert "benchmark" in STEPS
    assert ui_session.FILES_OWNED["benchmark"] == ["benchmark.json"]
