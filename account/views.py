### account/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import *
import pandas as pd


## Home Page
def home(request):
    # All Accounts
    accounts = Profile.objects.all()
    # accounts.delete()

    if request.method == "GET":
        search_query = request.GET.get('name')
        if search_query:
            accounts = Profile.objects.filter(name__icontains=search_query)
        else:
            pass
        context = {
            'accounts': accounts,
        }
        return render(request, "home/index.html", context)

    if request.method == "POST":
        try:
            # Read File
            file = request.FILES['csv_file']

            # Convert File to dictionaries
            data = convert_file(file)

            # Check File is CSV or XLSX File
            if data:
                # Save Data in Model
                for acc in data:
                    if not Profile.objects.filter(id=acc['ID']).exists():
                        Profile.objects.create(
                            id=acc['ID'],
                            name=acc['Name'],
                            balance=acc['Balance'],
                        )
                    else:
                        pass

                # Render all Users
                accounts = Profile.objects.all()
                context = {
                    'accounts': accounts,
                }
                return render(request, "home/index.html", context)
            
            # Check File is Not CSV File
            else:
                error_msg = "Please upload a valid CSV or XLSX file."
                context = {
                    'accounts': accounts,
                    'error_msg': error_msg,
                }
                return render(request, "home/index.html", context)
        except:
            # Check if file is provided
            error_msg = "Please select a file."
            context = {
                'accounts': accounts,
                'error_msg': error_msg,
            }
            return render(request, "home/index.html", context)


## Profile
def profile(request, user_id):
    accounts = Profile.objects.all()
    user_profile = Profile.objects.filter(id=user_id).first()

    if request.method == "GET":
        context = {
            'accounts': accounts,
            'user_profile': user_profile,
        }
        return render(request, "profile/profile.html", context)

    if request.method == "POST":
        receiver_id = request.POST.get('receiver')
        amount = request.POST.get('amount')
        amount = Decimal(amount)
        
        # Update Sender and Receiver Profile
        sender = Profile.objects.get(id=user_profile.id)
        receiver = Profile.objects.get(id=receiver_id)

        if sender.id ==  receiver.id:
            messages.error(request, "Can't Send Money to youself!")
            return redirect('profile', user_id=user_id)
        else:
            if sender.balance >= amount:
                # Update Balance in Sender Model
                sender.balance -= amount
                sender.save()

                # Update Balance in Receiver Model
                receiver.balance += amount
                receiver.save()

                # Save in Transfer Model
                Transfer.objects.create(
                    sender = sender,
                    receiver = receiver,
                    amount = amount,
                )

                # Msg if balance is valid
                messages.success(request, f'Successfully Sent {amount} to {receiver.name}.')
            else:
                # Msg if balance is invalid
                messages.error(request, "Insufficient Balance.")
                
            return redirect('profile', user_id=user_id)


# Convert CSV File
def convert_file(file):
    data = []

    if file.name.endswith('.xlsx'):
        # Read the CSV file into DataFrame
        df = pd.read_excel(file)
        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient='records')
    
    elif file.name.endswith('.csv'):
        # Read the XLSX file into DataFrame
        df = pd.read_csv(file)
        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient='records')
    
    else:
        data

    return data
