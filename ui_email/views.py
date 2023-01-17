from django.shortcuts import render , redirect ,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import smtplib , ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import gspread
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def index(request):
    return render(request , 'index.html')

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        try:
            if form.is_valid():
                form.save()
                messages.success(request ,'New User Created! Please Login in')
                return redirect('/')
        except Exception as e:
            print(e)
    else:
        form = UserCreationForm()

    return render(request , 'signup_page.html', {'form': form})

@csrf_protect
@login_required
def home(request):
    if request.method == 'POST':
        sub = request.POST.get('Subject')
        msgg = request.POST.get('Message')
        files = request.FILES.getlist('filesss')
        print(files)
        gc = gspread.service_account(filename='sheetAuth3.json')
        wks = gc.open('Bulk emails_M Joseph John').sheet1
        li = []
        ln =[]
        for i in wks.get_all_records():
            if i['Email ID'] != '': 
                try:
                    print(type(msgg))
                    msggg = eval(f"f'''{msgg}'''")
                    print(msggg)
                    msg = MIMEMultipart()
                    msg['From'] = 'mjosephjohn@cmcludhiana.in'
                    msg['To'] = i['Email ID']
                    msg['Subject'] = sub
                    msg.attach(MIMEText(msggg))
                    for fi in files:
                        part = MIMEBase('application', "octet-stream")
                        part.set_payload(fi.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment', filename = fi.name)
                        msg.attach(part)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com" , 465 , context=context) as server:
                        server.ehlo()
                        server.login(msg['From'], 'amoowrldoigqmfdc')
                        server.sendmail(msg['From'], msg['To'], msg.as_string())
                        server.quit()
                    print(f"mail has been sent to : {i['Email ID']}")
                    li.append(i['Email ID']) 
                except Exception as e:
                    print(e)
                    print(f"mail has nott been sent to : {i['Email ID']}")
                    ln.append(i['Email ID']) 
        context ={'li' :li,'ln':ln}
        return render(request , 'sentt.html' , context)
    gc = gspread.service_account(filename='sheetAuth3.json')
    wks = gc.open('Bulk emails_M Joseph John').sheet1
    contextt={}
    for i in wks.get_all_values()[0]:
        contextt[i] =i 
    print(contextt)
    return render(request,'home.html' ,{'contextt':contextt})