from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from shortcourse_app.forms import *


def admin_home(request):

    instructor_count = Instructors.objects.all().count()
    batch_count = Batch.objects.all().count()
    course_count = Courses.objects.all().count()

    course_all = Courses.objects.all()
    course_name_list = []
    batch_count_list = []
    student_count_list_in_course = []
    for course in course_all:
        batches = Batch.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        batch_count_list.append(batches)
        student_count_list_in_course.append(students)

    batches_all = Batch.objects.all()
    batch_list = []
    student_count_list_in_batch = []
    for batch in batches_all:
        course = Courses.objects.get(id=batch.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        batch_list.append(batch.batch_name)
        student_count_list_in_batch.append(student_count)

    instructors = Instructors.objects.all()
    attendance_present_list_instructors = []
    attendance_absent_list_instructors = []
    instructor_name_list = []
    for instructor in instructors:
        batch_ids = Batch.objects.filter(instructor_id=instructor.admin.id)
        attendance = Attendance.objects.filter(batch_id__in=batch_ids).count()
        leaves = LeaveReportInstructors.objects.filter(instructor_id=instructor.id, leave_status=1).count()
        attendance_present_list_instructors.append(attendance)
        attendance_absent_list_instructors.append(leaves)
        instructor_name_list.append(instructor.admin.username)

    students_all = Students.objects.all()
    student_count = students_all.count()
    attendance_present_list_student = []
    attendance_absent_list_student = []
    student_name_list = []
    for student in students_all:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves + absent)
        student_name_list.append(student.admin.username)

    context = {
        'student_count': student_count,
        'instructor_count': instructor_count,
        'batch_count': batch_count,
        'course_count': course_count,
        'course_name_list': course_name_list,
        'batch_count_list': batch_count_list,
        'student_count_list_in_course': student_count_list_in_course,
        'batch_list': batch_list,
        'student_count_list_in_batch': student_count_list_in_batch,
        'attendance_present_list_instructors': attendance_present_list_instructors,
        'attendance_absent_list_instructors': attendance_absent_list_instructors,
        'instructor_name_list': instructor_name_list,
        'attendance_present_list_student': attendance_present_list_student,
        'attendance_absent_list_student': attendance_absent_list_student,
        'student_name_list': student_name_list,
    }
    return render(request, 'admin_template/home_content.html', context)


def add_instructor(request):
    courses = Courses.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'admin_template/adding/add_instructor.html', context)


def add_instructor_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        course_id = request.POST.get('course')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=2)
            course_object = Courses.objects.get(id=course_id)
            user.instructors.course_id = course_object
            user.instructors.address = address
            user.save()
            messages.success(request, "Successfully Added instructor")
            return HttpResponseRedirect(reverse("add_instructor"))
        except:
            messages.error(request, "Failed to Add instructor")
            return HttpResponseRedirect(reverse("add_instructor"))


def edit_instructor(request, instructor_id):
    instructor = Instructors.objects.get(admin=instructor_id)
    courses = Courses.objects.all()

    return render(request, 'admin_template/editing/edit_instructor.html',
                  {'instructor': instructor, 'id': instructor_id, 'courses': courses})


