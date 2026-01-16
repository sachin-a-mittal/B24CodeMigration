Here is the EPS-standard response mapping for the PAN Luhn Check Digit Generation feature:

| TAL Response Code | Description | EPS Standard Response | EPS Semantics |
|-------------------|-------------|-----------------------|---------------|
| `200` | Partial PAN accepted, Luhn check digit computed successfully. | `EPS-200 (Success)` | Feature completed; check digit returned. |
| `400` (upstream validation) | Partial PAN invalid due to non-numeric characters or incorrect length. Feature itself is not invoked; error surfaced by upstream validation. | `EPS-400 (Invalid Request)` | Request rejected before feature execution; caller must correct the partial PAN. |

**Notes:**  
- The feature assumes upstream validation has already enforced rule compliance; only the success response (`200`) is emitted by the feature itself.  
- Invalid input cases are mapped to EPS-standard `400` responses even though the feature is not performed.