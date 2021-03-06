from django.db import models
from django.utils.timezone import now
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):

    # ------- login - password- register ----------------------------------

    def v_login(self, form):
        errors = []
        try:
            user = User.objects.get(email=form['email'])
            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                errors.append('Username or password is incorrect.')
                return errors
        except:
            errors.append('Username or password is incorrect.')
        return errors

    def login(self):
        pass

    def v_password_change(self, form, user_id):
        print('8'*80)
        print('hi')
        errors = []
        if len(form['password']) < 2:
            errors.append('Password is to short.')
        if form['password'] != form['confirm_password']:
            errors.append('Password must match the Confirm password')
        if not errors:
            pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
            user = User.objects.get(id=user_id)
            user.password = pw_hash
            user.save()
        else:
            return errors

    def v_register(self, form):
        errors = []
        if len(form['f_name'])<1:
            errors.append('First name must be filled out.')
        if len(form['l_name'])<1:
            errors.append('Last name must be filled out.')
        if len(form['email'])<1:
            errors.append('Email name must be filled out.')
        try:
            user = User.objects.get(email=form['email'])
            errors.append('Email aready in use, Please use another.')
        except:
            pass
        if len(form['email'])>1 and not EMAIL_REGEX.match(form['email']):
            errors.append('Not a valid email address.')
        if len(form['password']) < 2:
            errors.append('Password is to short.')
        if form['password'] != form['confirm_password']:
            errors.append('Password must match the Confirm password')
        return errors

    def register(self, form):
        pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        num_users = User.objects.all()
        x=0
        for user in num_users:
            x+=1

        if x==0:
            admin = True
        else:
            admin = False


        userinfo = self.create(
            f_name=form['f_name'],
            l_name=form['l_name'],
            email=form['email'],
            password=pw_hash,
            admin=admin
        )
        print('8'*80)
        print(userinfo)
        return userinfo

#------- user change profile - discription ----------------------------

    def v_profile_change(self, form, user_id):
        user = User.objects.get(id=user_id)
        # print(form['email'])
        # print(user.email)
        # print('email length = ', len(form['email']))
        errors = []
        if len(form['f_name'])<1:
            errors.append('First name must be filled out.')
        if len(form['l_name'])<1:
            errors.append('Last name must be filled out.')
        if form['email'] == user.email:
            print('Email is equal')
        elif len(form['email'])<1:
            errors.append('Email must be filled out.')
        elif len(form['email']) > 1 and not EMAIL_REGEX.match(form['email']):
            errors.append('Not a valid email address.')
            # print('not valid')
        else:
            try:
                user = User.objects.get(email=form['email'])
                errors.append('Email aready in use, Please use another.')
            except:
                pass
        if not errors:
            user.f_name=form['f_name']
            user.l_name=form['l_name']
            user.email=form['email']

            user.save()
        return (errors, user)

    def v_description_change(self, form, user_id):
        errors= []
        if len(form['personal_description'])<1:
            errors.append('Must enter something in Description to update.')
        else:
            user = User.objects.get(id=user_id)
            user.description = form['personal_description']
            user.save()
        return errors

# ---------Admin rights ------------------------------------------------
    def admin_edit_profile(self, form, user_id):
        errors = []
        user = User.objects.get(id=user_id)
        errors = []
        if len(form['f_name']) < 1:
            errors.append('First name must be filled out.')
        if len(form['l_name']) < 1:
            errors.append('Last name must be filled out.')
        if form['email'] == user.email:
            print('Email is equal')
        elif len(form['email']) < 1:
            errors.append('Email must be filled out.')
        elif len(form['email']) > 1 and not EMAIL_REGEX.match(form['email']):
            errors.append('Not a valid email address.')
        else:
            try:
                user = User.objects.get(email=form['email'])
                errors.append('Email aready in use, Please use another.')
            except:
                pass
        if form['admin'] == 'True':
            print('Admin is True')
            admin = True
        else:
            admin = False
        if not errors:
            user.f_name = form['f_name']
            user.l_name = form['l_name']
            user.email = form['email']
            user.admin = admin
            user.save()
        return errors

    def admin_register(self, form):
        pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        if form['admin'] == 'True':
            admin=True
        else:
            admin=False

        userinfo = self.create(
            f_name=form['f_name'],
            l_name=form['l_name'],
            email=form['email'],
            password=pw_hash,
            admin=admin
        )
        return userinfo


class User(models.Model):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    admin = models.BooleanField(default=False)
    description = models.CharField(default='None', max_length=600)
    image = models.ImageField(upload_to='profile_image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.f_name


class MessageManager(models.Manager):
    def v_message(self, form):
        if len(form['message'])<1:
            return False
        else:
            return True

    def create_message(self, form, to_user_id, user):
        to_user = User.objects.get(id=to_user_id)
        m = Message.objects.create(
            writee=to_user,
            writer=user,
            note=form['message']
        )
        return m


class Message(models.Model):
    writee = models.ForeignKey(User, related_name='writee')
    writer = models.ForeignKey(User, related_name='writer')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()


class CommentManager(models.Manager):
    def v_comment(self, form):
        if len(form['comment'])<1:
            return False
        else:
            return True

    def create_comment(self, form, user):
        to_message_id = Message.objects.get(id=form['id'])
        c = Comment.objects.create(
            writee=to_message_id,
            writer=user,
            note=form['comment']
        )
        return c


class Comment(models.Model):
    writee = models.ForeignKey(Message, related_name='comment')
    writer = models.ForeignKey(User, related_name='comment')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
