from .models import RecordAdmin, RevokedTokenAdmin, UserAdmin
from .views import ReportView

admin_views = [ReportView]
admin_models = [UserAdmin, RevokedTokenAdmin, RecordAdmin]
