from django.shortcuts import render, redirect
from django import views
from .models import UserModel
from .forms import UserForm, ProfileForm
from django.contrib import messages

class GetUsersView (views.View):
    def get(self, request):
        users = UserModel.objects.all()
        # Es algo parecido a SELECT * FROM USERS
        template_name = 'main/list.html'
        context = {
            'users': users
        }
        return render(request, template_name, context)

def GetUserView(request, id):
    user = UserModel.objects.get(pk=id)
    # Es algo parecido a SELECT * FROM USERS WHERE pk = id
    template_name = 'main/detail.html'
    context = {
        'user': user
    }

    return render(request, template_name, context)

class CreateUserView(views.View):
    template_name = 'main/form.html'
    action = 'create'
    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'action': self.action
        }
        return render(request, self.template_name, context)

    def post(self, request):
        new_user_form = UserForm(request.POST)
        new_profile_form = ProfileForm(request.POST, request.FILES)
        if new_user_form.is_valid() & new_profile_form.is_valid():
            user_form_data = new_user_form.save()
            profile_form_data = new_profile_form.save(commit=False)
            profile_form_data.user = user_form_data
            profile_form_data.save()
            messages.success(request, 'Usuario Creado Exitosamente!')
            return redirect('user:list')
        else:
            errors = new_user_form.errors.as_data()
            print(errors)
            form = UserForm()
            context = {
                'user_form': new_user_form,
                'profile_form': new_profile_form,
                'action': self.action
            }
            messages.error(request, 'Algo Fallo al momento de crear un usuario')
            return render(request, self.template_name, context)


class UpdateUserView(views.View):
    template_name = 'main/form.html'
    action = 'update'
    def get(self, request, id):
        user = UserModel.objects.get(id=id)
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        context = {
            'user': user,
            'user_form': user_form,
            'profile_form': profile_form,
            'action': self.action
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        user = UserModel.objects.get(id=id)
        edit_user_form = UserForm(request.POST, instance=user)
        edit_profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile) 
        if edit_user_form.is_valid() & edit_profile_form.is_valid():
            edit_user_data = edit_user_form.save()
            edit_profile_data = edit_profile_form.save()
            messages.success(request, 'Usuario Actualizado Exitosamente!')
            return redirect('user:detail', id)
        else:
            errors = edit_form.errors.as_data()
            user = UserModel.objects.get(id=id)
            user_form = UserForm(instance=user)
            profile_form = ProfileForm(instance=user.profile)
            context = {
                'user': user,
                'user_form': user_form,
                'profile_form': profile_form,
                'action': self.action
            }
            messages.error(request, 'Algo Fallo al editar la información del usuario')
            return render(request, self.template_name, context)



def DeleteUserView(request, id):
    user = UserModel.objects.get(id=id)
    user.delete()
    messages.success(request, 'Usuario Eliminado Exitosamente!')
    return redirect('user:list')