def edit_instructor_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        instructor_id = request.POST.get('instructor_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        address = request.POST.get('address')
        course_id = request.POST.get('course')

        try:
            user = CustomUser.objects.get(id=instructor_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.address = address
            user.save()

            instructor_model = Instructors.objects.get(admin=instructor_id)
            course_object = Courses.objects.get(id=course_id)
            instructor_model.course_id = course_object
            instructor_model.address = address
            instructor_model.save()

            messages.success(request, "Successfully Edited instructor")
            return HttpResponseRedirect(reverse('edit_instructor', kwargs={'instructor_id': instructor_id}))
        except:
            messages.error(request, "Failed to Edited instructor")
            return HttpResponseRedirect(reverse('edit_instructor', kwargs={'instructor_id': instructor_id}))


def manage_instructor(request):
    instructors = Instructors.objects.all()
    return render(request, 'admin_template/manage/manage_instructor.html', {'instructors': instructors})


def add_course(request):
    return render(request, "admin_template/adding/add_course.html")


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, 'admin_template/editing/edit_course.html', {'course': course, 'id': course_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect(reverse('edit_course', kwargs={'course_id': course_id}))
        except:
            messages.error(request, "Failed To Edit Course")
            return HttpResponseRedirect(reverse('edit_course', kwargs={'course_id': course_id}))


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'admin_template/manage/manage_course.html', {'courses': courses})


def add_batch(request):
    courses = Courses.objects.all()
    instructors = CustomUser.objects.filter(user_type=2)
    return render(request, 'admin_template/adding/add_batch.html', {'courses': courses, 'instructors': instructors})


def add_batch_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        batch = request.POST.get("batch")
        batch_time = request.POST.get('appt')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        instructor_id = request.POST.get("instructor")
        instructor = CustomUser.objects.get(id=instructor_id)
        try:
            batch_model = Batch(batch_name=batch, batch_time=batch_time, course_id=course, instructor_id=instructor)
            batch_model.save()
            messages.success(request, "Successfully Added Batch")
            return HttpResponseRedirect(reverse("add_batch"))
        except:
            messages.error(request, "Failed To Add Batch")
            return HttpResponseRedirect(reverse("add_batch"))


def edit_batch(request, batch_id):
    courses = Courses.objects.all()
    batches = Batch.objects.get(id=batch_id)
    instructors = CustomUser.objects.filter(user_type=2)

    return render(request, 'admin_template/editing/edit_batch.html',
                  {'courses': courses, 'batches': batches, 'id': batch_id, 'instructors': instructors})


def edit_batch_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        batch_id = request.POST.get('batch_id')
        batch = request.POST.get("batch")
        batch_time = request.POST.get('appt')
        course_id = request.POST.get('course')
        instructor_id = request.POST.get("instructor")
        try:
            batch_object = Batch.objects.get(id=batch_id)
            batch_object.batch_name = batch
            batch_object.batch_time = batch_time
            course_object = Courses.objects.get(id=course_id)
            batch_object.course_id = course_object
            instructor = CustomUser.objects.get(id=instructor_id)
            batch_object.instructor_id = instructor
            batch_object.save()
            messages.success(request, "Successfully Edited Batch")
            return HttpResponseRedirect(reverse('edit_batch', kwargs={'batch_id': batch_id}))
        except:
            messages.error(request, "Failed To Edit Batch")
            return HttpResponseRedirect(reverse('edit_batch', kwargs={'batch_id': batch_id}))


def manage_batches(request):
    batches = Batch.objects.all()
    return render(request, 'admin_template/manage/manage_batch.html', {'batches': batches})


def add_student(request):
    # courses = Courses.objects.all()
    # batches = Batch.objects.all()
    form = AddStudentForm()
    context = {
        # 'courses': courses,
        # 'batches': batches,
        'form': form,
    }
    return render(request, 'admin_template/adding/add_student.html', context)


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            fathers_name = form.cleaned_data['fathers_name']
            mothers_name = form.cleaned_data['mothers_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data['course']
            batch_id = form.cleaned_data['batch']
            sex = form.cleaned_data['sex']
            nationality = form.cleaned_data['nationality']
            phone_number = form.cleaned_data['phone_no']
            ssc_board = form.cleaned_data['ssc_board']
            hsc_board = form.cleaned_data['hsc_board']
            ssc_gpa = form.cleaned_data['ssc_gpa']
            hsc_gpa = form.cleaned_data['hsc_gpa']

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name, first_name=first_name, user_type=3)
                user.students.address = address
                user.students.ssc_gpa = ssc_gpa
                user.students.hsc_gpa = hsc_gpa
                user.students.ssc_board = ssc_board
                user.students.hsc_board = hsc_board
                user.students.fathers_name = fathers_name
                user.students.mothers_name = mothers_name
                user.students.city = city
                user.students.nationality = nationality
                user.students.phone_no = phone_number
                course_object = Courses.objects.get(id=course_id)
                user.students.course_id = course_object
                batch_object = Batch.objects.get(id=batch_id)
                user.students.batch = batch_object
                session_year = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.gender_choice = sex
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Successfully Added students")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add students")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, 'admin_template/adding/add_student.html', {'form': form})


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['fathers_name'].initial = student.fathers_name
    form.fields['mothers_name'].initial = student.mothers_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['city'].initial = student.city
    form.fields['nationality'].initial = student.nationality
    form.fields['phone_no'].initial = student.phone_no
    form.fields['ssc_gpa'].initial = student.ssc_gpa
    form.fields['hsc_gpa'].initial = student.hsc_gpa
    form.fields['ssc_board'].initial = student.ssc_board
    form.fields['hsc_board'].initial = student.hsc_board
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender_choice
    form.fields['session_year_id'].initial = student.session_year_id.id
    form.fields['batch'].initial = student.batch

    return render(request, 'admin_template/editing/edit_student.html',
                  {'form': form, 'id': student_id, 'username': student.admin.username})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id = request.session.get('student_id')
        if student_id is None:
            return HttpResponseRedirect(reverse('manage_student'))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            fathers_name = form.cleaned_data['fathers_name']
            mothers_name = form.cleaned_data['mothers_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data['course']
            batch = form.cleaned_data['batch']
            sex = form.cleaned_data['sex']
            nationality = form.cleaned_data['nationality']
            phone_no = form.cleaned_data['phone_no']
            ssc_board = form.cleaned_data['ssc_board']
            hsc_board = form.cleaned_data['hsc_board']
            ssc_gpa = form.cleaned_data['ssc_gpa']
            hsc_gpa = form.cleaned_data['hsc_gpa']

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=student_id)
                student.fathers_name = fathers_name
                student.mothers_name = mothers_name
                student.address = address
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender_choice = sex
                student.city = city
                student.nationality = nationality
                student.phone_no = phone_no
                student.ssc_board = ssc_board
                student.ssc_gpa = ssc_gpa
                student.hsc_board = hsc_board
                student.hsc_gpa = hsc_gpa
                course = Courses.objects.get(id=course_id)
                student.course_id = course
                batches = Batch.objects.get(id=batch)
                student.batch = batches

                if profile_pic_url is not None:
                    student.profile_pic = profile_pic_url

                student.save()
                del request.session['student_id']
                messages.success(request, "Successfully Edited student")
                return HttpResponseRedirect(reverse('edit_student', kwargs={'student_id': student_id}))
            except:
                messages.error(request, "Failed to Edited student")
                return HttpResponseRedirect(reverse('edit_student', kwargs={'student_id': student_id}))
        else:
            form - EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request, 'admin_template/editing/edit_student.html',
                          {'form': form, 'id': student_id, 'username': student.admin.username})


