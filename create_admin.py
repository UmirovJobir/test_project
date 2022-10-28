import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "strategy_agency.settings")
django.setup()
from django.contrib.auth.models import User
from django.conf import settings

def handle(*args, **options):
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = '123'
                print('Creating account for %s (%s)' % (username, email))
                admin = User.objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')

if __name__=='__main__':
    handle()