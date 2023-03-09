def user_authentication(func):
    def wrapper(*args, **kwargs):
        user = "Eddy"
        return func(user, *args, **kwargs)
    return wrapper

@user_authentication
def book_treatment(user, id):
    if user == "Eddy" and id == 3:
        return "correct"
    else:
        return "incorrect"

print(book_treatment(4))
