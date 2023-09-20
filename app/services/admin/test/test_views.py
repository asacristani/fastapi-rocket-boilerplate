from unittest import TestCase
from unittest.mock import patch, MagicMock

from app.services.admin.views import ReportView


class TestViews(TestCase):

    def test_report_page(self):
        pass
        # with patch("app.services.admin.views.User", MagicMock()) as mock_user,patch(
        #         "fastapi.requests.Request", MagicMock()) as mock_request:
        #     mock_user.side_effect = 5
        #
        # template = ReportView().report_page(mock_request)
        #
        # assert 200 == template.name
