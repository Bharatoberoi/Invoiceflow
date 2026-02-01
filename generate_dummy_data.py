"""Generate realistic dummy PDF files for orders and invoices"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime, timedelta
import os

# Create orders folder if it doesn't exist
os.makedirs('orders', exist_ok=True)
os.makedirs('invoices', exist_ok=True)

def create_order_pdf(filename, order_data):
    """Create an order PDF with realistic data"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>ORDER #{order_data['id']}</b>", styles['Heading1'])
    elements.append(title)
    elements.append(Spacer(1, 0.2))
    
    # Order details
    details_text = f"""
    <b>Order Date:</b> {order_data['date']}<br/>
    <b>Customer:</b> {order_data['customer']}<br/>
    <b>Status:</b> {order_data['status']}<br/>
    <b>Total Amount:</b> ${order_data['total']}<br/>
    """
    elements.append(Paragraph(details_text, styles['Normal']))
    elements.append(Spacer(1, 0.3))
    
    # Items table
    elements.append(Paragraph("<b>Order Items:</b>", styles['Heading3']))
    items_data = [['Product', 'Quantity', 'Price', 'Total']]
    for item in order_data['items']:
        items_data.append([item['name'], str(item['qty']), f"${item['price']}", f"${item['total']}"])
    
    items_table = Table(items_data, colWidths=[250, 80, 80, 80])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(items_table)
    
    # Shipping info
    elements.append(Spacer(1, 0.3))
    shipping_text = f"""
    <b>Shipping Address:</b><br/>
    {order_data['shipping_address']}<br/><br/>
    <b>Shipping Method:</b> {order_data['shipping_method']}<br/>
    <b>Expected Delivery:</b> {order_data['delivery_date']}<br/>
    """
    elements.append(Paragraph(shipping_text, styles['Normal']))
    
    doc.build(elements)

