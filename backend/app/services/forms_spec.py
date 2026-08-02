"""The forms wizard specification.

Sections/fields map 1:1 onto the semantic answer keys consumed by formfill.py.
Each field carries firm-practice help text ("why we ask") so the frontend can
render an informed wizard. AI pre-fills what it can from the case profile.
"""

WIZARD: list[dict] = [
    {
        "id": "beneficiary",
        "title": "Your identity",
        "fields": [
            {"key": "beneficiary.family_name", "label": "Family name (last name)",
             "type": "text", "required": True,
             "help": "Exactly as in your passport. This name flows to I-140, "
                     "ETA-9089 and later your green card."},
            {"key": "beneficiary.given_name", "label": "Given name (first name)",
             "type": "text", "required": True},
            {"key": "beneficiary.middle_name", "label": "Middle name", "type": "text"},
            {"key": "native_name.family", "label": "Family name in native alphabet",
             "type": "text",
             "help": "Only if your native alphabet is non-Roman (Chinese, Korean, "
                     "Cyrillic...)."},
            {"key": "native_name.given", "label": "Given name in native alphabet",
             "type": "text"},
            {"key": "beneficiary.dob", "label": "Date of birth (MM/DD/YYYY)",
             "type": "text", "required": True},
            {"key": "beneficiary.city_of_birth", "label": "City/town of birth",
             "type": "text", "required": True},
            {"key": "beneficiary.state_of_birth", "label": "State/province of birth",
             "type": "text"},
            {"key": "beneficiary.country_of_birth", "label": "Country of birth",
             "type": "text", "required": True,
             "help": "As on your birth certificate. Determines your visa-bulletin "
                     "chargeability."},
            {"key": "beneficiary.citizenship", "label": "Country of citizenship",
             "type": "text", "required": True},
            {"key": "beneficiary.a_number", "label": "A-Number (if any)",
             "type": "text",
             "help": "9 digits, no dashes. Found on prior USCIS approval notices "
                     "or EAD cards. Leave blank if you never had one."},
            {"key": "beneficiary.ssn", "label": "U.S. SSN (if any)", "type": "text"},
            {"key": "beneficiary.uscis_account",
             "label": "USCIS online account number (if any)", "type": "text"},
        ],
    },
    {
        "id": "contact",
        "title": "Mailing address & contact",
        "fields": [
            {"key": "mailing.street", "label": "Street number and name",
             "type": "text", "required": True,
             "help": "Your U.S. residence at time of filing. No P.O. boxes."},
            {"key": "mailing.apt", "label": "Apt/Ste/Flr number", "type": "text"},
            {"key": "mailing.city", "label": "City", "type": "text", "required": True},
            {"key": "mailing.state", "label": "State (2-letter)", "type": "text",
             "required": True},
            {"key": "mailing.zip", "label": "ZIP code", "type": "text",
             "required": True},
            {"key": "contact.daytime_phone", "label": "Daytime phone", "type": "text"},
            {"key": "contact.mobile_phone", "label": "Mobile phone", "type": "text",
             "required": True,
             "help": "Used on G-1145 for text notification when USCIS accepts "
                     "your package."},
            {"key": "contact.email", "label": "Email", "type": "text",
             "required": True},
        ],
    },
    {
        "id": "us_presence",
        "title": "U.S. immigration status",
        "fields": [
            {"key": "us_presence.in_us", "label": "Are you currently in the U.S.?",
             "type": "boolean", "required": True},
            {"key": "us_presence.date_of_arrival",
             "label": "Date of last arrival (MM/DD/YYYY)", "type": "text"},
            {"key": "us_presence.i94_number", "label": "I-94 number", "type": "text",
             "help": "Download your most recent I-94 from the CBP website."},
            {"key": "us_presence.current_status",
             "label": "Current nonimmigrant status (F-1, H-1B, O-1...)",
             "type": "text"},
            {"key": "us_presence.passport_number", "label": "Passport number",
             "type": "text"},
            {"key": "us_presence.passport_country",
             "label": "Passport country of issuance", "type": "text"},
            {"key": "us_presence.passport_exp",
             "label": "Passport expiration (MM/DD/YYYY)", "type": "text"},
            {"key": "processing.adjustment",
             "label": "Will you file I-485 adjustment of status in the U.S.?",
             "type": "boolean",
             "help": "If unsure between adjustment and consular processing, "
                     "answering consular is easier to change later than the "
                     "reverse. India/China-born applicants usually cannot file "
                     "I-485 concurrently due to visa retrogression."},
            {"key": "processing.premium",
             "label": "Request premium processing (Form I-907)?",
             "type": "boolean",
             "help": "Optional. USCIS decides within 45 business days for the "
                     "extra I-907 fee. Changes the mailing address (premium "
                     "lockbox) and adds I-907 to the package; the I-907 fee "
                     "needs its own payment form."},
            {"key": "processing.country_of_residence",
             "label": "Current country of residence", "type": "text"},
            {"key": "processing.consulate_city",
             "label": "If consular processing: consulate city", "type": "text"},
            {"key": "processing.consulate_country",
             "label": "If consular processing: consulate country", "type": "text"},
            {"key": "foreign_address.street", "label": "Foreign address: street",
             "type": "text", "required": True,
             "help": "Your address abroad (required on I-140 Part 4)."},
            {"key": "foreign_address.city", "label": "Foreign address: city",
             "type": "text"},
            {"key": "foreign_address.province", "label": "Foreign address: province",
             "type": "text"},
            {"key": "foreign_address.postal_code",
             "label": "Foreign address: postal code", "type": "text"},
            {"key": "foreign_address.country", "label": "Foreign address: country",
             "type": "text"},
        ],
    },
    {
        "id": "employment",
        "title": "Proposed employment",
        "fields": [
            {"key": "employment.job_title", "label": "Job title", "type": "text",
             "required": True,
             "help": "Your current position usually serves as the proposed "
                     "employment unless you plan to change jobs within 6 months."},
            {"key": "employment.soc_code", "label": "SOC code (e.g. 15-2051)",
             "type": "text", "required": True,
             "help": "Standard Occupational Classification — USCIS uses it at the "
                     "I-485 stage to verify you stayed in a 'same or similar' "
                     "field. Look yours up at onetonline.org."},
            {"key": "employment.soc_title", "label": "SOC occupational title",
             "type": "text"},
            {"key": "employment.job_description",
             "label": "Nontechnical job description", "type": "textarea",
             "required": True,
             "help": "Under 200 characters. Plain language; emphasize research "
                     "duties; do NOT name your employer, projects, or regions; "
                     "avoid teaching duties (officers rarely view teaching as "
                     "nationally important)."},
            {"key": "employment.full_time", "label": "Full-time position?",
             "type": "boolean", "default": True},
            {"key": "employment.permanent", "label": "Permanent position?",
             "type": "boolean", "default": True},
            {"key": "employment.new_position",
             "label": "New position (or hired < 6 months ago)?", "type": "boolean"},
            {"key": "employment.wages", "label": "Wages (amount)", "type": "text"},
            {"key": "employment.wages_per", "label": "Wages per (year/month/hour)",
             "type": "text", "default": "year"},
            {"key": "petitioner.occupation", "label": "Your occupation",
             "type": "text", "required": True,
             "help": "Not the same as job title — an occupation that reflects "
                     "your overall work and research (e.g. 'Research Scientist')."},
            {"key": "petitioner.annual_income", "label": "Annual income (USD)",
             "type": "text",
             "help": "Salary + cash bonus only; exclude stock, insurance, "
                     "tuition benefits."},
        ],
    },
    {
        "id": "education",
        "title": "Education (for ETA-9089 Appendix A)",
        "fields": [
            {"key": "degrees", "label": "Degrees", "type": "degree_list",
             "required": True,
             "help": "Highest first. Level is one of: doctorate, master, bachelor, "
                     "associate, other. Use the conferral date from your diploma; "
                     "if the transcript shows a Plan/Major, use that wording. "
                     "Foreign degrees need a NACES general evaluation as evidence."},
            {"key": "current_employer", "label": "Current employer",
             "type": "employer",
             "help": "Name, address, job title, start date (MM/YYYY), hours/week, "
                     "and 3-5 sentences of duties using action verbs. Do not "
                     "mention job title, employer name, advisor, or funding "
                     "sources inside the duties text."},
        ],
    },
    {
        "id": "family",
        "title": "Spouse & children",
        "fields": [
            {"key": "family", "label": "Family members", "type": "family_list",
             "help": "Spouse and all unmarried children under 21, whether or not "
                     "they immigrate with you. Each: names, date of birth, "
                     "country of birth, relationship."},
        ],
    },
]

