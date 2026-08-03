#!/usr/bin/env python3
"""Fill official NIW form PDFs from a case answers file. Standalone.

Usage:
    pip install pypdf cryptography          # one-time
    python3 fill_form.py <answers.json> <form> [blank_dir] [out_dir]

<form>: i-140 | eta-9089-appendix-a | eta-9089-final-determination | g-1145 | all
<answers.json>: flat semantic keys — see the "forms" reference for the full
key list. Example:
    {
      "beneficiary.family_name": "DOE", "beneficiary.given_name": "JANE",
      "mailing.street": "1 Main St", "mailing.city": "...", "mailing.state": "CA",
      "employment.job_title": "Research Scientist", "employment.soc_code": "15-2051",
      "degrees": [{"level": "master", "field": "...", "institution": "...",
                    "country": "...", "month_year": "06/2023"}],
      "current_employer": {"name": "...", "duties": "..."},
      "family": [{"family_name": "...", "given_name": "...", "dob": "...",
                   "country_of_birth": "...", "relationship": "Spouse"}]
    }

Unfilled/unmatched fields are reported — nothing is silently dropped.
"""
import io
import json
import pathlib
import sys
from typing import Any

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Missing dependency. Run:  pip install pypdf cryptography")
    raise SystemExit(2)

A = dict[str, Any]


# --- BEGIN SYNC: fill maps (source of truth: src/openniw/services/formfill.py) ---
def _yn(v: Any) -> bool:
    return v in (True, "true", "yes", "Yes", "Y", "1", 1)


# ---------------------------------------------------------------------------
# Per-form mappings: field-name suffix -> callable(answers) -> value | None.
# Text fields get strings; checkbox fields get True (their "on" state is
# resolved from the PDF) or None to leave untouched.
# ---------------------------------------------------------------------------

