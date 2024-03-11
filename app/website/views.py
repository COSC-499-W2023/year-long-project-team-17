from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from django.views import generic
from .decorators import *
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .forms import SignUpForm, EditProfileForm, ProfilePageForm
from .models import Profile, Message, Presentations
from util.generate_summary import generate_summary
from util.generate_presentation import generate_presentation
from util.detect_plagiarism import detect_plagiarism
from util.generate_exercises import generate_exercises_from_prompt, generate_similar_exercises
from util.adapt_content import generate_adapted_content
from util.modify_presentation import check_user_message, generate_modification_assistant_response, generate_modified_presentation
from django.http import FileResponse
from django.core.cache import cache
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from threading import Thread
from uuid import uuid4

import os
import docx
from pptx import Presentation
import PyPDF2
import logging
from django.http import HttpResponse, JsonResponse
import openai
from openai import OpenAI
import json
from django.contrib.auth.decorators import login_required
from django.db import models
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import get_usage, is_ratelimited
from humanfriendly import format_timespan
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from util import config
# Create your views here.
# logging.info("----"*100)
#
# logging.info(os.environ.get("OPENAI_API_KEY"))
# print("----"*100)
#
# print(os.environ.get("OPENAI_API_KEY"))

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class AboutUsView(CreateView):
    template_name = 'about_page.html'
    model = Profile
    form_class = ProfilePageForm
    # fields = '__all__'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def chat(request, username):
    receiver = User.objects.get(username=username)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    return render(request, 'chat.html', {'messages': messages, 'receiver': receiver})

@login_required
def send_message(request, username):
    if request.method == 'POST':
        receiver = User.objects.get(username=username)
        content = request.POST.get('content', '')

        if content:
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )

    return redirect('chat', username=username)

class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'create_user_profile_page.html'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
    success_url = reverse_lazy('home')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

def isLimited(request, exception):
    values = {}
    values['timeleft'] = 0

    if request.get_full_path() == "/":
        usage = get_usage(request, method=get_usage.ALL, key='post:username',
                       rate='5/5m', group='a')
        values['timeleft'] = format_timespan(usage['time_left'])
        return render(request, 'limited.html', values, status=429)
      
    elif request.get_full_path() == "/reset_password/":
        usage = get_usage(request, method=get_usage.ALL, key='ip', rate='8/5h', group='b')
        values['timeleft'] = format_timespan(usage['time_left'])
        return render(request, 'limited.html', values, status=429)

def faq(request):
    return render(request,'faq.html')

def contact_us(request):
    if request.method == 'POST':
        email = request.POST['email']
        message = request.POST['question']
        if(len(message) == 0):
            messages.error(request, "Please enter a question.")
            return render(request, 'contact_us.html')
        try:
            validate_email(email)
        except ValidationError as err:
            messages.error(request, "An invalid email address was entered please try again.")
            return render(request, 'contact_us.html')
        else:
            subject = 'Question from ' + email   
            #Sends question from user as email to noreplyeduprompt@gmail.com
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['noreplyeduprompt@gmail.com'],
                    fail_silently=False)
            messages.success(request, "Your question has been sent.")
            return render(request, 'contact_us.html')
        
    else:
        return render(request, 'contact_us.html')

@login_required
def get_presentations(request):
    results = Presentations.objects.filter(user_id = request.user).values('main_title','titles','date_created', 'is_shared').order_by('date_created')
    for item in results.values():
        print(item['main_title'])
        print(item['titles'])
        print(item['date_created'])
        print(item['is_shared'])
    return render(request, 'get_presentations.html')
    


@ratelimit(key='post:username', rate='5/5m',
           method=['POST'], group='a')
def home(request):


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
            messages.error(request, "There was an error logging in, please try again...")
            return redirect('home')
        
    else:
        return render(request, 'home.html')

@authenticated_user
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


#DELETE
def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')

#DELETE    
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
    
#DELETE
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

#DELETE
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

