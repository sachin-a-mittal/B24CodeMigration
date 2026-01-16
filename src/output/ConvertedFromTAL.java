```java
public class PanLuhnCheckDigitPlugin {

    // Business rule constants
    private static final int MIN_PAN_FRAGMENT_LENGTH = 12;
    private static final int MAX_PAN_FRAGMENT_LENGTH = 18;

    /**
     * Entry point invoked by EPS through the plugin hook.
     * Stateless; does not retain data between invocations.
     */
    public CheckDigitResult execute(String partialPan, String panSourceContext) {
        // Step 1: Validate inputs
        validatePartialPan(partialPan);

        // Step 2: Perform the Luhn sum calculation
        int luhnTotal = computeLuhnTotal(partialPan);

        // Step 3: Determine the check digit required to reach the next multiple of 10
        int checkDigit = deriveCheckDigit(luhnTotal);

        // Step 4: Package result (check digit mandatory, sum optional for tracing)
        return new CheckDigitResult(checkDigit, luhnTotal);
    }

    private void validatePartialPan(String partialPan) {
        if (partialPan == null || partialPan.isEmpty()) {
            throw new PluginBusinessException("Partial PAN is required", ErrorCode.INVALID_PAN_DATA);
        }

        if (partialPan.length() < MIN_PAN_FRAGMENT_LENGTH || partialPan.length() > MAX_PAN_FRAGMENT_LENGTH) {
            throw new PluginBusinessException("PAN fragment length outside allowed range",
                    ErrorCode.INVALID_LENGTH_ERROR);
        }

        if (!partialPan.chars().allMatch(Character::isDigit)) {
            throw new PluginBusinessException("PAN fragment contains non-numeric characters",
                    ErrorCode.INVALID_PAN_DATA);
        }
    }

    private int computeLuhnTotal(String partialPan) {
        int sum = 0;
        boolean doubleDigit = true; // Since check digit missing, start doubling from rightmost digit
        for (int index = partialPan.length() - 1; index >= 0; index--) {
            int digit = Character.digit(partialPan.charAt(index), 10);
            if (doubleDigit) {
                int doubled = digit * 2;
                if (doubled > 9) {
                    doubled -= 9;
                }
                sum += doubled;
            } else {
                sum += digit;
            }
            doubleDigit = !doubleDigit;
        }
        return sum;
    }

    private int deriveCheckDigit(int luhnTotal) {
        int remainder = luhnTotal % 10;
        return remainder == 0 ? 0 : 10 - remainder;
    }

    // Business-friendly result value object
    public static class CheckDigitResult {
        private final int checkDigit;
        private final int luhnTotal;

        public CheckDigitResult(int checkDigit, int luhnTotal) {
            this.checkDigit = checkDigit;
            this.luhnTotal = luhnTotal;
        }

        public int getCheckDigit() {
            return checkDigit;
        }

        public int getLuhnTotal() {
            return luhnTotal;
        }
    }

    // Simplified business exception mapping to EPS error codes
    private static class PluginBusinessException extends RuntimeException {
        private final ErrorCode errorCode;

        public PluginBusinessException(String message, ErrorCode errorCode) {
            super(message);
            this.errorCode = errorCode;
        }

        public ErrorCode getErrorCode() {
            return errorCode;
        }
    }

    private enum ErrorCode {
        INVALID_PAN_DATA,
        INVALID_LENGTH_ERROR,
        PROCESSING_FAILURE
    }
}
```