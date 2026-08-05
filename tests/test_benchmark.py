import json
import importlib.util
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]


def _benchmark_export_module():
    path = REPO / "scripts" / "export_benchmark.py"
    spec = importlib.util.spec_from_file_location("export_benchmark", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_benchmark_inputs_roundtrip(client, case_dir):
    r = client.get("/api/benchmark/inputs").json()
    assert r["inputs"] == {} and r["version"] == "0"
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
    assert d["columns"] == ["ym", "category", "field", "citations",
                            "publications", "processing_days", "premium"]
    assert len(d["cases"]) > 7000
    assert "NIW" in d["categories"]
    assert "survivor" in d["source"].lower() or "Approved" in d["source"]
    # de-identified: rows are pure numbers
    assert all(isinstance(v, int) for v in d["cases"][0])
    # no raw narrative fields anywhere
    assert set(d.keys()) == {"generated", "source", "ym0", "categories",
                             "fields", "columns", "premium_codes",
                             "aggregates", "cases"}
    agg = d["aggregates"]
    assert agg["rfe_overcome_2024"]["rate"] > 0
    assert len(agg["weekly"]) > 0
    assert sum(agg["rec_letters_niw_hist"].values()) > 2000


def test_benchmark_field_classifier_uses_domain_boundaries():
    field_group = _benchmark_export_module().field_group
    expected = {
        "Artificial Intelligence": "Computer Science & AI",
        "AI": "Computer Science & AI",
        "Computational Modeling": "Computer Science & AI",
        "Hardware Designs": "Electrical & Electronics Eng.",
        "Flexible Radio-frequency Sensor Design": "Electrical & Electronics Eng.",
        "Industrial and Systems Engineering": "Mechanical & Aerospace Eng.",
        "Mechanism Design": "Mechanical & Aerospace Eng.",
        "Systems Design Engineering": "Mechanical & Aerospace Eng.",
        "Environmental Engineering": "Civil & Environmental Eng.",
        "Advanced Material Design": "Materials Science",
        "Ophthalmology": "Medicine & Health",
        "Bioengineering": "Life Sciences",
        "Virology": "Life Sciences",
        "Earth Science": "Earth & Geosciences",
        "Environmental Science": "Earth & Geosciences",
        "Nanophysics": "Physics & Astronomy",
        "Applied Microeconometrics": "Business, Economics & Finance",
        "Sports Science": "Arts, Design & Sports",
        "Design": "Arts, Design & Sports",
    }
    assert {raw: field_group(raw) for raw in expected} == expected
    assert field_group(None) == "Other fields"


def test_benchmark_step_registered():
    from openniw import ui_session
    from openniw.cli import STEPS
    assert "benchmark" in STEPS
    assert ui_session.FILES_OWNED["benchmark"] == ["benchmark.json"]