@authenticated_user
def generate_summary_view(request):
    
    if request.method == "POST":
        input_option = request.POST.get("input_option")
        if input_option == "write":

            input_text = request.POST.get("input_text")
            if input_text:
                summary = generate_summary(input_text)
                return render(request, 'summary_generation.html',
                                {'summary': summary,
                                "input_option": input_option})
            else:
                messages.error(request, "Please enter a text that you want to summarize")
                return render(request, "summary_generation.html", {"input_option": "write"})
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
                                            {"summary": summary,
                                            "input_option": input_option})
                        else:
                            messages.error(request,
                                            "You uploaded an empty .docx file.", {"input_option": "upload"})

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
                                            {"summary": summary,
                                            "input_option": input_option})
                        else:
                            messages.error(request,
                                            "You uploaded an empty .pptx file.", {"input_option": "upload"})

                    elif file_extension == ".txt":
                        txt_text = uploaded_file.read().decode('utf-8')
                        if txt_text:
                            summary = generate_summary(txt_text)
                            return render(request, "summary_generation.html",
                                            {"summary": summary,
                                            "input_option": input_option})
                        else:
                            messages.error(request,
                                            "You uploaded an empty .txt file.", {"input_option": "upload"})

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
                                            {"summary": summary,
                                            "input_option": input_option})
                        else:
                            messages.error(request,
                                            "You uploaded an empty .pdf file.", {"input_option": "upload"})
                else:
                    messages.error(request,
                                    "The Uploaded file must have one of the following extensions: .docs, .pptx, .txt, .pdf", {"input_option": "upload"})

            else:
                messages.error(request, "Please upload a file")
                render(request, "summary_generation.html", {"input_option": "upload"})
    return render(request, "summary_generation.html", {"input_option": "write"})

from reportlab.pdfgen import canvas

def pptx_to_pdf(pptx_file, pdf_file):
    # Load the PowerPoint presentation
    prs = Presentation(pptx_file)

    # Create a canvas with PDF size
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Set up dimensions
    width, height = letter
    slide_width = width - 72  # 1 inch margin on each side
    slide_height = height - 72

    # Go through each slide in the presentation
    for slide in prs.slides:
        # Start a new page for each slide
        c.showPage()

        # Draw the slide onto the canvas
        slide.shapes._spTree.draw(c, 0, 0, slide_width, slide_height)

    # Save the PDF
    c.save()

def generate_new_file_id():
    current_uuid = uuid4()
    cache.set("generated_presentation_id", str(current_uuid))
    return current_uuid

import subprocess
import platform
import os

def convert_pptx_to_pdf(input_path, output_path=None):
    # Ensure that the path to soffice is correct or adapt it
    # it might be different depending on how LibreOffice is installed
    system_platform = platform.system()
    if system_platform == 'Windows':
        libreoffice_path = 'C:/Program Files/LibreOffice/program/soffice.exe'
    elif system_platform == 'Darwin':  # macOS
        libreoffice_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    elif system_platform == 'Linux':
        libreoffice_path = '/usr/bin/soffice'  # Adjust this path according to your Linux distribution
    else:
        print("Unsupported operating system.")
        return

    if output_path is None:
        output_path = os.getcwd()
        print(output_path)

    command = [libreoffice_path, '--convert-to', 'pdf', '--outdir', output_path, input_path]

    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Conversion successful: '{input_path}' to PDF.")
    except Exception as e:
        print(f"Error converting file: {e}")


def presentation_generation_task(request, input_text):

    if "generated_presentation_filename" in request.session:
        request.session['generated_presentation_filename'] = None

    fs = FileSystemStorage()
    new_id = generate_new_file_id()
    filename = f'generated_presentation_{new_id}.pptx'  # Choose a unique filename if necessary
    if fs.exists(filename):
        fs.delete(filename)
    #presentation = generate_presentation(input_text)
    values = generate_presentation(input_text)
    presentation = values['presentation']
    pres_info = values['pres_info']
    pres = Presentations.objects.create(
        user = request.user,
        presentation = pres_info['presentation_json'],
        main_title = pres_info['main_title'],
        titles = pres_info['titles']
    )
    cache.set("generated_presentation_json", json.dumps(pres_info['presentation_json']))
    with fs.open(filename, 'wb') as pptx_file:
        presentation.save(pptx_file)
    request.session['generated_presentation_filename'] = filename
    pdf_filename = f'generated_presentation_{new_id}.pdf'
    if fs.exists(filename):
        pptx_file_path = fs.path(filename)
        pdf_file_path = fs.path(pdf_filename)
        # Popen(['unoconv', '-f', 'pdf', '-o', pdf_file_path, ppt_file_path]) #`sudo apt-get install -y unoconv
        # while not os.path.exists(pdf_file_path):
        #     time.sleep(1)
        # pptx_to_pdf(pptx_file_path, pdf_file_path)

        convert_pptx_to_pdf(pptx_file_path)


