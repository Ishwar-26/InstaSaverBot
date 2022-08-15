import telebot
import instaloader

ig = instaloader.Instaloader()

bot = telebot.TeleBot('5512222550:AAGZ-r6ysZQMcHwG49AfdjuH1a9XRvZ2mow')

# username = "testinguser26"
# ig.load_session_from_file(username)
# profile = instaloader.Profile.from_username(ig.context,username)

# @bot.message_handler(commands=['Greet'])
# def greet(message):
#     bot.reply_to(message,"Hey ! how's it going?")

# @bot.message_handler(commands=['hello'])
# def hello(message):
#     bot.send_message(message.chat.id,"Hello !!")

@bot.message_handler(commands=['start'],content_types=['text'])
def start(message):
    user = bot.send_message(message.chat.id,"<strong>Hello User !! </strong>\n\nThis is bot is created for download all your saved posts from instagram !!\n\nIf you want to start using this bot you can use /welcome command.\n\nIf you need help you can use /help command.",parse_mode="HTML")
    if(user == '/welcome'):
        bot.register_next_step_handler(user, welcome)
    else:
        bot.send_message(message.chat.id,"Sorry, I don't understand !! please use /welcome command!!")

    

@bot.message_handler(commands=['welcome'],content_types=['text'])
def welcome(message):
    req_user = bot.send_message(message.chat.id, "Welcome to InstaSaver. what's your instagram username?")
    bot.register_next_step_handler(req_user, password_handler) #Next message will call the name_handler function

def password_handler(message):
    req_user = message.text
    req_password = bot.send_message(message.chat.id,"Enter your password")
    bot.register_next_step_handler(req_password, download_handler,req_user)


def download_handler(message,username):
    req_password = message.text
    try:
        ig.login(user=username,passwd=req_password)
    except instaloader.exceptions.BadCredentialsException:
        bot.send_message(message.chat.id,"I think your username or password is wrong!!")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        code = bot.send_message(message.chat.id,"Two factor authentication enabled please enter code !!")
        bot.register_next_step_handler(code, save_insta_collection,username)
    except instaloader.exceptions.InvalidArgumentException:
        bot.send_message(message.chat.id,"<strong>sorry</strong>, but I think this user is not exists or you type invalid username !!\n\nYou can start again by using /welcome command.",parse_mode="HTML")
    else:
        bot.send_message(message.chat.id,f"Hello {username} !! Your downloading will start soon !!")
        save_insta_collection(message,username)



def code_authenticate(message,username):
    if(message.text):
        try:
            ig.two_factor_login(message.text)
        except instaloader.exceptions.BadCredentialsException:
            bot.send_message(message.chat.id,"Invalid code !!")
        else:
            bot.send_message(message.chat.id,f"Hello {username} !! Your downloading will start soon !!")
            bot.register_next_step_handler(message, save_insta_collection,username)
            
        finally:
            bot.send_message(message.chat.id,"Thanks for using !!")

def save_insta_collection(message,username):

    profile = instaloader.Profile.from_username(ig.context,username)
    post_list = []
    for post in profile.get_saved_posts():
        post_list.append(post)
        # print(dir(post))
        if(post.is_video):
            bot.send_video(message.chat.id,post.video_url)
        else:
            bot.send_photo(message.chat.id,post.url)
        # ig.download_post(post,'mysavedcollection')
    bot.send_message(message.chat.id,"Thanks for using InstaSaver!!")
    

bot.polling()