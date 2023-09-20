from .models import UserAdmin, RevokedTokenAdmin, RecordAdmin
from .views import ReportView

admin_views = [ReportView]
admin_models = [UserAdmin, RevokedTokenAdmin, RecordAdmin]
