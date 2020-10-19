from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
admin.site.register(AdminHOD)
admin.site.register(Attendance)
admin.site.register(Courses)
admin.site.register(Batch)
admin.site.register(Instructors)
admin.site.register(Students)
admin.site.register(NotificationStudent)
admin.site.register(NotificationInstructors)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportInstructors)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackInstructors)
admin.site.register(AttendanceReport)

