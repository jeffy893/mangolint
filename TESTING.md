# Mangolint Testing Guide

## Overview

Comprehensive testing infrastructure for Mangolint including unit tests, integration tests, and example usage files.

## Test Files

### 1. `example_usages.txt`
**Purpose**: Real-world examples you can copy/paste into the Mangolint interface

**Contains 20 examples:**
- Single ingredients (mango, turmeric)
- Product descriptions (skincare, beverages)
- Recipes (traditional, modern)
- Spice blends (curry, pickling)
- Superfood combinations
- Aromatic descriptions

**How to use:**
1. Open `example_usages.txt`
2. Copy any example (they're separated by comment blocks)
3. Paste into Mangolint text editor at http://localhost:5001
4. Watch real-time analysis or click "Analyze Text"
5. Verify indigenous synonyms, cultural context, and brand insights appear

### 2. `tests/test_linter.py`
**Purpose**: Unit tests for BedrockLinter class

**Tests:**
- ✓ Initialization with correct region and model
- ✓ Prompt construction with persona and JSON format
- ✓ Empty text handling
- ✓ Mocked Bedrock API responses
- ✓ Model info retrieval

### 3. `tests/test_app.py`
**Purpose**: Integration tests for Flask application

**Tests:**
- ✓ Index route renders correctly
- ✓ Health endpoint returns status
- ✓ Model info endpoint
- ✓ Lint endpoint with various inputs
- ✓ Analyze endpoint validation
- ✓ Error handling for invalid requests

### 4. `run_tests.py`
**Purpose**: Test runner that generates comprehensive reports

**Features:**
- Discovers and runs all tests
- Generates formatted report with summary
- Shows detailed output, failures, and errors
- Provides recommendations
- Saves report to `test_report.txt`

## Running Tests

### Run All Tests
```bash
source venv/bin/activate
python3.10 run_tests.py
```

### Run Specific Test File
```bash
source venv/bin/activate
python3.10 -m unittest tests.test_linter
python3.10 -m unittest tests.test_app
```

### Run Single Test
```bash
source venv/bin/activate
python3.10 -m unittest tests.test_linter.TestBedrockLinter.test_initialization
```

## Test Report

After running `run_tests.py`, you'll get:

```
MANGOLINT TEST REPORT
Generated: 2026-02-15 11:48:17
Duration: 0.49 seconds

SUMMARY
Tests Run: 12
Successes: 12
Failures: 0
Errors: 0
Skipped: 0

STATUS: ✅ ALL TESTS PASSED
```

Report is saved to `test_report.txt` for review.

## Manual Testing Workflow

### 1. Start the Application
```bash
source venv/bin/activate
python3.10 app.py
```
Access at: http://localhost:5001

### 2. Test Real-Time Linting
1. Open `example_usages.txt`
2. Copy "EXAMPLE 1: Single Ingredient" (just the word "mango")
3. Paste into text editor
4. Wait 500ms - should see underline appear
5. Check sidebar for indigenous synonyms

### 3. Test Multiple Ingredients
1. Copy "EXAMPLE 2: Spice Blend"
2. Paste into editor
3. Verify 3 ingredients detected (ginger, cardamom, black pepper)
4. Click each underlined word
5. Verify sidebar scrolls to that ingredient

### 4. Test Complex Descriptions
1. Copy "EXAMPLE 3: Skincare Product Description"
2. Paste and analyze
3. Verify brand insights appear
4. Check authenticity markers
5. Review traditional uses

### 5. Test Edge Cases
- Empty text (should show empty state)
- Very short text (< 3 chars, should not analyze)
- Text with no ingredients (should show "no entities detected")
- Very long text (test performance)

## Expected Results

### For "mango":
- **Indigenous Synonyms**: Manga (Portuguese), Aam (Hindi), Māṅgāy (Tamil), Mangga (Tagalog)
- **Context**: Ripeness stages (green vs ripe)
- **Brand Insights**: Specify ripeness and preparation method
- **Traditional Uses**: Culinary, medicinal, ceremonial

### For "turmeric":
- **Indigenous Synonyms**: Haldi (Hindi), Manjal (Tamil), Pasupu (Telugu)
- **Context**: Fresh vs dried, culinary vs medicinal
- **Traditional Uses**: Ayurvedic medicine, ceremonial (Hindu weddings)

### For "coconut":
- **Indigenous Synonyms**: Nariyal (Hindi), Thengai (Tamil), Kelapa (Malay)
- **Context**: Young (tender water) vs mature (copra)
- **Traditional Uses**: Sacred in Hindu rituals

## Performance Benchmarks

Expected performance (with real Bedrock API):
- Single ingredient: 2-4 seconds
- 3-5 ingredients: 3-6 seconds
- Complex text (10+ ingredients): 5-10 seconds

Debounce delay: 500ms (prevents excessive API calls)

## Continuous Integration

To integrate with CI/CD:

```bash
# In your CI pipeline
python3.10 run_tests.py
if [ $? -eq 0 ]; then
    echo "Tests passed - deploying"
else
    echo "Tests failed - blocking deployment"
    exit 1
fi
```

## Adding New Tests

### Add Unit Test
1. Edit `tests/test_linter.py`
2. Add method starting with `test_`
3. Use assertions to verify behavior
4. Run `python3.10 run_tests.py`

### Add Integration Test
1. Edit `tests/test_app.py`
2. Use `self.client.get()` or `self.client.post()`
3. Assert response codes and data
4. Run tests

### Add Example Usage
1. Edit `example_usages.txt`
2. Add new section with clear header
3. Include expected results as comments
4. Test manually in the interface

## Troubleshooting

### Tests Fail with AWS Credentials Error
- Tests use mocked Bedrock responses
- Real API calls only happen in manual testing
- Check that mocking is working correctly

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version is 3.10

### Flask App Not Starting
- Check port 5001 is available
- Verify .env file exists
- Check AWS credentials in ~/.aws/credentials

## Best Practices

1. **Run tests before committing** - Ensure nothing breaks
2. **Add tests for new features** - Maintain coverage
3. **Use example_usages.txt** - Quick manual verification
4. **Review test reports** - Understand failures
5. **Test edge cases** - Empty, invalid, extreme inputs

## Next Steps

- Add end-to-end tests with real Bedrock API
- Add performance benchmarks
- Add load testing for concurrent requests
- Add UI automation tests (Selenium/Playwright)
- Add code coverage reporting
