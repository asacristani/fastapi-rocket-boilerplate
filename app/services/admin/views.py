from sqladmin import BaseView, expose

from app.services.user.models import User


class ReportView(BaseView):
    """
    A simple test custom view
    """
    name = "Report Page (test)"
    icon = "fa-chart-line"

    @expose("/report", methods=["GET"])
    def report_page(self, request):
        # Get the total of Users
        users_count = User.count()

        return self.templates.TemplateResponse(
            "report.html",
            context={"request": request, "users_count": users_count},
        )