FEES = {
    "i-140": 715,
    "asylum_program_fee_self": 300,
    "i-907_premium": 2965,
    "total_standard": 1015,
    "total_premium": 3980,
}

# Direct filing addresses for Form I-140 ("Direct Filing Addresses for Form
# I-140" at uscis.gov — state lists last verified 2026-08; they change, so the
# package README always tells the user to re-check just before mailing).
# Standard filing: Dallas or Chicago lockbox by state of intended employment.
# Premium (I-140 + I-907): Phoenix or Elgin lockbox. Concurrent I-140 + I-485
# without premium: Dallas "Attn: NFB" for every state.
_CHICAGO_STANDARD = {
    "CT", "DE", "DC", "IL", "IN", "IA", "KS", "ME", "MA", "MI", "MN", "MO",
    "NE", "NH", "NJ", "NY", "ND", "OH", "PA", "RI", "SD", "VT", "WI",
}
_PHOENIX_PREMIUM = {
    "AK", "AZ", "AR", "AA", "AE", "AP", "CA", "CO", "GA", "GU", "HI", "ID",
    "LA", "MH", "MT", "NV", "NM", "MP", "OK", "OR", "TX", "VI", "UT", "WA",
    "WY",
}

LOCKBOXES = {
    "dallas": {
        "name": "USCIS Dallas Lockbox",
        "usps": "USCIS\nAttn: I-140\nP.O. Box 660128\nDallas, TX 75266-0128",
        "courier": "USCIS\nAttn: I-140 (Box 660128)\n"
                   "2501 S. State Hwy. 121 Business\nSuite 400\n"
                   "Lewisville, TX 75067-8003",
    },
    "chicago": {
        "name": "USCIS Chicago Lockbox",
        "usps": "USCIS\nAttn: I-140\nP.O. Box 88774\nChicago, IL 60680-1774",
        "courier": "USCIS\nAttn: I-140 (Box 88774)\n"
                   "131 S. Dearborn St., 3rd Floor\nChicago, IL 60603-5517",
    },
    "dallas_nfb": {
        "name": "USCIS Dallas Lockbox (concurrent I-140 + I-485)",
        "usps": "USCIS\nAttn: NFB\nP.O. Box 660867\nDallas, TX 75266-0867",
        "courier": "USCIS\nAttn: NFB (Box 660867)\n"
                   "2501 S. State Highway 121 Business\nSuite 400\n"
                   "Lewisville, TX 75067-8003",
    },
    "phoenix_premium": {
        "name": "USCIS Phoenix Lockbox (premium)",
        "usps": "USCIS\nAttn: Premium I-140\nP.O. Box 21500\n"
                "Phoenix, AZ 85036-1500",
        "courier": "USCIS\nAttn: Premium I-140 (Box 21500)\n"
                   "2108 E. Elliot Rd.\nTempe, AZ 85284-1806",
    },
    "elgin_premium": {
        "name": "USCIS Elgin Lockbox (premium)",
        "usps": "USCIS\nAttn: Premium I-140\nP.O. Box 4008\n"
                "Carol Stream, IL 60197-4008",
        "courier": "USCIS\nAttn: Premium I-140 (Box 4008)\n"
                   "2500 Westfield Drive\nElgin, IL 60124-7836",
    },
}


