# blog_shop_chat


=======================
You can watch the [DEMO](https://bchavcut-bchavcut.fandogh.cloud/) and use this app

tutorial:

This app is a sipmle cms, blog, store builder, chat application that create by django and use postgres database,
for cms use grappelli package and for otp use Kavenegar

To run this app on your system. Do the following:

### How to Run the app

```git clone https://github.com/sina-mobarez/blog_shop_chat.git```

Change directory into the app:

```cd blog_shop_chat```

Create a new virtual environment

```python -m venv env```

Activate the environment

```source env/bin/activate``` On windows: ```source env\Scripts\activate```

Now install the necessary dependencies:

```pip install -r requirements.txt```

Go to root directory of project:

```cd BlogShopChat```

after installation,

now migrate:

```python manage.py makemigrations```
```python manage.py migrate```

Create super user:

```python manage.py createsuperuser```

Run the App:
```python manage.py runserver```

### Features:

CMS

Panel store for sell

Api for customers

Blog

Chat application (for every store created and confirmed by admin set a chatroom for comunicate between store keeper and it's customers)

2fa for user, send a verification code and verify phone number


