# UK Take-Home Pay Calculator

A small web app that works out UK take-home pay after income tax, National Insurance, student loan repayments and pension contributions, with a full **CI/CD pipeline** that automatically tests, builds and deploys every change.

**Live app:** _add your Streamlit link here_

Covers England, Wales and Northern Ireland for the 2026/27 tax year. Figures are estimates only.

## What it does

Enter a salary, a pension percentage and a student loan plan, and the app shows:

- income tax (including the personal allowance shrinking above £100,000)
- employee National Insurance
- student loan repayments (Plan 2 and Plan 5)
- pension contributions (salary sacrifice, taken off before tax)
- take-home pay per year and per month

## How the pipeline works

Every time code is pushed to `main`, GitHub Actions runs three stages in order. If any stage fails, the later ones don't run, so broken code never reaches the live app.

```
push to main
   │
   ▼
1. Lint and test ──── ruff checks code quality, pytest runs 16 automated tests
   │ (only if passed)
   ▼
2. Build container ── builds a Docker image and checks the app starts and responds
   │ (only if passed)
   ▼
3. Deploy ─────────── pushes the tested code to the `deploy` branch,
                      which Streamlit Community Cloud serves as the live app
```

## Project files

| File | What it is |
|---|---|
| `calculator.py` | The tax and pay calculations |
| `app.py` | The web page, built with Streamlit |
| `test_calculator.py` | Tests checking the calculations against known answers |
| `test_app.py` | Tests checking the web page loads and shows the right result |
| `Dockerfile` | Instructions for packaging the app into a container |
| `.github/workflows/pipeline.yml` | The CI/CD pipeline |
| `requirements.txt` / `requirements-dev.txt` | Packages the app and the tests need |

## Run it on your own computer

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -v                 # run the tests
streamlit run app.py      # open the app at http://localhost:8501
```

Or with Docker:

```bash
docker build -t uk-tax-calculator .
docker run -p 8501:8501 uk-tax-calculator
```

## What I learned

- How automated tests catch mistakes before they reach users. I tested this by deliberately breaking a tax rate and watching the pipeline fail.
- How a CI/CD pipeline chains stages together so code is only released once every check has passed
- How Docker packages an app so it runs the same way on any computer
- How the UK tax system works, including the 60% effective tax rate between £100,000 and £125,140
