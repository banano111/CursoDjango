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
        """ first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        gender= request.POST['gender']
        date_birth = request.POST['date_birth']

        if not date_birth:
            date_birth = None
        
        new_user = UserModel.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            gender = gender,
            date_birth = date_birth
        )

        if new_user:
            messages.success(request, 'Usuario Creado Exitosamente!')
            return redirect('/main')
        else:
            messages.error(request, 'Algo Fallo al momento de crear un usuario')
            return render(request, self.template_name) """

        new_form = UserForm(request.POST)
        if new_form.is_valid():
            form_data = new_form.save(commit=False)
            form_data.save()
            messages.success(request, 'Usuario Creado Exitosamente!')
            return redirect('/main')
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
        # user.first_name = request.POST['first_name']
        # user.last_name = request.POST['last_name']
        # user.email = request.POST['email']
        # user.phone_number = request.POST['phone_number']
        # user.gender = request.POST['gender']
        # user.date_birth = request.POST['date_birth']
        # user.save()
        # messages.success(request, 'Usuario Actualizado Exitosamente!')
        # return redirect('/main/' + str(id))
        edit_form =UserForm(request.POST, instance=user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Usuario Actualizado Exitosamente!')
            return redirect('/main/' +  str(id))
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
    return redirect('/main/')