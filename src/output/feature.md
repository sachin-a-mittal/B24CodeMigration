**Feature Name:** PAN Luhn Check Digit Calculation

---

**Business Purpose:**  
Determine the required Luhn check digit for an incomplete PAN so downstream enrollment, tokenization, or authorization flows can validate, store, or recreate a full card number in accordance with industry-standard integrity checks.

---

**Inputs:**  
1. `partial_pan` – The numeric string representing the PAN digits excluding the final check digit.  
   - Format: digits only.  
   - Typical length: up to 18 digits depending on card scheme.  
2. (Optional) `pan_source_context` – Metadata indicating whether the PAN is being processed for enrollment, tokenization, or authorization setup (for audit/logging and triggering this feature as part of respective flows).

---

**Rules:**  
1. Receive a numeric string representing the partial PAN.  
2. Validate input: ensure it contains only digits and falls within allowed length bounds.  
3. Starting from the rightmost digit of the partial PAN, iterate leftwards:  
   - Double every second digit.  
   - If the doubled value exceeds 9, subtract 9 from it.  
4. Sum the transformed digits and any untouched digits.  
5. Calculate the modulo 10 remainder of this sum.  
6. The check digit is the value (0–9) required to bring the total amount up to the next multiple of 10.  
7. Return the computed check digit for downstream storage or validation.

---

**Outputs:**  
- `check_digit` – Single digit (0–9) that completes the PAN according to Luhn rules.  
- `luhn_total` (optional, for logging/tracing) – The summed value before deriving the check digit to aid troubleshooting.

---

**Error Mapping:**  
| Condition | Error Description | EPS Mapping Suggestion |
|----------|-------------------|------------------------|
| `partial_pan` contains non-numeric characters | Input contains invalid characters; cannot perform Luhn calculation. | `INVALID_PAN_DATA` |
| `partial_pan` length outside expected range (too short/long) | PAN fragment length not within expected bounds for a valid card number. | `INVALID_LENGTH_ERROR` (if available) or `INVALID_PAN_DATA` |
| Internal processing failure (e.g., arithmetic overflow) | Unexpected processing error during check digit calculation. | `PROCESSING_FAILURE` |

*Note:* Error outputs should align with existing EPS error codes. If EPS does not have a direct equivalent for one of the above conditions, use the closest matching standard error code while logging the specific Luhn issue for audit/troubleshooting.