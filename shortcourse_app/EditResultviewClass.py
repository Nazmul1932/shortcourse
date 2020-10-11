'''from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from shortcourse_app.forms import EditResultForm
from shortcourse_app.models import *


class EditResultViewClass(View):

    def get(self,request,*args,**kwargs):
        instructor_id=request.user.id
        edit_result_form=EditResultForm(instructor_id=instructor_id)
        return render(request,"instructor_template/edit_student_result.html",{"form":edit_result_form})

    def post(self,request,*args,**kwargs):
        form=EditResultForm(instructor_id=request.user.id,data=request.POST)
        if form.is_valid():
            student_admin_id = form.cleaned_data['student_ids']
            exam_marks = form.cleaned_data['exam_marks']
            batch_id = form.cleaned_data['batch_id']

            student_obj = Students.objects.get(admin=student_admin_id)
            batch_obj = Batch.objects.get(id=batch_id)
            result=StudentResult.objects.get(batch_id=batch_obj,student_id=student_obj)
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("edit_student_result"))
        else:
            messages.error(request, "Failed to Update Result")
            form=EditResultForm(request.POST,instructor_id=request.user.id)
            return render(request,"instructor_template/edit_student_result.html",{"form":form})'''