from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from util.generate_summary import generate_summary
from util.generate_presentation import generate_presentation
import os
import docx
from pptx import Presentation
import PyPDF2
import logging
from django.http import HttpResponse
# Create your views here.

def home(request):
    records = Record.objects.all()


    #check to see if logging in
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, please try again...")
            return redirect('home')
        
    else:
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out...")
    return redirect('home')

def register_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                #Authenticate and login
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username = username, password = password)
                login(request, user)
                messages.success(request, "You have succesfully registered")
                return redirect('home')
        else:
            form = SignUpForm()
            return render(request, 'register.html', {'form':form})
        return render(request, 'register.html', {'form':form})
    else:
        messages.success(request, "You have already registered an account")
        return redirect('home')


def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "The customer has been deleted succesfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in do that action")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')

        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance = current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')

def generate_summary_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            input_option = request.POST.get("input_option")
            if input_option == "write":

                input_text = request.POST.get("input_text")
                if input_text:
                    summary = generate_summary(input_text)
                    return render(request, 'summary_generation.html',
                                  {'summary': summary["choices"][0]["message"]["content"],
                                   "input_option": input_option})
                else:
                    messages.error(request, "Please enter a text")
                    return render(request, "summary_generation.html")
            elif input_option == "upload":
                uploaded_file = request.FILES.get("file")

                if uploaded_file:
                    logging.info("Upload")
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    print(file_extension)
                    if file_extension in [".txt", ".pptx", ".docx", ".pdf"]:
                        if file_extension == ".docx":
                            doc = docx.Document(uploaded_file)
                            full_text = []
                            for paragraph in doc.paragraphs:
                                full_text.append(paragraph.text)

                            document_text = "\n".join(full_text)
                            if document_text:
                                summary = generate_summary(document_text)
                                return render(request, "summary_generation.html",
                                              {"summary": summary["choices"][0]["message"]["content"],
                                               "input_option": input_option})
                            else:
                                messages.error(request,
                                               "You uploaded an empty .docx file.")

                        elif file_extension == ".pptx":
                            presentation = Presentation(uploaded_file)

                            slide_text = []

                            for slide in presentation.slides:
                                slide_text.append("")
                                for shape in slide.shapes:
                                    if hasattr(shape, "text"):
                                        slide_text.append(shape.text)

                            presentation_text = "\n".join(slide_text)
                            if presentation_text:
                                summary = generate_summary(presentation_text)
                                return render(request, "summary_generation.html",
                                              {"summary": summary["choices"][0]["message"]["content"],
                                               "input_option": input_option})
                            else:
                                messages.error(request,
                                               "You uploaded an empty .pptx file.")

                        elif file_extension == ".txt":
                            txt_text = uploaded_file.read().decode('utf-8')
                            if txt_text:
                                summary = generate_summary(txt_text)
                                return render(request, "summary_generation.html",
                                              {"summary": summary["choices"][0]["message"]["content"],
                                               "input_option": input_option})
                            else:
                                messages.error(request,
                                               "You uploaded an empty .txt file.")

                        elif file_extension == ".pdf":
                            pdf_content = uploaded_file
                            pdf_file = PyPDF2.PdfReader(pdf_content)
                            pdf_text = ""

                            for page_num in range(len(pdf_file.pages)):
                                page = pdf_file.pages[page_num]
                                pdf_text += page.extract_text()

                            if pdf_text:
                                summary = generate_summary(pdf_text)
                                return render(request, "summary_generation.html",
                                              {"summary": summary["choices"][0]["message"]["content"],
                                               "input_option": input_option})
                            else:
                                messages.error(request,
                                               "You uploaded an empty .pdf file.")
                    else:
                        messages.error(request,
                                       "The Uploaded file must have one of the following extensions: .docs, .pptx, .txt, .pdf")

                else:
                    messages.error(request, "Please upload a file")

        return render(request, "summary_generation.html", {"input_option": "write"})
    else:
        messages.success(request, "You must be logged in....")
        return redirect("home")


def generate_presentation_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            input_option = request.POST.get("input_option")
            if input_option == "write":
                input_text = request.POST.get("input_text")
                if input_text:
                    presentation = generate_presentation(input_text)
                    response = HttpResponse(
                        content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                    response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                    presentation.save(response)
                    return response
                else:
                    messages.error(request, "Please enter text for the presentation")
                    return render(request, "presentation_generation.html")
            elif input_option == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

                    if file_extension in [".txt", ".docx", ".pdf"]:
                        if file_extension == ".docx":
                            doc = docx.Document(uploaded_file)
                            full_text = []
                            for paragraph in doc.paragraphs:
                                full_text.append(paragraph.text)

                            document_text = "\n".join(full_text)
                            if document_text:
                                presentation = generate_presentation("I want a presentation based on the following content:\n" + str(document_text))
                                response = HttpResponse(
                                    content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                                response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                                presentation.save(response)
                                return response
                            else:
                                messages.error(request, "You uploaded an empty .docx file.")

                        elif file_extension == ".txt":
                            txt_text = uploaded_file.read().decode('utf-8')
                            if txt_text:
                                presentation = generate_presentation(
                                    "I want a presentation based on the following content:\n" + str(txt_text))
                                response = HttpResponse(
                                    content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                                response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                                presentation.save(response)
                                return response
                            else:
                                messages.error(request,
                                               "You uploaded an empty .txt file.")

                        elif file_extension == ".pdf":
                            pdf_content = uploaded_file
                            pdf_file = PyPDF2.PdfReader(pdf_content)
                            pdf_text = ""

                            for page_num in range(len(pdf_file.pages)):
                                page = pdf_file.pages[page_num]
                                pdf_text += page.extract_text()

                            if pdf_text:
                                presentation = generate_presentation(
                                    "I want a presentation based on the following content:\n" + str(pdf_text))
                                response = HttpResponse(
                                    content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                                response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                                presentation.save(response)
                                return response
                            else:
                                messages.error(request,
                                               "You uploaded an empty .pdf file.")
                    else:
                        messages.error(request,
                                       "The Uploaded file must have one of the following extensions: .docs, .pptx, .txt, .pdf")

                else:
                    messages.error(request, "Please upload a file")

                # if input_text:
                #     presentation = generate_presentation(input_text)  # Modify this line to generate the presentation
                #     if presentation:
                #         # Save the presentation to a temporary file
                #         presentation_path = "path_to_temporary_file.pptx"
                #         presentation.save(presentation_path)
                #         return render(request, 'presentation_generation.html', {'presentation_link': presentation_path})
                #     else:
                #         messages.error(request, "Failed to generate presentation.")
                # else:
                #     messages.error(request, "Please enter text for the presentation")
                #     return render(request, "presentation_generation.html")
        return render(request, "presentation_generation.html")
    else:
        messages.success(request, "You must be logged in to view that page...")
        return redirect('home')
