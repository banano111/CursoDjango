from django.shortcuts import render, redirect
from django import views
from .models import UserModel
from .forms import UserForm
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
        form = UserForm()
        context = {
            'form': form,
            'action': self.action
        }
        return render(request, self.template_name, context)

    def post(self, request):
        new_form = UserForm(request.POST)
        if new_form.is_valid():
            form_data = new_form.save(commit=False)
            form_data.save()
            messages.success(request, 'Usuario Creado Exitosamente!')
            return redirect('user:list')
        else:
            errors = new_form.errors.as_data()
            print(errors)
            form = UserForm()
            context = {
                'form': form,
                'action': self.action
            }
            messages.error(request, 'Algo Fallo al momento de crear un usuario')
            return render(request, self.template_name, context)


class UpdateUserView(views.View):
    template_name = 'main/form.html'
    action = 'update'
    def get(self, request, id):
        user = UserModel.objects.get(id=id)
        form = UserForm(instance=user)
        context = {
            'user': user,
            'action': self.action,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        user = UserModel.objects.get(id=id)

        edit_form =UserForm(request.POST, instance=user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Usuario Actualizado Exitosamente!')
            return redirect('user:detail', id)
        else:
            errors = edit_form.errors.as_data()
            print(errors)
            form = UserForm(instance=user)
            context = {
                'form': form,
                'action': self.action,
                'user': user
            }
            messages.error(request, 'Algo Fallo al editar la información del usuario')
            return render(request, self.template_name, context)



def DeleteUserView(request, id):
    user = UserModel.objects.get(id=id)
    user.delete()
    messages.success(request, 'Usuario Eliminado Exitosamente!')
    return redirect('user:list')