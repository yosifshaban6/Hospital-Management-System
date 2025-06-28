{
    'name':'lab4',
    'suammary':'ITI Hospital system',
    'author':'Youssef-Shaaban',
    'category':'Accounting',
    'version':'0.1',
    'depends':['crm','account','base'],
    'data':[
            'security/ir.model.access.csv',
            'security/security.xml',
            'security/rules.xml',
            'views/menus.xml',
            'views/departments_view.xml',
            'views/doctors_view.xml',
            'views/res_partner_view.xml',
            'reports/patient_template.xml',
            'reports/patient_report.xml',
            'views/patient_view.xml',
    ],
    'installable': True,
    'application': True
}