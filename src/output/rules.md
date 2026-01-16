1. **Rule name:** Compute Luhn Check Digit  
   **Condition:** The system receives a partial PAN without the final digit during card enrollment, tokenization, or authorization setup.  
   **Action:** Iterate digits from right to left, double every second digit per the Luhn algorithm, subtract 9 from doubled values exceeding 9, sum all digits, compute the modulo 10 remainder, and return the check digit that brings the total to the next multiple of 10.  
   **Response code:** N/A