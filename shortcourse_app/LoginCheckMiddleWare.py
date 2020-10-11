from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponseRedirect


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        print(module_name)
        user = request.user

        if user.is_authenticated:

            if user.user_type == '1':

                if module_name == 'shortcourse_app.admin_view':
                    pass
                elif module_name == 'shortcourse_app.views' or module_name == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('admin_home'))

            elif user.user_type == '2':

                if module_name == 'shortcourse_app.instructor_view' or module_name == 'shortcourse_app.EditResultViewClass':
                    pass
                elif module_name == 'shortcourse_app.views' or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse('instructor_home'))

            elif user.user_type == '3':

                if module_name == 'shortcourse_app.student_view' or module_name == 'django.views.static':
                    pass
                elif module_name == 'shortcourse_app.views':
                    pass
                else:
                    return HttpResponseRedirect(reverse('student_home'))
            else:
                return HttpResponseRedirect(reverse('login_user'))

        else:
            if request.path == reverse('login_user') or request.path == reverse('do_login') or module_name == 'django.contrib.auth.views' or module_name == 'django.contrib.admin.sites':

                pass
            else:
                return HttpResponseRedirect(reverse('login_user'))

