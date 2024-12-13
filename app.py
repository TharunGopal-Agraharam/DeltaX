from flask import Flask, render_template, request, redirect, url_for
from models import db, Lead
import matplotlib.pyplot as plt
import os

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Screen 1: Lead Listing
@app.route('/')
def lead_listing():
    leads = Lead.query.all()
    return render_template('lead_listing.html', leads=leads)

# Screen 2: Lead Details
@app.route('/lead/<int:lead_id>')
def lead_details(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    return render_template('lead_details.html', lead=lead)

# Screen 3: Lead Management
@app.route('/manage_lead', methods=['GET', 'POST'])
def manage_lead():
    if request.method == 'POST':
        lead_id = request.form.get('id')
        name = request.form['name']
        contact = request.form['contact']
        source = request.form['source']
        status = request.form.get('status', 'New')
        salesperson = request.form['salesperson']

        if lead_id:  # Update existing lead
            lead = Lead.query.get(lead_id)
            lead.name = name
            lead.contact = contact
            lead.source = source
            lead.status = status
            lead.salesperson = salesperson
        else:  # Add new lead
            new_lead = Lead(name=name, contact=contact, source=source, status=status, salesperson=salesperson)
            db.session.add(new_lead)

        db.session.commit()
        return redirect(url_for('lead_listing'))

    lead_id = request.args.get('id')
    lead = Lead.query.get(lead_id) if lead_id else None
    return render_template('manage_lead.html', lead=lead)

# Screen 4: Dashboard
@app.route('/dashboard')
def dashboard():
    leads = Lead.query.all()

    # Generate charts
    sources = [lead.source for lead in leads]
    statuses = [lead.status for lead in leads]

    if not os.path.exists('static'):
        os.makedirs('static')

    plt.figure(figsize=(10, 5))
    # Pie chart for lead sources
    plt.subplot(1, 2, 1)
    plt.pie([sources.count(src) for src in set(sources)], labels=set(sources), autopct='%1.1f%%')
    plt.title("Leads by Source")

    # Bar chart for lead statuses
    plt.subplot(1, 2, 2)
    plt.bar(set(statuses), [statuses.count(status) for status in set(statuses)])
    plt.title("Leads by Status")
    plt.savefig('static/dashboard.png')
    plt.close()

    return render_template('dashboard.html', chart_url='/static/dashboard.png')

if _name_ == '_main_':
    app.run(debug=True)
