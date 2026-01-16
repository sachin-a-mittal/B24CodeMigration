Here is a clear mapping of the TAL (feature-level) response conditions for “PAN Luhn Check Digit Calculation” to the corresponding EPS-standard responses:

| TAL Condition / Response | EPS-Standard Response Code | Notes |
|--------------------------|----------------------------|-------|
| `partial_pan` contains non-numeric characters (invalid characters detected during validation) | `INVALID_PAN_DATA` | Use EPS’s `INVALID_PAN_DATA` code to indicate invalid characters, aligning directly with the TAL error description. |
| `partial_pan` length is outside the allowed bounds (too short or too long) | `INVALID_LENGTH_ERROR` (if available) <br>otherwise `INVALID_PAN_DATA` | Prefer EPS’s dedicated `INVALID_LENGTH_ERROR` if the namespace supports it; otherwise map to the broader `INVALID_PAN_DATA`. |
| Unexpected internal processing failure (e.g., arithmetic overflow) during check digit calculation | `PROCESSING_FAILURE` | Represents downstream/internal errors encountered while computing the Luhn digit. |

This table ensures each TAL condition is expressed using the closest EPS-standard response code, as outlined in the EPS feature specification.