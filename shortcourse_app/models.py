from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    objects = models.Manager()
    session_start_year = models.DateField()
    session_end_year = models.DateField()


class CustomUser(AbstractUser):
    user_type_data = ((1, 'Admin'), (2, 'Instructor'), (3, 'Students'))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=20)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.course_name


class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    batch_name = models.CharField(max_length=200, null=True)
    batch_time = models.CharField(max_length=200, null=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    instructor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.batch_name


class Instructors(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    # batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE, default=1)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    instructor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Students(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200, null=True)
    fathers_name = models.CharField(max_length=200, null=True)
    mothers_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    nationality = models.CharField(max_length=200, null=True)
    phone_no = models.CharField(max_length=200, null=True)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )
    gender_choice = models.CharField(max_length=20, null=True, choices=GENDER)
    BOARDS = [
        ('Dhaka', 'Dhaka'),
        ('Cumilla', 'Cumilla'),
        ('Chittagong', 'Chittagong'),
        ('Rajshahi', 'Rajshahi'),
        ('Sylhet', 'Sylhet'),
        ('Dinajpur', 'Dinajpur'),
        ('Khulna', 'Khulna'),
        ('Barishal', 'Barishal'),
        ('Jessore', 'Jessore'),
    ]
    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    ssc_board = models.CharField(max_length=100, null=True, choices=BOARDS)
    ssc_gpa = models.FloatField(default=0.0)
    city = models.CharField(max_length=100, null=True, choices=BOARDS)
    hsc_board = models.CharField(max_length=100, null=True, choices=BOARDS)
    hsc_gpa = models.FloatField(default=0.0)
    address = models.TextField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.FileField()
    objects = models.Manager()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportInstructors(models.Model):
    id = models.AutoField(primary_key=True)
    instructor_id = models.ForeignKey(Instructors, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackInstructors(models.Model):
    id = models.AutoField(primary_key=True)
    instructor_id = models.ForeignKey(Instructors, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationInstructors(models.Model):
    id = models.AutoField(primary_key=True)
    instructor_id = models.ForeignKey(Instructors, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    batch_id=models.ForeignKey(Batch, on_delete=models.CASCADE)
    course_exam_marks=models.FloatField(default=0)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    objects=models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Instructors.objects.create(admin=instance, address='')
        if instance.user_type == 3:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1), session_year_id=SessionYearModel.objects.get(id=1),
                                    address='', gender_choice='', profile_pic='')


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.instructors.save()
    if instance.user_type == 3:
        instance.students.save()
