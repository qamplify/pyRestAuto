import pytest
import time

pytest.main(['--html=html_reports/TestReport_'
             ''+time.strftime("%d-%b-%Y_%H-%M-%S")+'.html'])