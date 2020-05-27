import web
import os
from Models import AccountsModel, Posts

web.config.debug = False

urls = (
    '/', 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/post-registration', 'PostRegistration',
    '/check-login', 'CheckLogin',
    '/post-activity', 'PostActivity',
    '/profile/(.*)/info', 'UserInfo',
    '/settings', 'UserSettings',
    '/update-settings', 'UpdateSettings',
    '/profile/(.*)', 'UserProfile',
    '/submit-comment', 'SubmitComment',
    '/upload-image/(.*)', 'UploadImage'
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout",
                             globals={'session': session_data, 'current_user': session_data["user"]})


# Classes/Routes


class Home:
    def GET(self):

        post_model = Posts.Posts()
        posts = post_model.get_all_posts()

        print(posts)
        return render.Home(posts)


class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        return render.Login()


class PostRegistration:
    def POST(self):
        data = web.input()

        reg_model = AccountsModel.RegisterModel()
        reg_model.insert_user(data)

        return data.username


class CheckLogin:
    def POST(self):
        data = web.input()

        login = AccountsModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect

        return "error"


class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()

        return post_model.insert_post(data)


class UserProfile:
    def GET(self, user):
        login = AccountsModel.LoginModel()
        user_info = login.get_profile(user)

        post_model = Posts.Posts()
        posts = post_model.get_user_posts(user)

        return render.Profile(posts, user_info)


class UserInfo:
    def GET(self, user):
        login = AccountsModel.LoginModel()
        user_info = login.get_profile(user)

        return render.Info(user_info)


class UserSettings:
    def GET(self):
        return render.Settings()


class UpdateSettings:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        settings_model = AccountsModel.LoginModel()
        if settings_model.update_info(data):
            return "success"
        else:
            return "A fatal error has occurred"


class SubmitComment:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        added_comment = post_model.add_comment(data)

        if added_comment:
            return added_comment
        else:
            return {"error": "403"}


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None

        session.kill()
        return "success"


class UploadImage:
    def POST(self, type):
        file = web.input(avatar={}, background={})
        file_dir = os.getcwd() + "/static/uploads/" + session_data["user"]["username"]

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        if "avator" or "background" in file:
            filepath = file[type].filename.replace('\\', '/')
            filename = filepath.split("/")[-1]
            f = open(file_dir + "/" + filename, 'wb')
            f.write(file[type].file.read())
            f.close()

            update = {}
            update["type"] = type
            update["img"] = "/static/uploads/" + session_data["user"]["username"] + filename
            update["username"] = session_data["user"]["username"]

            image_model = AccountsModel.LoginModel()
            update_avatar = image_model.update_image(update)

        raise web.seeother("/settings")

if __name__ == "__main__":
    app.run()
