import pytest
import os
from utils.driver_factory import get_driver
from utils.logger import get_logger

logger = get_logger()

@pytest.fixture(scope="function")
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs['driver']
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(f"screenshots/{item.name}.png")
        logger.error(f"Test failed: {item.name}")
