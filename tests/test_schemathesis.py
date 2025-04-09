import schemathesis
# from hypothesis import settings, Phase
# import pytest

# pytest -v -p no:warnigs --html=report.html --self-contained-html
# je potřeba mít spuštěný server na localhost:8000


schemathesis.experimental.OPEN_API_3_1.enable()

schema = schemathesis.from_uri("http://localhost:8000/openapi.json")


@schema.parametrize()
def test_api(case):
    response = case.call()
    case.validate_response(response)
