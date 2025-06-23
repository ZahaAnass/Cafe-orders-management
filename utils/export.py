import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def export_to_pdf(data, filename):
    pdf = canvas.Canvas(filename, pagesize=A4)
    pdf.setFont('Helvetica', 12)
    pdf.drawString(100, 750, 'Sales Report')
    pdf.drawString(100, 725, 'Period: ' + data['period'])
    pdf.drawString(100, 700, 'Total: ' + str(data['total']))
    x = 100
    y = 675
    for row in data['rows']:
        pdf.drawString(x, y, row['date'])
        pdf.drawString(x + 100, y, str(row['total']))
        y -= 25
    pdf.save()
