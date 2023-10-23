from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

from .decorators import *
from .forms import SignUpForm, AddRecordForm
from .models import Record
from util.generate_summary import generate_summary
from util.generate_presentation import generate_presentation
from util.detect_plagiarism import detect_plagiarism

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

@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            groupName = form.cleaned_data['user_group']
            group = Group.objects.get(name=groupName)
            user = authenticate(username = username, password = password)
            user.groups.add(group)
            login(request, user)
            messages.success(request, "You have succesfully registered")
            return redirect('home')
        else:
            return render(request, 'register.html', {'form':form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')
    
@allowed_users(allowed_roles=['teacher'])
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "The customer has been deleted succesfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in do that action")
        return redirect('home')
    

@allowed_users(allowed_roles=['teacher'])
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

@allowed_users(allowed_roles=['teacher'])
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


@allowed_users(allowed_roles=['teacher'])
def detect_plagiarism_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            uploaded_files = request.FILES.getlist('file')
            if uploaded_files and len(uploaded_files) > 1:
                for uploaded_file in uploaded_files:
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    if file_extension not in [".docx", ".pdf"]:
                        messages.error(request, "The uploaded files must have one of the following extensions: .docx, .pdf")
                        return render(request, "plagiarism_detection.html")
                uploaded_files_names = []
                uploaded_files_texts = []
                for uploaded_file in uploaded_files:
                    uploaded_files_names.append(uploaded_file.name)
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    if file_extension == ".docx":
                        doc = docx.Document(uploaded_file)
                        full_text = []
                        for paragraph in doc.paragraphs:
                            full_text.append(paragraph.text)

                        document_text = "\n".join(full_text)
                        if document_text.strip():
                            uploaded_files_texts.append(document_text)
                            print(document_text)
                        else:
                            messages.error(request,
                                           "You uploaded an empty .docx file. The file name is the following: " + uploaded_file.name)
                            return render(request, "plagiarism_detection.html")

                    elif file_extension == ".pdf":
                        pdf_content = uploaded_file
                        pdf_file = PyPDF2.PdfReader(pdf_content)
                        pdf_text = ""

                        for page_num in range(len(pdf_file.pages)):
                            page = pdf_file.pages[page_num]
                            pdf_text += page.extract_text()

                        if pdf_text.strip():
                            uploaded_files_texts.append(pdf_text)
                            print(pdf_text)
                        else:
                            messages.error(request,
                                           "You uploaded an empty .pdf file. The file name is the following: " + uploaded_file.name)
                            return render(request, "plagiarism_detection.html")

                plagiarised_files = []
                similarity_for_each_file_pair = []
                if uploaded_files_texts:
                    plagiarism_pairs, all_similarity_scores = detect_plagiarism(uploaded_files_texts, 0.85)
                    print(plagiarism_pairs)
                    print(all_similarity_scores)
                    if plagiarism_pairs:
                        for plag_pairs in plagiarism_pairs:
                            plagiarised_files.append((uploaded_files_names[plag_pairs[0]], uploaded_files_names[plag_pairs[1]], plag_pairs[2]*100))
                    if all_similarity_scores:
                        for sim_score in all_similarity_scores:
                            similarity_for_each_file_pair.append((uploaded_files_names[sim_score[0]], uploaded_files_names[sim_score[1]], sim_score[2]*100))
                if plagiarised_files:
                    print(plagiarised_files)
                if similarity_for_each_file_pair:
                    print(similarity_for_each_file_pair)

                return render(request, "plagiarism_detection.html",
                              {"plagiarised_files": plagiarised_files, "all_similarities": similarity_for_each_file_pair})

            elif len(uploaded_files) == 1:
                messages.error(request, "Please upload more than one file.")
                return render(request, "plagiarism_detection.html")
            else:
                messages.error(request, "Please upload files before clicking the button. The number of files should be at least two.")
                return render(request, "plagiarism_detection.html")
        return render(request, "plagiarism_detection.html")
    else:
        messages.success(request, "You must be logged in to view that page...")
        return redirect('home')