def manage_students(request):
    students = Students.objects.all()

    return render(request, 'admin_template/manage/manage_student.html', {'students': students})


def manage_session(request):
    return render(request, 'admin_template/manage/manage_session.html')


def add_session_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('manage_session'))
    else:
        session_start_year = request.POST.get('session_start')
        session_end_year = request.POST.get('session_end')
        try:
            session_year_model = SessionYearModel(session_start_year=session_start_year,
                                                  session_end_year=session_end_year)
            session_year_model.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse('manage_session'))
        except:
            messages.error(request, "Failed To Added Session")
            return HttpResponseRedirect(reverse('manage_session'))


@csrf_exempt
def check_user_email_exists(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedback_students = FeedBackStudent.objects.all()
    context = {
        'feedback_students': feedback_students,
    }
    return render(request, 'admin_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_msg = request.POST.get('message')

    try:
        feedback_student = FeedBackStudent.objects.get(id=feedback_id)
        feedback_student.feedback_reply = feedback_msg
        feedback_student.save()
        return HttpResponse('True')
    except:
        return HttpResponse('False')


def instructor_feedback_message(request):
    feedback_instructors = FeedBackInstructors.objects.all()
    return render(request, "admin_template/instructor_feedback_template.html",
                  {"feedback_instructors": feedback_instructors})


@csrf_exempt
def instructor_feedback_message_reply(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackInstructors.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        'leaves': leaves,
    }
    return render(request, 'admin_template/student_leave_view.html', context)


def student_approve_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_disapprove_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def instructor_leave_view(request):
    leaves = LeaveReportInstructors.objects.all()
    return render(request, "admin_template/instructor_leave_view.html", {"leaves": leaves})


def instructor_approve_leave(request, leave_id):
    leave = LeaveReportInstructors.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("instructor_leave_view"))


def instructor_disapprove_leave(request, leave_id):
    leave = LeaveReportInstructors.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("instructor_leave_view"))


def admin_view_attendance(request):
    batches = Batch.objects.all()
    session_years_id = SessionYearModel.objects.all()
    context = {
        'batches': batches,
        'session_years_id': session_years_id,
    }
    return render(request, 'admin_template/admin_view_attendance.html', context)


@csrf_exempt
def admin_get_attendance_date(request):
    batch = request.POST.get("batch")
    session_year_id = request.POST.get("session_year_id")
    batch_obj = Batch.objects.get(id=batch)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(batch_id=batch_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
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


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_template/admin_profile.html", {"user": user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            custom_user = CustomUser.objects.get(id=request.user.id)
            custom_user.first_name = first_name
            custom_user.last_name = last_name
            if password is not None and password != "":
                custom_user.set_password(password)
            custom_user.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