@authenticated_user
def generate_presentation_view(request):

    if request.method == "POST":
        input_option = request.POST.get("input_option")
        if input_option == "write":
            input_text = request.POST.get("input_text")
            if input_text:
                thread = Thread(target=presentation_generation_task, args=(request, input_text))
                thread.start()

                return JsonResponse({'status': 'success', 'message': 'Presentation generated'})
            else:
                messages.error(request, "Please enter text for the presentation")
                return render(request, "presentation_generation.html", {"input_option": "write"})
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
                            # presentation = generate_presentation()
                            # response = HttpResponse(
                            #     content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                            # response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                            # presentation.save(response)
                            # return response
                            input_text = "I want a presentation based on the following content:\n" + str(document_text)
                            thread = Thread(target=presentation_generation_task, args=(request, input_text))
                            thread.start()

                            return JsonResponse({'status': 'success', 'message': 'Presentation generated'})
                        else:
                            messages.error(request, "You uploaded an empty .docx file.", {"input_option": "upload"})

                    elif file_extension == ".txt":
                        txt_text = uploaded_file.read().decode('utf-8')
                        if txt_text:
                            # presentation = generate_presentation(
                            #     "I want a presentation based on the following content:\n" + str(txt_text))
                            # response = HttpResponse(
                            #     content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                            # response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                            # presentation.save(response)
                            # return response
                            input_text = "I want a presentation based on the following content:\n" + str(txt_text)
                            thread = Thread(target=presentation_generation_task, args=(request, input_text))
                            thread.start()

                            return JsonResponse({'status': 'success', 'message': 'Presentation generated'})
                        else:
                            messages.error(request,
                                            "You uploaded an empty .txt file.", {"input_option": "upload"})

                    elif file_extension == ".pdf":
                        pdf_content = uploaded_file
                        pdf_file = PyPDF2.PdfReader(pdf_content)
                        pdf_text = ""

                        for page_num in range(len(pdf_file.pages)):
                            page = pdf_file.pages[page_num]
                            pdf_text += page.extract_text()

                        if pdf_text:
                            # presentation = generate_presentation(
                            #     "I want a presentation based on the following content:\n" + str(pdf_text))
                            # response = HttpResponse(
                            #     content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                            # response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                            # presentation.save(response)
                            # return response
                            input_text = "I want a presentation based on the following content:\n" + str(pdf_text)
                            thread = Thread(target=presentation_generation_task, args=(request, input_text))
                            thread.start()

                            return JsonResponse({'status': 'success', 'message': 'Presentation generated'})
                        else:
                            messages.error(request,
                                            "You uploaded an empty .pdf file.", {"input_option": "upload"})
                else:
                    messages.error(request,
                                    "The Uploaded file must have one of the following extensions: .docs, .pptx, .txt, .pdf", {"input_option": "upload"})

            else:
                messages.error(request, "Please upload a file", {"input_option": "upload"})

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
    return render(request, "presentation_generation.html", {"input_option": "write"})
    

@authenticated_user
@allowed_users(allowed_roles=['teacher'])
def detect_plagiarism_view(request):
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


@authenticated_user
def generate_exercise_view(request):

        if request.method == "POST":
            input_option = request.POST.get("input_option")
            if input_option == "write":
                input_text = request.POST.get("input_text")
                if input_text:
                    generated_exercises = generate_exercises_from_prompt(input_text)
                    return render(request, 'exercise_generation.html',
                                    {'generated_exercises': generated_exercises,
                                    "input_option": input_option})
                else:
                    messages.error(request, "Please describe what type of exercises do you want.")
                    return render(request, "exercise_generation.html", {"input_option": "write"})
            elif input_option == "upload":
                uploaded_file = request.FILES.get("file")
                if uploaded_file:
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    if file_extension not in [".docx", ".pdf"]:
                        messages.error(request,
                                        "The uploaded file must have one of the following extensions: .docx, .pdf")
                        return render(request, "exercise_generation.html", {"input_option": "upload"})
                    elif file_extension == ".docx":
                            doc = docx.Document(uploaded_file)
                            full_text = []
                            for paragraph in doc.paragraphs:
                                full_text.append(paragraph.text)

                            document_text = "\n".join(full_text)
                            if document_text.strip():
                                similar_exercises = generate_similar_exercises(document_text)
                                return render(request, "exercise_generation.html",
                                                {"generated_exercises": similar_exercises,
                                                "input_option": input_option})
                            else:
                                messages.error(request,
                                                "You uploaded an empty .docx file.")
                    elif file_extension == ".pdf":
                        pdf_content = uploaded_file
                        pdf_file = PyPDF2.PdfReader(pdf_content)
                        pdf_text = ""

                        for page_num in range(len(pdf_file.pages)):
                            page = pdf_file.pages[page_num]
                            pdf_text += page.extract_text()

                        if pdf_text.strip():
                            similar_exercises = generate_similar_exercises(pdf_text)
                            return render(request, "exercise_generation.html",
                                            {"generated_exercises": similar_exercises,
                                            "input_option": input_option})
                        else:
                            messages.error(request,
                                            "You uploaded an empty .pdf file.")
                else:
                    messages.error(request,
                                    "Please upload a file before Pressing the button. The uploaded file must have one of the following extensions: .docx, .pdf")
                    return render(request, "exercise_generation.html", {"input_option": "upload"})
        return render(request, "exercise_generation.html", {"input_option": "write"})
    