def _i140(a: A) -> dict[str, Any]:
    m: dict[str, Any] = {
        # Part 1 — petitioner (= the beneficiary, self-petition)
        "Pt1Line1a_FamilyName[0]": a.get("beneficiary.family_name"),
        "Pt1Line1b_GivenName[0]": a.get("beneficiary.given_name"),
        "Pt1Line1c_MiddleName[0]": a.get("beneficiary.middle_name"),
        "Line6b_StreetNumberName[0]": a.get("mailing.street"),
        "Line6c_AptSteFlrNumber[0]": a.get("mailing.apt"),
        "Line6d_CityOrTown[0]": a.get("mailing.city"),
        "Line6e_State[0]": a.get("mailing.state"),
        "Line6f_ZipCode[0]": a.get("mailing.zip"),
        "Line6h_Province[0]": a.get("mailing.province"),
        "Line6g_PostalCode[0]": a.get("mailing.postal_code"),
        "Line6i_Country[0]": a.get("mailing.country", "United States"),
        "Line7_SSN[0]": a.get("beneficiary.ssn"),
        "Pt1Line8_USCISOnlineActNumber[0]": a.get("beneficiary.uscis_account"),
        # Asylum Program Fee: individual self-petitioners answer these
        "P1_Line5_Checkbox[0]": True if not _yn(a.get("petitioner.nonprofit")) else None,
        "P1_Line5_Checkbox[1]": True if _yn(a.get("petitioner.nonprofit")) else None,
        "P1_Line6_Checkbox[1]": True if _yn(a.get("petitioner.small_employer", True)) else None,
        "P1_Line6_Checkbox[0]": True if not _yn(a.get("petitioner.small_employer", True)) else None,
        # Part 2 — petition type box 1.h: NIW (advanced degree / exceptional ability)
        "prt2PetitionType[6]": True,
        # Part 3 — beneficiary
        "Pt3Line1a_FamilyName[0]": a.get("beneficiary.family_name"),
        "Pt3Line1b_GivenName[0]": a.get("beneficiary.given_name"),
        "Pt3Line1c_MiddleName[0]": a.get("beneficiary.middle_name"),
        "Line2b_StreetNumberName[0]": a.get("mailing.street"),
        "Line2c_AptSteFlrNumber[0]": a.get("mailing.apt"),
        "Line2d_CityOrTown[0]": a.get("mailing.city"),
        "Line2e_State[0]": a.get("mailing.state"),
        "Line2f_ZipCode[0]": a.get("mailing.zip"),
        "Line2h_Province[0]": a.get("mailing.province"),
        "Line2g_PostalCode[0]": a.get("mailing.postal_code"),
        "Line2i_Country[0]": a.get("mailing.country", "United States"),
        "Line5_DateOfBirth[0]": a.get("beneficiary.dob"),
        "Line6_CityTownOfBirth[0]": a.get("beneficiary.city_of_birth"),
        "Line7_StateProvinceOfBirth[0]": a.get("beneficiary.state_of_birth"),
        "Line8_Country[0]": a.get("beneficiary.country_of_birth"),
        "Line9_Country[0]": a.get("beneficiary.citizenship"),
        "Pt3Line8_AlienNumber[0]": a.get("beneficiary.a_number"),
        "Line12_SSN[0]": a.get("beneficiary.ssn"),
    }
    if _yn(a.get("us_presence.in_us")):
        m.update({
            "Line13_DateOArrival[0]": a.get("us_presence.date_of_arrival"),
            "Line14a_ArrivalDeparture[0]": a.get("us_presence.i94_number"),
            "Line14b_Passport[0]": a.get("us_presence.passport_number"),
            "Line14c_TravelDoc[0]": a.get("us_presence.travel_doc_number"),
            "Line14d_CountryOfIssuance[0]": a.get("us_presence.passport_country"),
            "Line14e_ExpDate[0]": a.get("us_presence.passport_exp"),
            "Line15_CurrentNon[0]": a.get("us_presence.current_status"),
        })
    # Part 4 — processing: consular vs adjustment
    if _yn(a.get("processing.adjustment")):
        m["Line1b_Status[0]"] = True
        m["Line1b_Country[0]"] = a.get("processing.country_of_residence")
    elif a.get("processing.consulate_city"):
        m["Line1a_Visa[0]"] = True
        m["Line1a_CityorTown[0]"] = a.get("processing.consulate_city")
        m["Line1a_Country[0]"] = a.get("processing.consulate_country")
    m.update({
        "Line2a_StreetNumberName[0]": a.get("foreign_address.street"),
        "Line2c_CityOrTown[0]": a.get("foreign_address.city"),
        "Line2e_Province[0]": a.get("foreign_address.province"),
        "Line2d_PostalCode[0]": a.get("foreign_address.postal_code"),
        "Line2f_Country[0]": a.get("foreign_address.country"),
        "Line3a_FamilyName2[0]": a.get("native_name.family"),
        "Line3b_GivenName2[0]": a.get("native_name.given"),
        "Line3c_MiddleName2[0]": a.get("native_name.middle"),
        # Part 4 items 5-8 (prior petitions / proceedings): default No
        "Line5_No[0]": True if not _yn(a.get("processing.prior_petition")) else None,
        "Line5_Yes[0]": True if _yn(a.get("processing.prior_petition")) else None,
        "Line6_No[0]": True if not _yn(a.get("processing.in_proceedings")) else None,
        "Line6_Yes[0]": True if _yn(a.get("processing.in_proceedings")) else None,
        # Part 5 — petitioner type: Self
        "Line1b_Self[0]": True,
        "Line3a_Occupation[0]": a.get("petitioner.occupation"),
        "Line3b_AnnualIncome[0]": a.get("petitioner.annual_income"),
        # Part 6 — proposed employment
        "Line1_JobTitle[0]": a.get("employment.job_title"),
        "Line2_SOCCode1[0]": (a.get("employment.soc_code") or "")[:2] or None,
        "Line2_SOCCode2[0]": (a.get("employment.soc_code") or "").replace("-", "")[2:6] or None,
        "Line3_JobDescription[0]": a.get("employment.job_description"),
        "Line4_Yes1[0]": True if _yn(a.get("employment.full_time", True)) else None,
        "Line4_No1[0]": True if not _yn(a.get("employment.full_time", True)) else None,
        "Line5_Hours[0]": a.get("employment.hours"),
        "Line6_Yes1[0]": True if _yn(a.get("employment.permanent", True)) else None,
        "Line6_No1[0]": True if not _yn(a.get("employment.permanent", True)) else None,
        "Line7_Yes1[0]": True if _yn(a.get("employment.new_position", True)) else None,
        "Line7_No1[0]": True if not _yn(a.get("employment.new_position", True)) else None,
        "Line8_Wages[0]": a.get("employment.wages"),
        "Line8_Per[0]": a.get("employment.wages_per"),
        # Part 8 — petitioner contact + signature date (signature itself is wet-ink)
        "Part7_Item3a_FamilyName[0]": a.get("beneficiary.family_name"),
        "Part7_Item3b_GivenName[0]": a.get("beneficiary.given_name"),
        "Part7_Item4_Title[0]": "Self-petitioner",
        "Part7_Item5_DayPhone[0]": a.get("contact.daytime_phone"),
        "Part7_Item6_MobilePhone[0]": a.get("contact.mobile_phone"),
        "Part7_Item7_Email[0]": a.get("contact.email"),
    })
    # Part 7 — spouse and children (up to 2 in v1; more via Part 11 addendum)
    family = a.get("family") or []
    if len(family) > 0:
        p = family[0]
        m.update({
            "Line1a_Person1FamilyName[0]": p.get("family_name"),
            "Line1b_Person1GivenName[0]": p.get("given_name"),
            "Line1c_Person1MiddleName[0]": p.get("middle_name"),
            "Line1d_Person1DateOfBirth[0]": p.get("dob"),
            "Line1e_CountryOfBirth[0]": p.get("country_of_birth"),
            "Line1f_Relationship[0]": p.get("relationship"),
        })
    # family[1:6] (Persons Two..Six) use scrambled widget indices on the
    # official PDF and are resolved by field label in fill() below.
    return m


