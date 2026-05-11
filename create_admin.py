# Script to create/reset admin user
# Run: python manage.py shell < create_admin.py

from django.contrib.auth.models import User

username = 'admin'
email = 'admin@example.com'
password = 'YourStrongAdminPass123!'

if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'Password updated for existing user: {username}')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Created new superuser: {username}')