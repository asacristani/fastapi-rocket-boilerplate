from unittest import TestCase


class TestViews(TestCase):
    def test_report_page(self):
        pass
        # with patch(
        # "app.services.admin.views.User", MagicMock()
        # ) as mock_user,patch(
        #         "fastapi.requests.Request", MagicMock()) as mock_request:
        #     mock_user.side_effect = 5
        #
        # template = ReportView().report_page(mock_request)
        #
        # assert 200 == template.name