_PERSON_ORDINALS = ["Person Two", "Person Three", "Person Four", "Person Five",
                    "Person Six"]
_FAMILY_ATTRS = [
    ("Family Name", "family_name"),
    ("Given Name", "given_name"),
    ("Middle Name", "middle_name"),
    ("Date of Birth", "dob"),
    ("Country of Birth", "country_of_birth"),
    ("Relationship", "relationship"),
]


def _family_by_label(answers: A, fields: dict) -> tuple[dict[str, str], int]:
    """Match family[1:] to I-140 Part 7 Persons Two..Six via /TU labels."""
    family = answers.get("family") or []
    updates: dict[str, str] = {}
    for i, person in enumerate(family[1:6]):
        ordinal = _PERSON_ORDINALS[i]
        for label_key, answer_key in _FAMILY_ATTRS:
            value = person.get(answer_key)
            if not value:
                continue
            for full_name, f in fields.items():
                label = str(f.get("/TU") or "")
                if ordinal in label and label_key in label and f.get("/FT") == "/Tx":
                    updates[full_name] = str(value)
                    break
    return updates, max(0, len(family) - 6)


_DEGREE_BOXES = {
    "highschool": "High SchoolGED",
    "associate": "Associate",
    "bachelor": "Bachelors",
    "master": "Masters",
    "doctorate": "Doctorate PhD",
    "other": "Other degree JD MD etc",
}