def filing_address(state: str | None, premium: bool = False,
                   concurrent_i485: bool = False) -> dict:
    """Pick the USCIS lockbox for an I-140 mailing.

    `state` is the 2-letter state of intended employment. Returns the LOCKBOXES
    entry plus a `verified` note; falls back to the standard Dallas lockbox
    with a warning when the state is unknown.
    """
    st = (state or "").strip().upper()
    if premium:
        key = "phoenix_premium" if st in _PHOENIX_PREMIUM else "elgin_premium"
    elif concurrent_i485:
        key = "dallas_nfb"
    else:
        key = "chicago" if st in _CHICAGO_STANDARD else "dallas"
    out = dict(LOCKBOXES[key])
    out["key"] = key
    out["note"] = (
        "State lists last verified 2026-08. Always re-check the current "
        "address at uscis.gov (Direct Filing Addresses for Form I-140) just "
        "before mailing."
    )
    if not st:
        out["note"] = "No state on file — defaulted to the most common lockbox. " + out["note"]
    return out


LOCKBOX_NOTE = (
    "Mail the package to the USCIS lockbox for Form I-140 for your state — "
    "verify the current address at uscis.gov/i-140 (Direct Filing Addresses) "
    "just before mailing; addresses change, and premium (I-907) filings use a "
    "different lockbox. Payment must be electronic — G-1650 ACH (recommended) "
    "or G-1450 credit card (a declined card rejects the entire package) — or "
    "file Form G-1651 if you qualify for a paper-payment exemption. The I-907 "
    "premium fee needs its own payment form. USCIS recommends the payment "
    "form on top, then G-1145, then the forms. Mark the envelope and cover "
    "letter with 'Original Submission — Form I-140'. Print single-sided on "
    "8.5x11, no staples or binders, sign in black ink; never use highlighter "
    "or correction fluid on a form (start the page over instead). If shipping "
    "FedEx, use 'Direct Signature Required' — lockboxes cannot accept 'Adult "
    "Signature Required'."
)
