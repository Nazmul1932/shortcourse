import json
from django.shortcuts import render, reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages


def instructor_home(request):
    batches = Batch.objects.filter(instructor_id=request.user.id)
    course_id_list = []
    for batch in batches:
        course = Courses.objects.get(id=batch.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(course_id__in=final_course).count()
    attendance_count = Attendance.objects.filter(batch_id__in=batches).count()

    instructor = Instructors.objects.get(admin=request.user.id)
    leave_count = LeaveReportInstructors.objects.filter(instructor_id=instructor.id, leave_status=1).count()
    batch_count = batches.count()

    batch_list = []
    attendance_list = []
    for batch in batches:
        attendance_count1 = Attendance.objects.filter(batch_id=batch.id).count()
        batch_list.append(batch.batch_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context = {
        'students_count': students_count,
        'attendance_count': attendance_count,
        'leave_count': leave_count,
        'batch_count': batch_count,
        'batch_list': batch_list,
        'attendance_list': attendance_list,
        'student_list': student_list,
        'student_list_attendance_present': student_list_attendance_present,
        'student_list_attendance_absent': student_list_attendance_absent,
    }
    return render(request, 'instructor_template/instructor_home_template.html', context)


def attendance(request):
    batches = Batch.objects.filter(instructor_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        'batches': batches,
        'session_years': session_years
    }

    return render(request, 'instructor_template/attendance_template.html', context)


@csrf_exempt
def get_students(request):
    batch_id = request.POST.get('batch')
    session_year = request.POST.get('session_year')

    batch = Batch.objects.get(id=batch_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    students = Students.objects.filter(course_id=batch.course_id, session_year_id=session_model)

    list_data = []
    for student in students:
        data_small = {'id': student.admin.id, 'name': student.admin.first_name + ' ' + student.admin.last_name}
        list_data.append(data_small)

    # student_data = serializers.serialize('json', students)
    return JsonResponse(json.dumps(list_data), safe=False)

    # return HttpResponse(students)


@csrf_exempt
def save_attendance_date(request):
    student_ids = request.POST.get('student_ids')
    batch_id = request.POST.get('batch_id')
    attendance_date = request.POST.get('attendance_date')
    session_year_id = request.POST.get('session_year_id')

    batch_model = Batch.objects.get(id=batch_id)
    session_model = SessionYearModel.objects.get(id=session_year_id)
    json_student = json.loads(student_ids)

    try:
        attendance = Attendance(batch_id=batch_model, attendance_date=attendance_date, session_year_id=session_model)
        attendance.save()

        for student in json_student:
            stu = Students.objects.get(admin=student['id'])
            attendance_report = AttendanceReport(student_id=stu, attendance_id=attendance, status=student['status'])
            attendance_report.save()

        return HttpResponse('OK')

    except:
        return HttpResponse('ERROR')


def update_attendance(request):
    batches = Batch.objects.filter(instructor_id=request.user.id)
    session_years_id = SessionYearModel.objects.all()
    context = {
        'batches': batches,
        'session_years_id': session_years_id,
    }
    return render(request, 'instructor_template/update_attendance.html', context)


@csrf_exempt
def get_attendance_date(request):
    batch = request.POST.get('batch')
    session_year_id = request.POST.get('session_years_id')
    batch_obj = Batch.objects.get(id=batch)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance_date = Attendance.objects.filter(batch_id=batch_obj, session_year_id=session_year_obj)

    attendance_obj = []
    for attendance_single in attendance_date:
        date = {'id': attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                'session_year_id': attendance_single.session_year_id.id}
        attendance_obj.append(date)
    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), safe=False)


@csrf_exempt
def save_update_attendance_data(request):
    student_ids = request.POST.get('student_ids')
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)
    json_student = json.loads(student_ids)

    try:

        for student in json_student:
            stu = Students.objects.get(admin=student['id'])
            attendance_report = AttendanceReport.objects.get(student_id=stu, attendance_id=attendance)
            attendance_report.status = student['status']
            attendance_report.save()

        return HttpResponse('OK')

    except:
        return HttpResponse('ERROR')


