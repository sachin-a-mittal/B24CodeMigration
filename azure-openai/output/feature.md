**Feature Name**  
PAN Luhn Check Digit Generation

**Business Purpose**  
Provide a reusable mechanism to compute the missing Luhn check digit for a PAN when the preceding digits are supplied, ensuring PANs conform to the industry-standard integrity check before downstream use.

**Inputs**  
1. Partial PAN – numeric string composed of all PAN digits except the final check digit. Length must match expected PAN length minus one.

**Rules**  
1. Input must consist solely of numeric digits and match the expected length for a partial PAN; upstream validation is required before invoking this feature.  
2. Apply the Luhn algorithm: starting from the rightmost digit of the partial PAN, double every second digit moving leftward; if the doubled value exceeds 9, subtract 9; sum all digits (modified and untouched).  
3. Determine the check digit as the value (0–9) that, when added to the total sum, results in the next highest multiple of ten.

**Outputs**  
1. Check Digit – single numeric digit that completes the PAN’s Luhn computation.  
2. Standard success indicator (e.g., response code 200) to denote successful computation.

**Error Mapping**  
1. Invalid Input (non-numeric characters or incorrect length) – map to upstream validation error, resulting in a 400-level error before feature invocation (feature assumes correct input).