@authenticated_user
def chatbot_view(request):
    chat_history = request.session.get('chat_history', [])

    if request.method == "POST":
        message = request.POST.get('message')
        chat_history_string = ""
        if chat_history:
            chat_history_string = "\n".join([f'User: {entry.get("USER")}\nAI: {entry.get("AI")}' for entry in chat_history])
        response = get_chatbot_response(chat_history_string, message)

        chat_history.append({'USER': message, 'AI': response})

        # Store the updated chat history in the session
        request.session['chat_history'] = chat_history

        return JsonResponse({'message': message, 'response': response})
    return render(request, "chatbot.html")



def get_chatbot_response(chat_history: str, request: str):
    response = ""
    try:
        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.WEBSITE_DESCRIPTION_FOR_CHATBOT}.\n This is your chat history: {chat_history}. \nUSER:{request}\nYour Response:'}
            ],

        )
        final_response = response.choices[0].message.content

        logging.info(final_response)
        return final_response

    except Exception as e:
        logging.info(response.choices[0].message.content)
        logging.info("something went wrong with generating exercises based on the provided prompt.")
        logging.error(e)


@authenticated_user
def generate_adapted_content_view(request):
    if request.method == "POST":
        input_option = request.POST.get("input_option")
        if input_option == "write":
            input_text = request.POST.get("input_text")
            input_user_group = request.POST.get("input_user_group")
            if input_text:
                adapted_content = generate_adapted_content(input_text, input_user_group)

                return render(request, 'adapted_content_generation.html',
                                          {'adapted_content': adapted_content,
                                           "input_option": input_option})
            else:
                messages.error(request, "Please enter text that needs to be adapted for the target user group")
                return render(request, "adapted_content_generation.html")
        elif input_option == "upload":
            uploaded_file = request.FILES.get("file")
            input_user_group = request.POST.get("input_user_group")
            if uploaded_file:
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()

                if file_extension in [".docx", ".pdf", ".pptx"]:
                    if file_extension == ".docx":
                        doc = docx.Document(uploaded_file)
                        full_text = []
                        for paragraph in doc.paragraphs:
                            full_text.append(paragraph.text)

                        document_text = "\n".join(full_text)
                        if document_text:
                            adapted_content = generate_adapted_content(document_text, input_user_group)

                            document = docx.Document()

                            document.add_heading(f"Document for: {input_user_group}", level=1)
                            document.add_paragraph(str(adapted_content))

                            response = HttpResponse(
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                            response['Content-Disposition'] = 'attachment; filename="generated_document.docx"'

                            document.save(response)
                            return response
                        else:
                            messages.error(request, "You uploaded an empty .docx file.")

                    elif file_extension == ".pdf":
                        pdf_content = uploaded_file
                        pdf_file = PyPDF2.PdfReader(pdf_content)
                        pdf_text = ""

                        for page_num in range(len(pdf_file.pages)):
                            page = pdf_file.pages[page_num]
                            pdf_text += page.extract_text()

                        if pdf_text:
                            adapted_content = generate_adapted_content(pdf_text, input_user_group)

                            response = HttpResponse(content_type='application/pdf')
                            response['Content-Disposition'] = 'attachment; filename="generated_document.pdf"'

                            pdf_buffer = response

                            styles = getSampleStyleSheet()

                            story = []

                            title = f"Document for: {input_user_group}"
                            story.append(Paragraph(title, styles['Title']))

                            story.append(Spacer(1, 12))

                            content_paragraphs = adapted_content.split('\n')
                            for paragraph in content_paragraphs:
                                story.append(Paragraph(paragraph, styles['Normal']))

                            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                            doc.build(story)
                            return response
                        else:
                            messages.error(request,
                                            "You uploaded an empty .pdf file.")

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
                            uploaded_content_summary = generate_summary(presentation_text)
                            adapted_content = generate_adapted_content(uploaded_content_summary, input_user_group)

                            presentation = generate_presentation(
                                f"Generate a presentation using the following content. The content is designed for: {input_user_group}. Do not forget to use images when appropriate to make the presentation more entertaining. Your images must be illustrative for the user group. The content is the following:\n" + str(adapted_content))
                            response = HttpResponse(
                                content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                            response['Content-Disposition'] = 'attachment; filename="generated_presentation.pptx"'
                            presentation.save(response)

                            return response
                        else:
                            messages.error(request,
                                            "You uploaded an empty .pptx file.")
                else:
                    messages.error(request,
                                    "The Uploaded file must have one of the following extensions: .docs, .pptx, .txt, .pdf")

            else:
                messages.error(request, "Please upload a file")

    return render(request, "adapted_content_generation.html")


def loading_page_view(request):
    return render(request, "loading_page.html", {})


def presentation_download(request):

    presentation_id = cache.get("generated_presentation_id", "000")
    filename = f'generated_presentation_{presentation_id}.pptx'
    if filename:
        fs = FileSystemStorage()
        if fs.exists(filename):
            response = FileResponse(fs.open(filename, 'rb'), content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            #fs.delete(filename)
            fs.delete(filename)
            cache.clear()

            return response

    messages.error(request, "No presentation was generated or the session has expired.")
    return render(request, "presentation_generation.html")


def presentation_status(request):

    presentation_id = cache.get("generated_presentation_id", "000")
    filename = f'generated_presentation_{presentation_id}.pptx'
    fs = FileSystemStorage()

    if fs.exists(filename):
        return JsonResponse({'status': 'ready'})
    else:
        return JsonResponse({'status': 'pending'})

from django.templatetags.static import static


def presentation_preview(request):
    presentation_id = cache.get("generated_presentation_id", "000")
    filename = f'generated_presentation_{presentation_id}.pdf'  # Assuming conversion to PDF is done.
    fs = FileSystemStorage()

    if fs.exists(filename):

        # pdf_url = fs.url(filename)
        pdf_url = '/' + fs.base_url.lstrip('/') + filename

        return render(request, "presentation_preview.html", {"presentation_pdf_url": pdf_url})
    else:
        messages.error(request, "No presentation was ready for preview.")
        return redirect('generate_presentation')



from django.http import HttpResponse
from django.conf import settings
import os


def view_pdf(request):
    # Path to the PDF file
    # pdf_path = 'my_presentation.pdf'
    presentation_id = cache.get("generated_presentation_id", "000")
    pdf_path = f'generated_presentation_{presentation_id}.pdf'
    fs = FileSystemStorage()
    if fs.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()

    # Return the PDF content as the HTTP response
        fs.delete(pdf_path)
        return HttpResponse(pdf_data, content_type='application/pdf')
    else:
        messages.error(request, "Something went wrong while generating your presentation, please try again.")
        return redirect('generate_presentation')


def handle_modification_message(request):
    logging.info("IN HANDLE MODIFICATION")
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Call your function to check user message
        modify_presentation = check_user_message(user_message)

        if modify_presentation:
            # Call your modify_presentation function here
            # Example: modify_presentation(user_message)
            response_data = {'modifyPresentation': True}
        else:
            # Call your function to answer user message
            # Example: response = answer_user_message(user_message)
            modification_assistant_answer = generate_modification_assistant_response(user_message)
            response_data = {'modifyPresentation': False, 'response': modification_assistant_answer}

        return JsonResponse(response_data)


def modify_presentation(request):
    logging.info("IN MODIFY PRESENTATION")
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        generated_presentation_json = cache.get("generated_presentation_json", "{}")
        logging.info(f"GENERATED PRESENTATION JSON: {generated_presentation_json}")
        generated_presentation_json = json.loads(generated_presentation_json)
        modified_presentation_json, modified_presentation_object = generate_modified_presentation(generated_presentation_json, user_message)
        cache.set("generated_presentation_json", json.dumps(modified_presentation_json))
        presentation_id = cache.get("generated_presentation_id", "000")
        filename = f'generated_presentation_{presentation_id}.pptx'
        fs = FileSystemStorage()
        if fs.exists(filename):
            pass
        with fs.open(filename, 'wb') as pptx_file:
            modified_presentation_object.save(pptx_file)

        if fs.exists(filename):
            pptx_file_path = fs.path(filename)
            convert_pptx_to_pdf(pptx_file_path)

        pdf_path = f'generated_presentation_{presentation_id}.pdf'

        if fs.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()

            # Return the PDF content as the HTTP response
            fs.delete(pdf_path)
            return HttpResponse(pdf_data, content_type='application/pdf')
        else:
            messages.error(request, "Something went wrong while generating your modified presentation, please try again.")
            return redirect('generate_presentation')
