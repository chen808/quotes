from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)
        self.load_model('WelcomeModel')



    def index(self):
        return self.load_view('index.html')




    def register(self):
        user_info = {
        'name' : request.form['name'],
        'alias' : request.form['alias'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password']
        }

        create_status = self.models['WelcomeModel'].register_user(user_info)

        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            return redirect('/success')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')




    def login(self):
        user_info = {
        'email' : request.form['email'],
        'password' : request.form['password']
        }

        status = self.models['WelcomeModel'].login_user(user_info)

        if status['status'] == False:
            for message in status['errors']:
                flash(message, 'Login_errors')
            return redirect('/')
        else:
            session['name'] = status['user']['name']
            return redirect('/success')





    def success(self):
        return self.load_view('success.html')


    def logout(self):
        session.clear()
        return redirect('/')

