```java
public class PanLuhnCheckDigitPlugin /* implements EpsPlugin */ {

    /**
     * Computes the missing Luhn check digit for a PAN when all preceding digits are provided.
     * The plugin assumes upstream validation guarantees:
     * - The partialPan contains only numeric digits.
     * - The length equals the PAN length minus one.
     *
     * @param partialPan the PAN digits excluding the final check digit
     * @return the single-digit Luhn check digit
     */
    public String computeCheckDigit(String partialPan) {
        int sum = 0;
        boolean doubleDigit = true;

        /*
         * Business rule: Starting from the rightmost digit of the partial PAN,
         * double every second digit moving leftward. If doubling produces a value
         * greater than 9, subtract 9. Accumulate the resulting digits into a sum.
         */
        for (int index = partialPan.length() - 1; index >= 0; index--) {
            int digit = Character.getNumericValue(partialPan.charAt(index));
            if (doubleDigit) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            sum += digit;
            doubleDigit = !doubleDigit;
        }

        /*
         * Business rule: Determine the check digit as the value that brings the sum
         * up to the next multiple of ten.
         */
        int mod = sum % 10;
        int checkDigit = (mod == 0) ? 0 : (10 - mod);

        return Integer.toString(checkDigit);
    }

    /**
     * Example plugin entry point EPS would invoke.
     * Assumes upstream ensures input validity and handles any errors pre-invocation.
     *
     * @param request contains partial PAN
     * @return response with computed check digit and success indicator
     */
    public PluginResponse handleRequest(PluginRequest request) {
        String partialPan = request.getPartialPan();
        String checkDigit = computeCheckDigit(partialPan);

        PluginResponse response = new PluginResponse();
        response.setCheckDigit(checkDigit);
        response.setStatusCode(200);
        return response;
    }

    // Placeholder request/response structures to illustrate expected usage.
    public static class PluginRequest {
        private String partialPan;

        public String getPartialPan() {
            return partialPan;
        }

        public void setPartialPan(String partialPan) {
            this.partialPan = partialPan;
        }
    }

    public static class PluginResponse {
        private String checkDigit;
        private int statusCode;

        public String getCheckDigit() {
            return checkDigit;
        }

        public void setCheckDigit(String checkDigit) {
            this.checkDigit = checkDigit;
        }

        public int getStatusCode() {
            return statusCode;
        }

        public void setStatusCode(int statusCode) {
            this.statusCode = statusCode;
        }
    }
}
```