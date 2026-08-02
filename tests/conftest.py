import json
import pathlib
import shutil
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))


FULL_ANSWERS = {
    "beneficiary.family_name": "Doe", "beneficiary.given_name": "Jane",
    "beneficiary.middle_name": "Q", "beneficiary.dob": "01/02/1990",
    "beneficiary.city_of_birth": "Springfield",
    "beneficiary.state_of_birth": "Hunan",
    "beneficiary.country_of_birth": "China",
    "beneficiary.citizenship": "China",
    "beneficiary.a_number": "123456789", "beneficiary.ssn": "987654321",
    "beneficiary.uscis_account": "111222333",
    "native_name.family": "杜", "native_name.given": "简", "native_name.middle": "",
    "mailing.street": "1 Main St", "mailing.apt": "2B",
    "mailing.city": "Boston", "mailing.state": "MA", "mailing.zip": "02110",
    "mailing.province": "", "mailing.postal_code": "", "mailing.country": "",
    "contact.daytime_phone": "6175550100",
    "contact.mobile_phone": "6175550101", "contact.email": "jane@example.org",
    "us_presence.in_us": True, "us_presence.date_of_arrival": "08/15/2019",
    "us_presence.i94_number": "94123456789",
    "us_presence.travel_doc_number": "",
    "us_presence.current_status": "F-1",
    "us_presence.passport_number": "E12345678",
    "us_presence.passport_country": "China",
    "us_presence.passport_exp": "12/31/2030",
    "processing.adjustment": True, "processing.premium": True,
    "processing.prior_petition": False, "processing.in_proceedings": False,
    "processing.country_of_residence": "United States",
    "processing.consulate_city": "", "processing.consulate_country": "",
    "foreign_address.street": "88 Renmin Rd", "foreign_address.city": "Changsha",
    "foreign_address.province": "Hunan", "foreign_address.postal_code": "410000",
    "foreign_address.country": "China",
    "employment.job_title": "Research Scientist",
    "employment.soc_code": "15-2051", "employment.soc_title": "Data Scientists",
    "employment.job_description": "Conducts machine learning research.",
    "employment.full_time": True, "employment.hours": "",
    "employment.permanent": True, "employment.new_position": False,
    "employment.wages": "150000", "employment.wages_per": "year",
    "petitioner.occupation": "Research Scientist",
    "petitioner.annual_income": "150000",
    "petitioner.nonprofit": False, "petitioner.small_employer": True,
    "degrees": [
        {"level": "doctorate", "field": "Computer Science",
         "institution": "MIT", "country": "United States",
         "month_year": "05/2024"},
        {"level": "other", "other_label": "Diploma",
         "field": "Music", "institution": "Juilliard",
         "country": "United States", "month_year": "05/2012"},
    ],
    "current_employer": {
        "name": "Acme Labs", "address1": "1 Acme Way", "address2": "",
        "city": "Boston", "state": "MA", "postal_code": "02110",
        "country": "United States", "job_title": "Research Scientist",
        "start": "06/2024", "end": "", "hours_per_week": "40",
        "duties": "Designs and evaluates machine learning models.",
    },
    "family": [
        {"family_name": "Doe", "given_name": "John", "middle_name": "",
         "dob": "03/04/1989", "country_of_birth": "China",
         "relationship": "Spouse"},
        {"family_name": "Doe", "given_name": "Jill", "middle_name": "",
         "dob": "05/06/2020", "country_of_birth": "United States",
         "relationship": "Child"},
    ],
}


@pytest.fixture
def case_dir(tmp_path):
    """A minimal case folder with blank forms linked from the repo vendored set."""
    (tmp_path / "forms" / "blank").mkdir(parents=True)
    vendored = {
        "i-140.pdf": REPO / "forms" / "uscis" / "i-140.pdf",
        "g-1145.pdf": REPO / "forms" / "uscis" / "g-1145.pdf",
        "ETA-9089-Appendix-A.pdf":
            REPO / "forms" / "dol" / "ETA-9089-Appendix-A.pdf",
        "ETA-9089-Final-Determination.pdf":
            REPO / "forms" / "dol" / "ETA-9089-Final-Determination.pdf",
    }
    for name, src in vendored.items():
        if src.exists():
            shutil.copy(src, tmp_path / "forms" / "blank" / name)
    (tmp_path / "forms" / "answers.json").write_text(
        json.dumps(FULL_ANSWERS))
    (tmp_path / "STATE.md").write_text("# Case state\nStage: IV Forms\n")
    (tmp_path / "case.json").write_text("{}")
    return tmp_path


@pytest.fixture
def client(case_dir):
    from fastapi.testclient import TestClient
    from openniw.server import create_app
    app = create_app(case_dir, token="testtoken", step="forms",
                     url="http://127.0.0.1:1/forms/?token=testtoken", port=1)
    return TestClient(app, headers={"X-OpenNIW-Token": "testtoken",
                                    "Host": "127.0.0.1"})
