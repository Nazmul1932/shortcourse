from django.shortcuts import render, reverse
from . models import *
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib import messages



def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()
    course_name = Courses.objects.get(course_name=student_obj.course_id.course_name)
    batch_name = Batch.objects.get(batch_name=student_obj.batch.batch_name)

    batches_name = []
    data_present = []
    data_absent = []
    batch_date = Batch.objects.filter(course_id=student_obj.course_id)

    for batch in batch_date:
        attendance = Attendance.objects.filter(batch_id=batch.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,
                                                                   student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False,
                                                                  student_id=student_obj.id).count()
        batches_name.append(batch.batch_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    attendance_avg = attendance_present/attendance_total
    attendance_round = attendance_avg * 100
    attendance_percent = round(attendance_round, 2)

    context = {
        'attendance_total': attendance_total,
        'attendance_percent': attendance_percent,
        'attendance_present': attendance_present,
        'attendance_absent': attendance_absent,
        'course_name': course_name,
        'batch_name': batch_name,
        'batches_name': batches_name,
        'data_present': data_present,
        'data_absent': data_absent,
    }
    return render(request, 'student_template/student_home_template.html', context)


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    batches = Batch.objects.filter(course_id=course)
    context = {
        'batches': batches,
    }
    return render(request, 'student_template/student_view_attendance.html', context)


def student_view_attendance_post(request):
    batch_id = request.POST.get("batch")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_data_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_data_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    batch_obj = Batch.objects.get(id=batch_id)
    user_object = CustomUser.objects.get(id=request.user.id)
    stud_obj = Students.objects.get(admin=user_object)

    attendance = Attendance.objects.filter(attendance_date__range=(start_data_parse, end_data_parse),
                                           batch_id=batch_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

    context = {
        'attendance_reports': attendance_reports,
    }

    return render(request, 'student_template/student_attendance_data.html', context)


def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data,
    }
    return render(request, "student_template/student_apply_leave.html", context)


def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    student_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=student_id)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "student_template/student_feedback.html", context)


def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")
        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    context = {
        "user": user,
        "student": student,
    }
    return render(request, "student_template/student_profile.html", context)


def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            custom_user = CustomUser.objects.get(id=request.user.id)
            custom_user.first_name = first_name
            custom_user.last_name = last_name
            if password is not None and password != "":
                custom_user.set_password(password)
            custom_user.save()

            student = Students.objects.get(admin=custom_user)
            student.address = address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    return render(request, "student_template/student_result.html", {"student_result": student_result})