def _appendix_a(a: A) -> dict[str, Any]:
    m: dict[str, Any] = {
        "1  Foreign Workers Last family Name": a.get("beneficiary.family_name"),
        "2  Foreign Workers First given Name": a.get("beneficiary.given_name"),
        "3  Foreign Workers Middle Names": a.get("beneficiary.middle_name"),
        "4  Address 1 current": a.get("mailing.street"),
        "5  Address 2 apartmentsuitefloor and number": a.get("mailing.apt"),
        "6  City": a.get("mailing.city"),
        "7  State": a.get("mailing.state"),
        "8  Postal Code": a.get("mailing.zip") or a.get("mailing.postal_code"),
        "9  Country": a.get("mailing.country", "United States"),
        "10  Province": a.get("mailing.province"),
        "11  Date of Birth mmddyyyy": a.get("beneficiary.dob"),
        "12  Class of admission": a.get("us_presence.current_status"),
        "13  Alien registration number A if applicable": a.get("beneficiary.a_number") or "N/A",
        "14  Country of birth": a.get("beneficiary.country_of_birth"),
        "15  Country of citizenship or nationality": a.get("beneficiary.citizenship"),
    }
    degrees = a.get("degrees") or []
    for i, d in enumerate(degrees[:5]):
        sfx = "" if i == 0 else f"_{i + 1}"
        level = str(d.get("level", "")).lower()
        box = _DEGREE_BOXES.get(level)
        if box:
            # blocks 4-5 rename Associate/Master and restart their suffixes
            if i >= 3 and level == "associate":
                m["Associates" if i == 3 else "Associates_2"] = True
            elif i >= 3 and level == "master":
                m["Master" if i == 3 else "Master_2"] = True
            else:
                m[f"{box}{sfx}"] = True
        if level == "other" and d.get("other_label"):
            m["1a If Other degree in question 1 specify the diplomadegree "
              "attained" + sfx] = d.get("other_label")
        m[f"1c  Name of institution that issued the degreediploma{sfx}"] = d.get("institution")
        m[f"1d  Name of country of institution identified in question 1c{sfx}"] = d.get("country")
        m[f"1e  Monthyear attained mmyyyy{sfx}"] = d.get("month_year")
        m[
            "1b  Specify majors andor fields of study may list more than one "
            "related major and more than one field" + sfx
        ] = d.get("field")
    emp = a.get("current_employer") or {}
    if emp.get("name"):
        m.update({
            "1 Employer name": emp.get("name"),
            "1a  Address 1": emp.get("address1"),
            "1b  Address 2": emp.get("address2"),
            "1c  City or town": emp.get("city"),
            "1d  Postal code": emp.get("postal_code"),
            "1e  Country": emp.get("country"),
            "1f  State territory or province": emp.get("state"),
            "1g  Job title": emp.get("job_title"),
            "1h  Start date mmyyyy": emp.get("start"),
            "1i  End date mmyyyy": emp.get("end"),
            "1k  Hours worked per week": emp.get("hours_per_week"),
        })
        m[
            "1l Job duties Specify details of job work tasks performed use of "
            "toolsequipment supervision etc up to 3500 characters"
        ] = emp.get("duties")
    return m


def _final_determination(a: A) -> dict[str, Any]:
    # NIW: DOL never processes this page; USCIS wants it attached with the
    # worker identified and signed by BOTH the petitioner and the
    # beneficiary (same person when self-petitioning). DOL-only fields and
    # the attorney block stay blank; signatures and sign-dates are wet-ink
    # on signing day (they surface in the required_unfilled report).
    return {
        "5  Foreign Workers Last family Name": a.get("beneficiary.family_name"),
        "6  Foreign Workers First given Name": a.get("beneficiary.given_name"),
        "7  Foreign Workers Middle Names": a.get("beneficiary.middle_name"),
        "8  Job Title": a.get("employment.job_title"),
        "9  SOC Code": a.get("employment.soc_code"),
        "10 SOC Occupational Title": a.get("employment.soc_title"),
        # Employer/petitioner declaration block (self-petitioner = beneficiary)
        "1 Last family Name": a.get("beneficiary.family_name"),
        "2 First given Name_2": a.get("beneficiary.given_name"),
        "3 Middle Initial_2": (a.get("beneficiary.middle_name") or "")[:1] or None,
        "4 Title": "Self-petitioner",
    }


def _g1145(a: A) -> dict[str, Any]:
    return {
        "LastName[0]": a.get("beneficiary.family_name"),
        "FirstName[0]": a.get("beneficiary.given_name"),
        "MiddleName[0]": a.get("beneficiary.middle_name"),
        "Email[0]": a.get("contact.email"),
        "MobilePhoneNumber[0]": a.get("contact.mobile_phone"),
    }

# --- END SYNC: fill maps ---

FORMS = {
    "i-140": ("i-140.pdf", _i140),
    "eta-9089-appendix-a": ("ETA-9089-Appendix-A.pdf", _appendix_a),
    "eta-9089-final-determination": ("ETA-9089-Final-Determination.pdf", _final_determination),
    "g-1145": ("g-1145.pdf", _g1145),
}


