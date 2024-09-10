from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt
import os


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'Authentication/login.html')



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')
    return render(request, 'Authentication/register.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  
    return redirect('login')









def terminal_view(request):
    return render(request, 'Authentication/terminal.html')

# @login_required
# @csrf_exempt
# def run_command_view(request):
#     if request.method == "POST":
#         command = request.POST.get("command")
#         if command:
#             try:
#                 result = subprocess.run(command, shell=True, capture_output=True, text=True)
#                 if result.returncode != 0:
#                     output = f"Error: {result.stderr}"
#                 else:
#                     output = result.stdout
#             except Exception as e:
#                 output = f"Exception: {str(e)}"
#         else:
#             output = "No command provided."
#         return JsonResponse({"output": output})
#     return JsonResponse({"output": "Invalid request method."})






@csrf_exempt
def run_command_view(request):
    if request.method == "POST":
        command = request.POST.get("command")
        if command:
            try:
                # Determine the home directory based on the operating system
                if os.name == 'nt':  # Windows
                    home_dir = os.environ.get('USERPROFILE', '')
                else:  # Unix/Linux/macOS
                    home_dir = os.environ.get('HOME', '')

                # Replace `~` with the home directory in the command
                if home_dir:
                    command = command.replace('~', home_dir)

                # Run the command
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
                
                if result.returncode != 0:
                    output = f"Error: {result.stderr.strip()}"
                else:
                    output = result.stdout.strip()
                
                return JsonResponse({"output": output}, status=200)
            except subprocess.CalledProcessError as e:
                return JsonResponse({"output": f"Subprocess Error: {str(e)}"}, status=500)
            except subprocess.TimeoutExpired as e:
                return JsonResponse({"output": f"Command timed out: {str(e)}"}, status=500)
            except Exception as e:
                return JsonResponse({"output": f"Exception: {str(e)}"}, status=500)
        else:
            return JsonResponse({"output": "No command provided."}, status=400)
    return JsonResponse({"output": "Invalid request method."}, status=405)