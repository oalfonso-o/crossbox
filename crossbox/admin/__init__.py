from django.contrib import admin

from crossbox.models.capacity_limit import CapacityLimit
from crossbox.models.card import Card
from crossbox.models.day import Day
from crossbox.models.fee import Fee
from crossbox.models.hour import Hour
from crossbox.models.reservation import Reservation
from crossbox.models.session import Session
from crossbox.models.session_template import SessionTemplate
from crossbox.models.session_type import SessionType
from crossbox.models.subscriber import Subscriber
from crossbox.models.week_template import WeekTemplate
from crossbox.models.payment import Payment

from crossbox.admin.capacity_limit import CapacityLimitAdmin
from crossbox.admin.card import CardAdmin
from crossbox.admin.day import DayAdmin
from crossbox.admin.fee import FeeAdmin
from crossbox.admin.hour import HourAdmin
from crossbox.admin.reservation import ReservationAdmin
from crossbox.admin.session import SessionAdmin
from crossbox.admin.session_template import SessionTemplateAdmin
from crossbox.admin.session_type import SessionTypeAdmin
from crossbox.admin.subscriber import SubscriberAdmin
from crossbox.admin.week_template import WeekTemplateAdmin
from crossbox.admin.payment import PaymentAdmin

admin.site.register(CapacityLimit, CapacityLimitAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Hour, HourAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(SessionTemplate, SessionTemplateAdmin)
admin.site.register(SessionType, SessionTypeAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(WeekTemplate, WeekTemplateAdmin)
admin.site.register(Payment, PaymentAdmin)
