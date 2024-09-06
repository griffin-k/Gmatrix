from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
import requests
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages



import os
import sys
sys.path.append(os.getcwd())











@login_required
def dashboard_view(request):
    return render(request, 'Dashboard/admin_panal.html')
@login_required
def settings_view(request):
    return render(request, 'Dashboard/setting.html')








@login_required
def generate_Attendence(request):
    api_url = 'http://127.0.0.1:8000/members_api/'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        members = response.json()
    
        active_members = [
            member for member in members if member.get('status') == 'Active'
        ]

        if not active_members:
            return HttpResponse("No active members found.", status=404)

    except requests.RequestException as e:
        return HttpResponse(f"Error fetching data: {e}", status=500)
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,  # Set a base top margin
        bottomMargin=inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=14,
        alignment=1,  # Center alignment
        fontName="Helvetica-Bold"
    )
    date_style = ParagraphStyle(
        name="DateStyle",
        fontSize=11,
        alignment=2,  # Right alignment
        fontName="Helvetica"
    )
    normal_style = ParagraphStyle(
        name="NormalStyle",
        fontSize=11,
        alignment=0,  # Left alignment
        fontName="Helvetica"
    )
    elements.append(Spacer(1, 1.5 * inch))  # Add 1 inch padding at the top

    title = Paragraph("Attendance Sheet", title_style)
    current_date = datetime.now().strftime("%Y-%m-%d")
    date = Paragraph(f"Date: {current_date}", date_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(date)
    elements.append(Spacer(1, 0.2 * inch))
    data = [['Sr No', 'Name', 'Present', 'Absent']]
    for idx, member in enumerate(active_members, start=1):
        row = [str(idx), member.get('name', ''), '', '']
        data.append(row)
    table = Table(data, colWidths=[0.5 * inch, 3 * inch, 1.5 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    existing_pdf_path = 'Assets/pdf_temps/attendence.pdf'
    try:
        existing_pdf = PdfReader(existing_pdf_path)
        output_pdf = PdfWriter()
        header_pdf = PdfReader(buffer)
        header_page = header_pdf.pages[0]
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            page.merge_page(header_page)
            output_pdf.add_page(page)
        final_buffer = BytesIO()
        output_pdf.write(final_buffer)
        final_buffer.seek(0)
        response = HttpResponse(final_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="attendance_sheet.pdf"'
        return response

    except FileNotFoundError:
        return HttpResponse("Error: PDF template not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error processing PDF: {e}", status=500)


@login_required
def student_body(request):
    api_url = 'http://127.0.0.1:8000/members_api/'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        members = response.json()

        if not members:
            return HttpResponse("No data found.", status=404)

    except requests.RequestException as e:
        return HttpResponse(f"Error fetching data: {e}", status=500)

    # Filter members based on status and designation
    filtered_members = [
        {
            'name': member['name'],
            'designation': member['designation'],
            'phone_no': member.get('phone_no', 'N/A')  # Use 'phone_no' for contact
        }
        for member in members
        if member.get('status') == 'Active' and member.get('designation') != 'Member'
    ]

    if not filtered_members:
        return HttpResponse("No active members with the specified designation.", status=404)

    # Create a PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=1.5 * inch,  # Adjust top margin for padding
        bottomMargin=inch
    )

    # Define elements list to add content
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=14,
        alignment=1,  # Center alignment
        fontName="Helvetica-Bold"
    )
    date_style = ParagraphStyle(
        name="DateStyle",
        fontSize=11,
        alignment=2,  # Right alignment
        fontName="Helvetica"
    )

    # Add extra space at the top
    elements.append(Spacer(1, 1 * inch))

    # Title and Date
    title = Paragraph("Filtered Members List", title_style)
    current_date = datetime.now().strftime("%Y-%m-%d")
    date = Paragraph(f"Date: {current_date}", date_style)

    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(date)
    elements.append(Spacer(1, 0.2 * inch))

    # Table header and data
    data = [['Sr No', 'Name', 'Designation', 'Phone No']]
    for idx, member in enumerate(filtered_members, start=1):
        row = [str(idx), member['name'], member['designation'], member['phone_no']]
        data.append(row)

    # Create table with styles
    table = Table(data, colWidths=[0.5 * inch, 2.5 * inch, 2 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
    ]))

    # Add table to elements
    elements.append(table)

    # Build the PDF to buffer
    doc.build(elements)
    buffer.seek(0)

    # Load existing PDF template
    existing_pdf_path = 'Assets/pdf_temps/attendence.pdf'
    try:
        existing_pdf = PdfReader(existing_pdf_path)
        output_pdf = PdfWriter()
        header_pdf = PdfReader(buffer)
        header_page = header_pdf.pages[0]

        # Add the header PDF to each page of the existing PDF template
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            page.merge_page(header_page)
            output_pdf.add_page(page)

        # Save the output PDF to a BytesIO buffer
        final_buffer = BytesIO()
        output_pdf.write(final_buffer)
        final_buffer.seek(0)

        # Prepare HTTP response
        response = HttpResponse(final_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="filtered_members_list.pdf"'
        return response

    except FileNotFoundError:
        return HttpResponse("Error: PDF template not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error processing PDF: {e}", status=500)
    








#################################
# Support Center view
#################################
def support_center(request):
    if request.method == "POST":
        request_for = request.POST.get('request_for')
        description = request.POST.get('description')
        data = {
            'request_for': request_for,
            'description': description,
            'subject': 'New form submission',
        }
        try:
            response = requests.post(
                'https://formspree.io/f/xpwanjdq',  
                data=data,
            )
            if response.status_code == 200:
                messages.success(request, "Your request has been successfully submitted!")
            else:
                messages.error(request, "There was an error submitting your request. Please try again later.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect('support_center')
    return render(request, 'Dashboard/support_center.html')







###########################################
##     Function without custom temp      ##
###########################################


# def generate_pdf(request):
#     # Fetch data from the API
#     api_url = 'http://127.0.0.1:8000/members_api/'
#     response = requests.get(api_url)
#     members = response.json()

#     # Prepare the HTTP response
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="attendance_sheet.pdf"'

#     # Create the PDF object, set to A4 size
#     doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)

#     # Define elements list to add content
#     elements = []

#     # Define styles
#     styles = getSampleStyleSheet()
#     title_style = ParagraphStyle(
#         name="TitleStyle",
#         fontSize=14,
#         alignment=1,  # Center alignment
#         fontName="Helvetica-Bold"
#     )
#     date_style = ParagraphStyle(
#         name="DateStyle",
#         fontSize=11,
#         alignment=2,  # Right alignment
#         fontName="Helvetica"
#     )
#     normal_style = ParagraphStyle(
#         name="NormalStyle",
#         fontSize=11,
#         alignment=0,  # Left alignment
#         fontName="Helvetica"
#     )

#     # Title and Date
#     title = Paragraph("Attendance Sheet", title_style)
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     date = Paragraph(f"Date: {current_date}", date_style)

#     elements.append(title)
#     elements.append(Spacer(1, 0.2 * inch))
#     elements.append(date)
#     elements.append(Spacer(1, 0.2 * inch))

#     # Table header and data
#     data = [['Sr No', 'Name', 'Present', 'Absent']]

#     for idx, member in enumerate(members, start=1):
#         row = [str(idx), member['name'], '', '']
#         data.append(row)

#     # Create table with styles
#     table = Table(data, colWidths=[0.5 * inch, 3 * inch, 1.5 * inch, 1.5 * inch])
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.white),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 11),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#         ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 1), (-1, -1), 11),
#     ]))

#     # Add table to elements
#     elements.append(table)

#     # Build the PDF
#     doc.build(elements)

#     return response
