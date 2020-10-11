from django.urls import path, include
from . import views, admin_view, instructor_view, student_view, EditResultviewClass


urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin_home/', admin_view.admin_home, name='admin_home'),
    path('do_login', views.do_login, name='do_login'),
    path('get_user_details/', views.get_user_details, name='get_user_details'),
    path('logout_user/', views.logout_user, name='logout_user'),


    path('signup_admin/'),
    path('signup_student/'),
    path('signup_instructor/'),


    # admins view
    path('add_instructor/', admin_view.add_instructor, name='add_instructor'),
    path('add_instructor_save/', admin_view.add_instructor_save, name='add_instructor_save'),
    path('add_course/', admin_view.add_course, name='add_course'),
    path('add_course_save/', admin_view.add_course_save, name='add_course_save'),
    path('add_student/', admin_view.add_student, name='add_student'),
    path('add_student_save/', admin_view.add_student_save, name='add_student_save'),
    path('add_batch/', admin_view.add_batch, name='add_batch'),
    path('add_batch_save/', admin_view.add_batch_save, name='add_batch_save'),
    path('manage_instructor/', admin_view.manage_instructor, name='manage_instructor'),
    path('manage_student/', admin_view.manage_students, name='manage_student'),
    path('manage_courses/', admin_view.manage_course, name='manage_courses'),
    path('manage_batch/', admin_view.manage_batches, name='manage_batch'),
    path('edit_instructor/<str:instructor_id>/', admin_view.edit_instructor, name='edit_instructor'),
    path('edit_instructor_save', admin_view.edit_instructor_save, name='edit_instructor_save'),
    path('edit_student/<str:student_id>/', admin_view.edit_student, name='edit_student'),
    path('edit_student_save', admin_view.edit_student_save, name='edit_student_save'),
    path('edit_batch/<str:batch_id>/', admin_view.edit_batch, name='edit_batch'),
    path('edit_batch_save', admin_view.edit_batch_save, name='edit_batch_save'),
    path('edit_course/<str:course_id>/', admin_view.edit_course, name='edit_course'),
    path('edit_course_save', admin_view.edit_course_save, name='edit_course_save'),
    path('manage_session/', admin_view.manage_session, name='manage_session'),
    path('add_session_save', admin_view.add_session_save, name='add_session_save'),
    path('student_feedback_message/', admin_view.student_feedback_message, name='student_feedback_message'),
    path('student_feedback_message_reply/', admin_view.student_feedback_message_reply, name='student_feedback_message_reply'),
    path('instructor_feedback_message/', admin_view.instructor_feedback_message, name='instructor_feedback_message'),
    path('instructor_feedback_message_reply/', admin_view.instructor_feedback_message_reply, name='instructor_feedback_message_reply'),
    path('check_user_email_exists/', admin_view.check_user_email_exists, name='check_user_email_exists'),
    path('check_username_exist/', admin_view.check_username_exist, name='check_username_exist'),
    path('student_leave_view/', admin_view.student_leave_view, name='student_leave_view'),
    path('student_approve_leave/<str:leave_id>', admin_view.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', admin_view.student_disapprove_leave,
         name="student_disapprove_leave"),
    path('instructor_leave_view/', admin_view.instructor_leave_view, name='instructor_leave_view'),
    path('staff_disapprove_leave/<str:leave_id>', admin_view.instructor_approve_leave, name="instructor_approve_leave"),
    path('staff_approve_leave/<str:leave_id>', admin_view.instructor_disapprove_leave,
         name="instructor_disapprove_leave"),
    path('admin_view_attendance/', admin_view.admin_view_attendance, name='admin_view_attendance'),
    path('admin_get_attendance_date/', admin_view.admin_get_attendance_date, name='admin_get_attendance_date'),
    path('admin_get_attendance_student/', admin_view.admin_get_attendance_student, name='admin_get_attendance_student'),
    path('admin_profile/', admin_view.admin_profile, name='admin_profile'),
    path('admin_profile_save/', admin_view.admin_profile_save, name='admin_profile_save'),


    # instructors view
    path('instructor_home/', instructor_view.instructor_home, name='instructor_home'),
    path('attendance/', instructor_view.attendance, name='attendance'),
    path('get_students/', instructor_view.get_students, name='get_students'),
    path('save_attendance_date/', instructor_view.save_attendance_date, name='save_attendance_date'),
    path('get_attendance_date/', instructor_view.get_attendance_date, name='get_attendance_date'),
    path('update_attendance/', instructor_view.update_attendance, name='update_attendance'),
    path('get_attendance_student/', instructor_view.get_attendance_student, name='get_attendance_student'),
    path('save_update_attendance_data/', instructor_view.save_update_attendance_data, name='save_update_attendance_data'),
    path('instructor_apply_leave/', instructor_view.instructor_apply_leave, name='instructor_apply_leave'),
    path('instructor_apply_leave_save/', instructor_view.instructor_apply_leave_save, name='instructor_apply_leave_save'),
    path('instructor_feedback/', instructor_view.instructor_feedback, name='instructor_feedback'),
    path('instructor_feedback_save/', instructor_view.instructor_feedback_save, name='instructor_feedback_save'),
    path('instructor_profile/', instructor_view.instructor_profile, name='instructor_profile'),
    path('instructor_profile_save/', instructor_view.instructor_profile_save, name='instructor_profile_save'),
    path('instructor_add_result/', instructor_view.instructor_add_result, name='instructor_add_result'),
    path('save_student_result/', instructor_view.save_student_result, name='save_student_result'),
    # path('edit_student_result', EditResultviewClass.as_view(), name="edit_student_result"),
    path('fetch_result_student',instructor_view.fetch_result_student, name="fetch_result_student"),



    # students view
    path('student_home/', student_view.student_home, name='student_home'),
    path('student_view_attendance/', student_view.student_view_attendance, name='student_view_attendance'),
    path('student_view_attendance_post/', student_view.student_view_attendance_post, name='student_view_attendance_post'),
    path('student_apply_leave/', student_view.student_apply_leave, name='student_apply_leave'),
    path('student_apply_leave_save/', student_view.student_apply_leave_save, name='student_apply_leave_save'),
    path('student_feedback/', student_view.student_feedback, name='student_feedback'),
    path('student_feedback_save/', student_view.student_feedback_save, name='student_feedback_save'),
    path('student_profile/', student_view.student_profile, name='student_profile'),
    path('student_profile_save/', student_view.student_profile_save, name='student_profile_save'),
    path('student_view_result/', student_view.student_view_result, name='student_view_result'),

]