def create_invoice_pdf(filename, invoice_data):
    """Create an invoice PDF with realistic data"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>INVOICE #{invoice_data['id']}</b>", styles['Heading1'])
    elements.append(title)
    elements.append(Spacer(1, 0.2))
    
    # Invoice details
    details_text = f"""
    <b>Invoice Date:</b> {invoice_data['date']}<br/>
    <b>Due Date:</b> {invoice_data['due_date']}<br/>
    <b>Customer:</b> {invoice_data['customer']}<br/>
    <b>Status:</b> {invoice_data['status']}<br/>
    <b>Invoice Amount:</b> ${invoice_data['total']}<br/>
    """
    elements.append(Paragraph(details_text, styles['Normal']))
    elements.append(Spacer(1, 0.3))
    
    # Services/Items table
    elements.append(Paragraph("<b>Invoice Details:</b>", styles['Heading3']))
    items_data = [['Description', 'Quantity', 'Rate', 'Amount']]
    for item in invoice_data['items']:
        items_data.append([item['description'], str(item['qty']), f"${item['rate']}", f"${item['amount']}"])
    
    items_table = Table(items_data, colWidths=[200, 80, 80, 80])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(items_table)
    
    # Summary
    elements.append(Spacer(1, 0.3))
    summary_text = f"""
    <b>Subtotal:</b> ${invoice_data['subtotal']}<br/>
    <b>Tax (10%):</b> ${invoice_data['tax']}<br/>
    <b>Total:</b> ${invoice_data['total']}<br/>
    <br/>
    <b>Payment Terms:</b> {invoice_data['payment_terms']}<br/>
    <b>Notes:</b> {invoice_data['notes']}<br/>
    """
    elements.append(Paragraph(summary_text, styles['Normal']))
    
    doc.build(elements)

# Generate Orders
orders = [
    {
        'id': 'ORD-2024-001',
        'date': '2024-12-15',
        'customer': 'Acme Corporation',
        'status': 'SHIPPED',
        'total': '4500',
        'items': [
            {'name': 'Premium Software License (1 Year)', 'qty': 5, 'price': '500', 'total': '2500'},
            {'name': 'Enterprise Support Package', 'qty': 1, 'price': '1500', 'total': '1500'},
            {'name': 'Implementation Training', 'qty': 1, 'price': '500', 'total': '500'},
        ],
        'shipping_address': '123 Business Ave, New York, NY 10001',
        'shipping_method': 'Standard Shipping',
        'delivery_date': '2024-12-20',
    },
    {
        'id': 'ORD-2024-002',
        'date': '2024-12-18',
        'customer': 'TechStart Inc',
        'status': 'PROCESSING',
        'total': '2800',
        'items': [
            {'name': 'Cloud Storage (100GB/Month)', 'qty': 12, 'price': '150', 'total': '1800'},
            {'name': 'API Access License', 'qty': 1, 'price': '800', 'total': '800'},
            {'name': 'Priority Support', 'qty': 1, 'price': '200', 'total': '200'},
        ],
        'shipping_address': '456 Innovation Blvd, San Francisco, CA 94105',
        'shipping_method': 'Express Shipping',
        'delivery_date': '2024-12-21',
    },
    {
        'id': 'ORD-2024-003',
        'date': '2024-12-20',
        'customer': 'Global Enterprises Ltd',
        'status': 'PENDING',
        'total': '7200',
        'items': [
            {'name': 'Enterprise Database License', 'qty': 3, 'price': '1500', 'total': '4500'},
            {'name': 'Backup & Disaster Recovery', 'qty': 1, 'price': '1200', 'total': '1200'},
            {'name': 'Managed Services (3 months)', 'qty': 1, 'price': '1500', 'total': '1500'},
        ],
        'shipping_address': '789 Corporate Drive, Chicago, IL 60601',
        'shipping_method': 'Standard Shipping',
        'delivery_date': '2024-12-28',
    },
]

# Generate Invoices
invoices = [
    {
        'id': 'INV-2024-001',
        'date': '2024-12-01',
        'due_date': '2024-12-31',
        'customer': 'CloudSoft Solutions',
        'status': 'PAID',
        'subtotal': '5000',
        'tax': '500',
        'total': '5500',
        'items': [
            {'description': 'Software Development Services (40 hours)', 'qty': 1, 'rate': '2000', 'amount': '2000'},
            {'description': 'Cloud Infrastructure Setup', 'qty': 1, 'rate': '1500', 'amount': '1500'},
            {'description': 'Security Audit & Compliance Review', 'qty': 1, 'rate': '1500', 'amount': '1500'},
        ],
        'payment_terms': 'Net 30',
        'notes': 'Payment received on 2024-12-15. Thank you for your business.',
    },
    {
        'id': 'INV-2024-002',
        'date': '2024-12-05',
        'due_date': '2024-12-20',
        'customer': 'Digital Innovations Corp',
        'status': 'PENDING',
        'subtotal': '3200',
        'tax': '320',
        'total': '3520',
        'items': [
            {'description': 'UI/UX Design Services (32 hours)', 'qty': 1, 'rate': '1600', 'amount': '1600'},
            {'description': 'Mobile App Development (16 hours)', 'qty': 1, 'rate': '1600', 'amount': '1600'},
        ],
        'payment_terms': 'Net 15',
        'notes': 'Invoice awaiting payment. Please remit funds to the specified account.',
    },
    {
        'id': 'INV-2024-003',
        'date': '2024-12-10',
        'due_date': '2024-01-10',
        'customer': 'NextGen Systems',
        'status': 'OVERDUE',
        'subtotal': '4800',
        'tax': '480',
        'total': '5280',
        'items': [
            {'description': 'Annual Maintenance Contract', 'qty': 1, 'rate': '2400', 'amount': '2400'},
            {'description': 'Technical Support Services', 'qty': 1, 'rate': '1200', 'amount': '1200'},
            {'description': 'Software License Renewal', 'qty': 1, 'rate': '1200', 'amount': '1200'},
        ],
        'payment_terms': 'Net 30',
        'notes': 'This invoice is overdue. Please prioritize payment to avoid service interruption.',
    },
]

# Create PDF files
print("Generating order PDFs...")
for order in orders:
    create_order_pdf(f"orders/{order['id']}.pdf", order)
    print(f"  Created: orders/{order['id']}.pdf")

print("\nGenerating invoice PDFs...")
for invoice in invoices:
    create_invoice_pdf(f"invoices/{invoice['id']}.pdf", invoice)
    print(f"  Created: invoices/{invoice['id']}.pdf")

print("\n✓ All dummy data PDFs generated successfully!")
