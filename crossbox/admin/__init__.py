from django.contrib import admin

from crossbox.models import (
    Reservation,
    Session,
    SessionTemplate,
    Hour,
    Day,
    Subscriber,
)
from crossbox.models.session_template import WeekTemplate, AppraisalLimit
from .reservation import ReservationAdmin
from .session import SessionAdmin
from .session_template import (
    SessionTemplateAdmin,
    WeekTemplateAdmin,
    AppraisalLimitAdmin,
)
from .hour import HourAdmin
from .day import DayAdmin
from .subscriber import SubscriberAdmin

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(SessionTemplate, SessionTemplateAdmin)
admin.site.register(WeekTemplate, WeekTemplateAdmin)
admin.site.register(AppraisalLimit, AppraisalLimitAdmin)
admin.site.register(Hour, HourAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
