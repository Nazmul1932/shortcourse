from django import forms
from .models import *
from django.forms import ChoiceField


class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass


class DateInput(forms.DateInput):
    input_type = 'date'


class AddStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=200, widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete":"off"}))
    password = forms.CharField(label='Password', max_length=200, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label='First Name', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label='Last Name', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    fathers_name = forms.CharField(label='Fathers Name', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    mothers_name = forms.CharField(label='Mothers Name', max_length=200,  widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label='UserName', max_length=200,  widget=forms.TextInput(attrs={"class": "form-control", "autocomplete":"off"}))
    address = forms.CharField(label='Address', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(label='City', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label='Nationality', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_no = forms.CharField(label='Phone No', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))

    board_choice = (
        ('Dhaka', 'Dhaka'),
        ('Cumilla', 'Cumilla'),
        ('Chittagong', 'Chittagong'),
        ('Rajshahi', 'Rajshahi'),
        ('Sylhet', 'Sylhet'),
        ('Dinajpur', 'Dinajpur'),
        ('Khulna', 'Khulna'),
        ('Barishal', 'Barishal'),
        ('Jessore', 'Jessore'),
    )
    ssc_board = forms.ChoiceField(label='SSC Board', choices=board_choice,  widget=forms.Select(attrs={"class": "form-control"}))
    hsc_board = forms.ChoiceField(label='HSC Board', choices=board_choice, widget=forms.Select(attrs={"class": "form-control"}))
    ssc_gpa = forms.CharField(label='SSC GPA', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    hsc_gpa = forms.CharField(label='HSC GPA', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            small_course = (course.id, course.course_name)
            course_list.append(small_course)
    except:
        course_list = []
    course = forms.ChoiceField(label='Course', choices=course_list, widget=forms.Select(attrs={"class": "form-control"}))
    batch_list = []
    try:
        batches = Batch.objects.all()
        for batch in batches:
            small_batches = (batch.id, batch.batch_name)
            batch_list.append(small_batches)
    except:
        batch_list = []
    batch = forms.ChoiceField(label='Batch', choices=batch_list, widget=forms.Select(attrs={"class": "form-control"}))
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = forms.ChoiceField(label='Gender', choices=gender_choices, widget=forms.Select(attrs={"class": "form-control"}))
    session_list = []
    try:
        sessions = SessionYearModel.objects.all()
        for i in sessions:
            session = (i.id, str(i.session_start_year) + ' TO ' + str(i.session_end_year))
            session_list.append(session)
    except:
        session_list = []
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", max_length=50,  widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=200, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label='First Name', max_length=200,  widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label='Last Name', max_length=200,  widget=forms.TextInput(attrs={"class": "form-control"}))
    fathers_name = forms.CharField(label='Fathers Name', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    mothers_name = forms.CharField(label='Mothers Name', max_length=200,  widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label='UserName', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label='Address', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(label='City', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label='Nationality', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_no = forms.CharField(label='Phone No', max_length=200,  widget=forms.TextInput(attrs={"class": "form-control"}))
    board_choice = (
        ('Dhaka', 'Dhaka'),
        ('Cumilla', 'Cumilla'),
        ('Chittagong', 'Chittagong'),
        ('Rajshahi', 'Rajshahi'),
        ('Sylhet', 'Sylhet'),
        ('Dinajpur', 'Dinajpur'),
        ('Khulna', 'Khulna'),
        ('Barishal', 'Barishal'),
        ('Jessore', 'Jessore'),
    )
    ssc_board = forms.ChoiceField(label='SSC Board', choices=board_choice,  widget=forms.Select(attrs={"class": "form-control"}))
    hsc_board = forms.ChoiceField(label='HSC Board', choices=board_choice,  widget=forms.Select(attrs={"class": "form-control"}))
    ssc_gpa = forms.CharField(label='SSC GPA', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    hsc_gpa = forms.CharField(label='HSC GPA', max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            small_course = (course.id, course.course_name)
            course_list.append(small_course)
    except:
        course_list = []
    course = forms.ChoiceField(label='Course', choices=course_list, widget=forms.Select(attrs={"class": "form-control"}))
    batch_list = []
    try:
        batches = Batch.objects.all()
        for batch in batches:
            small_batches = (batch.id, batch.batch_name)
            batch_list.append(small_batches)
    except:
        batch_list = []
    batch = forms.ChoiceField(label='Batch', choices=batch_list, widget=forms.Select(attrs={"class": "form-control"}))
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = forms.ChoiceField(label='Gender', choices=gender_choices,widget=forms.Select(attrs={"class": "form-control"}))
    session_list = []
    try:
        sessions = SessionYearModel.objects.all()
        for i in sessions:
            session = (i.id, str(i.session_start_year) + ' TO ' + str(i.session_end_year))
            session_list.append(session)
    except:
        session_list = []
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", max_length=50,  widget=forms.FileInput(attrs={"class": "form-control"}), required=False)


'''class EditResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instructor_id=kwargs.pop("staff_id")
        super(EditResultForm,self).__init__(*args,**kwargs)
        batch_list=[]
        try:
            batches=Batch.objects.filter(instructor_id=self.instructor_id)
            for batch in batches:
                batch_single=(batch.id,batch.batch_name)
                batch_list.append(batch_single)
        except:
            batch_list=[]
        self.fields['batch_id'].choices=batch_list

    session_list=[]
    try:
        sessions=SessionYearModel.objects.all()
        for session in sessions:
            session_single=(session.id,str(session.session_start_year)+" TO "+str(session.session_end_year))
            session_list.append(session_single)
    except:
        session_list=[]

    subject_id=forms.ChoiceField(label="Subject",widget=forms.Select(attrs={"class":"form-control"}))
    session_ids=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    student_ids=ChoiceNoValidation(label="Student",widget=forms.Select(attrs={"class":"form-control"}))
    exam_marks=forms.CharField(label="Exam Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
'''