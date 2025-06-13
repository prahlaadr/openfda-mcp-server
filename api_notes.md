# OpenFDA Classification API Notes

## Endpoint
- URL: https://api.fda.gov/device/classification.json
- Method: GET

## Parameters
- search: string (optional) - search query
- limit: integer (default 100, max 1000) - number of results
- skip: integer (default 0) - pagination offset

## Response Structure
```json
{
  "meta": {
    "disclaimer": "...",
    "terms": "...",
    "license": "...",
    "last_updated": "2025-06-02",
    "results": {
      "skip": 0,
      "limit": 1,
      "total": 6978
    }
  },
  "results": [
    {
      "device_name": "Instrument, Special Lens, For Endoscope",
      "device_class": "1",
      "medical_specialty_description": "Gastroenterology, Urology",
      "regulation_number": "876.1500",
      "product_code": "FEI",
      "review_panel": "GU",
      "medical_specialty": "GU",
      "definition": "",
      "implant_flag": "N",
      "life_sustain_support_flag": "N",
      "gmp_exempt_flag": "N",
      "third_party_flag": "N",
      "summary_malfunction_reporting": "Eligible",
      "submission_type_id": "4",
      "unclassified_reason": "",
      "review_code": "",
      "openfda": {
        "registration_number": [...],
        "fei_number": [...],
        "k_number": [...]
      }
    }
  ]
}
```

## Key Fields
- **device_name**: Name of the medical device
- **device_class**: Classification (1, 2, or 3)
- **medical_specialty_description**: Human-readable specialty
- **regulation_number**: FDA regulation reference
- **product_code**: Unique product code
- **implant_flag**: Whether device is implantable (Y/N)
- **life_sustain_support_flag**: Life support device (Y/N)