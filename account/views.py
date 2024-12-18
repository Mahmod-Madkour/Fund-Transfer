### account/views.py

from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from .models import Profile, Transfer
from decimal import Decimal
import pandas as pd

# Home Page
def home(request):
    if request.method == "GET":
        # Check if search
        search_query = request.GET.get('name')
        if search_query:
            accounts = Profile.objects.filter(name__icontains=search_query)
        else:
            accounts = Profile.objects.all()

        context = {'accounts': accounts}
        return render(request, "home/index.html", context)

    if request.method == "POST":
        accounts = Profile.objects.all()
        file = request.FILES.get('csv_file')

        # Not have a file
        if not file:
            error_msg = "Please select a file."
            context = {
                'accounts': accounts,
                'error_msg': error_msg,
            }
            return render(request, "home/index.html", context)
        
        # Check file format
        if not (file.name.endswith('.csv') or file.name.endswith('.xlsx')):
            error_msg = "Please upload a valid CSV or XLSX file."
            context = {
                'accounts': accounts,
                'error_msg': error_msg,
            }
            return render(request, "home/index.html", context)
        
        # Convert data to list
        data = convert_file(file)
        if not data:
            error_msg = "The file is empty or contains invalid data."
            context = {
                'accounts': accounts,
                'error_msg': error_msg,
            }
            return render(request, "home/index.html", context)
        
        # Process valid data
        new_records = 0
        for acc in data:
            if not Profile.objects.filter(id=acc['ID']).exists():
                Profile.objects.create(
                    id=acc['ID'],
                    name=acc['Name'],
                    balance=acc['Balance']
                )
                new_records += 1


        msg = f"Data added successfully. {new_records} new records were added."
        context = {
            'accounts': accounts,
            'msg': msg,
        }
        return render(request, "home/index.html", context)

# Profile Page
def profile(request, user_id):
    if request.method == "GET":
        accounts = Profile.objects.all()
        user_profile = Profile.objects.get(id=user_id)
        context = {
            'accounts': accounts,
            'user_profile': user_profile,
        }
        return render(request, "profile/profile.html", context)

    if request.method == "POST":
        receiver_id = request.POST.get('receiver')
        amount = Decimal(request.POST.get('amount'))

        # Get Sender and Receiver Profile
        sender = Profile.objects.get(id=user_id)
        receiver = Profile.objects.get(id=receiver_id)

        # Check amount number > 1
        if amount and amount < 1:
            messages.error(request, "Invalid amount. Please enter a positive number >= 1")
            return redirect('profile', user_id=user_id)

        # Check choose right account
        if sender.id == receiver.id:
            messages.error(request, "Can't Send Money to yourself!")
            return redirect('profile', user_id=user_id)

        # Check balance is valid
        if sender.balance < amount:
            messages.error(request, "Insufficient Balance.")
            return redirect('profile', user_id=user_id)

        # Handle the transfer process
        try:
            with transaction.atomic():
                # Update Balances
                sender.balance -= amount
                sender.save()

                receiver.balance += amount
                receiver.save()

                # Save the transfer record
                Transfer.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount
                )

            messages.success(request, f'Successfully Sent {amount} to {receiver.name}.')
            return redirect('profile', user_id=user_id)

        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
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
        pass
    return data