def fill(form_code: str, answers: A, blank_dir: pathlib.Path,
         out_dir: pathlib.Path) -> dict:
    src, builder = FORMS[form_code]
    src_path = blank_dir / src
    if not src_path.exists():
        return {"error": f"{src_path} not found — run fetch_forms.py first"}
    reader = PdfReader(str(src_path))
    writer = PdfWriter()
    writer.append(reader)

    fields = reader.get_fields() or {}
    by_suffix: dict[str, tuple[str, Any]] = {}
    for full_name, f in fields.items():
        by_suffix[full_name.split(".")[-1]] = (full_name, f)
        by_suffix.setdefault(full_name, (full_name, f))

    wanted = {k: v for k, v in builder(answers).items() if v not in (None, "")}
    updates: dict[str, str] = {}
    unmatched: list[str] = []
    warnings: list[str] = []
    for suffix, value in wanted.items():
        hit = by_suffix.get(suffix)
        if hit is None:
            unmatched.append(suffix)
            continue
        full_name, f = hit
        if f.get("/FT") == "/Btn":
            states = [s for s in (f.get("/_States_") or []) if s != "/Off"]
            if value is True and states:
                updates[full_name] = states[0]
        else:
            updates[full_name] = str(value)

    if form_code == "i-140":
        # Persons Two..Six are matched by field label (scrambled widget indices).
        fam_updates, overflow = _family_by_label(answers, fields)
        updates.update(fam_updates)
        if overflow:
            warnings.append(
                f"{overflow} family member(s) beyond six do not fit Part 7 — "
                "list them in Part 11 (Additional Information) by hand."
            )

    for page in writer.pages:
        writer.update_page_form_field_values(page, updates, auto_regenerate=False)
    try:
        writer.set_need_appearances_writer(True)
    except Exception:
        pass
    # USCIS PDFs are XFA hybrids: Adobe renders from the XFA layer, which we
    # cannot write, so a filled AcroForm can display as BLANK in Acrobat.
    # Dropping the XFA key forces every viewer to render the filled AcroForm.
    try:
        acro = writer._root_object.get("/AcroForm")
        if acro is not None:
            acro = acro.get_object()
            if "/XFA" in acro:
                del acro["/XFA"]
    except Exception:
        pass

    # Required-flagged PDF fields still blank after the fill — surface what
    # each one needs instead of shipping silent blanks.
    required_unfilled: list[dict[str, str]] = []
    seen_req: set[tuple[str, str]] = set()
    for full_name, f in fields.items():
        if not (int(f.get("/Ff") or 0) & 2):
            continue
        if updates.get(full_name):
            continue
        label = str(f.get("/TU") or full_name.split(".")[-1]).strip()
        low = label.lower()
        if "signature" in low:
            action = "sign by hand in black ink on signing day"
        elif "date signed" in low:
            action = "write the date by hand when you sign"
        elif "attorney" in low or "agent" in low or "firm" in low:
            action = "leave blank unless an attorney represents you"
        else:
            action = "complete by hand"
        key = (label, action)
        if key in seen_req:
            continue
        seen_req.add(key)
        required_unfilled.append({"field": label, "action": action})

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{form_code}-filled.pdf"
    buf = io.BytesIO()
    writer.write(buf)
    out_path.write_bytes(buf.getvalue())
    return {"output": str(out_path), "filled": len(updates),
            "unmatched": unmatched, "warnings": warnings,
            "required_unfilled": required_unfilled}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    answers = json.loads(pathlib.Path(sys.argv[1]).read_text())
    form = sys.argv[2]
    blank_dir = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else "forms/blank")
    out_dir = pathlib.Path(sys.argv[4] if len(sys.argv) > 4 else "forms")
    codes = list(FORMS) if form == "all" else [form]
    ok = True
    for code in codes:
        if code not in FORMS:
            print(f"unknown form: {code} (choose from {list(FORMS)})")
            return 2
        report = fill(code, answers, blank_dir, out_dir)
        if "error" in report:
            ok = False
            print(f"{code}: ERROR {report['error']}")
        else:
            note = f", unmatched: {report['unmatched']}" if report["unmatched"] else ""
            print(f"{code}: {report['filled']} fields -> {report['output']}{note}")
            for w in report.get("warnings", []):
                print(f"  WARNING: {w}")
    print("\nAlways PRINT the filled PDFs and visually verify every page "
          "before signing — do not trust one on-screen viewer.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
