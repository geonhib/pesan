# PESAN SACCO SYSTEM

### Instructions 
- clone site
- Set up a python virtual enviroment according to your OS eg python -m venv venv for unix
- pip freeze -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
-  Create an admin user with your email and password following the command below:
- python manage.py createsuperuser
- python manage.py runserver
- Copy the socket generated by the development server in the terminal to a browser


### Workflow
Admin
- Admin logins 
- Add packages [default active], CRUD sacco packages
- De/activate packages
- Filter active packages to directors
- Adds sacco [default deactivated], CRUD Sacco
- De/activates sacco
- Creates license key
- License  De/activates sacco status
- Multitenant sacco
- trails
- Set default settings
- Dashboard-> package statuses & total,sacco statuses & total,  licenses statuses & next expiry, audits 

Director
- Recieves auth credentials
- Login
- Changes password
- check users sacco if exist
- Check if sacco is active/suspended 
- List active pages in dropdown
- Select package if none/expired
- View Sacco details, licence, expiry
- View dashboard
- View settings
- List filtered users
- Choose director
- CRUD users
- Mgt cmd for creating sacco members
- Limit sacco members for package
- dDashboard-> member gender & total, member statuses & total,  license next expiry, audits 

Member
- Login
- Change password
- Check if account is active/suspended
- View dasboard/tranaction details
- dDashboard-> last login, my audits 




