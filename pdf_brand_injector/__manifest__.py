{
    'name': 'PDF Brand Injector',
    'version': '1.1.0',
    'summary': 'Automatically inject your company logo into PDF files with smart positioning',
    'description': """
PDF Brand Injector

Automatically inject your company logo into uploaded PDF files in Odoo with flexible positioning options.

🚀 Features:
- Automatically adds logo to all uploaded PDF files
- Predefined positions (Top Left, Top Center, Top Right, Middle Center, Bottom Center, Bottom Right)
- Manual X/Y positioning override
- Adjustable logo size (width & height)
- Works seamlessly with all attachments
- Simple configuration via Settings

🎯 Use Cases:
- Invoice branding
- Document watermarking
- Report customization
- Company document standardization

⚙️ How it works:
1. Configure logo position in Settings
2. Upload a PDF file
3. Logo is automatically injected

No extra steps required!

✔ Compatible with standard Odoo modules  
✔ Lightweight and fast  
✔ Easy to use  

Support:
Contact us for customization or support.
""",
    'category': 'Tools',
    'author': 'Sanmark Solutions',
    'website': 'https://sanmarksolutions.com/',
    'license': 'LGPL-3',

    'depends': ['base', 'web'],

    'data': [
        'views/settings_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'price': 19.0,
    'currency': 'USD',

    'images': [
        'static/description/banner.png',
    ],
}