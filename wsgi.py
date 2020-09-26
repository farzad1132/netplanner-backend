from app import connex_app

# Running app with gunicorn:
# in Terminal:
#   gunicorn -c gunicorn.conf.py wsgi:connex_app
#   watch access and error logs for more information

if __name__ == "__main__":
    connex_app.run()