def instructor_apply_leave(request):
    instructor_obj = Instructors.objects.get(admin=request.user.id)
    leave_data = LeaveReportInstructors.objects.filter(instructor_id=instructor_obj)
    context = {
        'leave_data': leave_data,
    }
    return render(request, 'instructor_template/apply_leave.html', context)


def instructor_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('instructor_apply_leave'))
    else:
        leave_date = request.POST.get('leave_date')
        leave_msg = request.POST.get('leave_msg')
        instructor_obj = Instructors.objects.get(admin=request.user.id)

        try:
            leave_report = LeaveReportInstructors(instructor_id=instructor_obj, leave_date=leave_date,
                                                  leave_message=leave_msg,
                                                  leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully applied for leave")
            return HttpResponseRedirect(reverse("instructor_apply_leave"))

        except:
            messages.error(request, "Failed To applied for leave")
            return HttpResponseRedirect(reverse("instructor_apply_leave"))


def instructor_feedback(request):
    instructor_obj = Instructors.objects.get(admin=request.user.id)
    feedback_data = FeedBackInstructors.objects.filter(instructor_id=instructor_obj)
    context = {
        'feedback_data': feedback_data,
    }
    return render(request, 'instructor_template/feedback.html', context)


def instructor_feedback_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('instructor_feedback_save'))
    else:
        feedback_msg = request.POST.get('feedback_msg')
        instructor_obj = Instructors.objects.get(admin=request.user.id)

        try:
            feedback = FeedBackInstructors(instructor_id=instructor_obj, feedback=feedback_msg, feedback_reply='')
            feedback.save()
            messages.success(request, "Successfully sent feedback")
            return HttpResponseRedirect(reverse("instructor_feedback"))

        except:
            messages.error(request, "Failed To send feedback")
            return HttpResponseRedirect(reverse("instructor_feedback"))


def instructor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    instructors = Instructors.objects.get(admin=user)
    context = {
        "user": user,
        "instructors": instructors,
    }
    return render(request, "instructor_template/instructor_profile.html", context)


def instructor_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            custom_user = CustomUser.objects.get(id=request.user.id)
            custom_user.first_name = first_name
            custom_user.last_name = last_name
            if password is not None and password != "":
                custom_user.set_password(password)
            custom_user.save()

            instructors = Instructors.objects.get(admin=custom_user.id)
            instructors.address = address
            instructors.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("instructor_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("instructor_profile"))


def instructor_add_result(request):
    batches = Batch.objects.filter(instructor_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "batches": batches,
        "session_years": session_years,
    }
    return render(request, "instructor_template/instructor_add_result.html", context)


def save_student_result(request):
    if request.method != 'POST':
        return HttpResponseRedirect('instructor_add_result')

    student_admin_id = request.POST.get('student_list')
    exam_marks = request.POST.get('exam_marks')
    batch_id = request.POST.get('batch')

    student_obj = Students.objects.get(admin=student_admin_id)
    batch_obj = Batch.objects.get(id=batch_id)

    try:
        check_exist = StudentResult.objects.filter(batch_id=batch_obj, student_id=student_obj).exists()

        if check_exist:
            result = StudentResult.objects.get(subject_id=batch_obj, student_id=student_obj)
            result.subject_exam_marks = exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("instructor_add_result"))
        else:
            result = StudentResult(student_id=student_obj, batch_id=batch_obj, course_exam_marks=exam_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("instructor_add_result"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("instructor_add_result"))


@csrf_exempt
def fetch_result_student(request):
    batch_id=request.POST.get('batch_id')
    student_id=request.POST.get('student_id')
    student_obj=Students.objects.get(admin=student_id)
    result=StudentResult.objects.filter(student_id=student_obj.id,batch_id=batch_id).exists()
    if result:
        result=StudentResult.objects.get(student_id=student_obj.id,batch_id=batch_id)
        result_data={"exam_marks":result.subject_exam_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")