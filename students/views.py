from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Student


def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})


def student_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if Student.objects.filter(email=email).exists():
            messages.error(request, "This email already exists!")
            return redirect('student_create')

        try:
            Student.objects.create(
                name=name,
                email=email,
                gender=gender,
                phone=phone
            )
            messages.success(request, "Student added successfully.")
            return redirect('student_list')

        except IntegrityError:
            messages.error(request, "This email already exists!")
            return redirect('student_create')

    return render(request, 'students/create.html')


def student_edit(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if Student.objects.filter(email=email).exclude(id=id).exists():
            messages.error(request, "This email already exists!")
            return redirect('student_edit', id=id)

        try:
            student.name = name
            student.email = email
            student.gender = gender
            student.phone = phone
            student.save()

            messages.success(request, "Student updated successfully.")
            return redirect('student_list')

        except IntegrityError:
            messages.error(request, "This email already exists!")
            return redirect('student_edit', id=id)

    return render(request, 'students/edit.html', {'student': student})


def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('student_list')
