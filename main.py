from db import DataBase
from utils import clear
import os

from Crypto.Cipher import AES

key = b'<Z\xe4v\xb5\x80\x04\x16\x00\xe3X\x9b\x1ap2\xe20\xadr\x7f\x156\x90\xa1\x80D\x0e\xbd\x80\xc1\xf8\x9f'
nounce = b'\x97\x07\xc5\xb9I1\x02\xf9\xcbL"\xc6\x10\xbeq\xe0V\x93\rU\xd3_\x02\x90\x93VF\xaa&\xc6\xa3S\xd8 x6\x9a\xd7\xb6\xc5\xff\x9dX\'\x86X\xacY\xd6%\xd0\x08\xad\x0c\xb2q\xeaI8\xceV\xd2\xab\xc4H\xc1\xb6\xae}!\xf7\xf6s\xaa\xb6\xe9{\x03\xb0\x1dp\xea2&|\xb8\x9e\x8d\xadV\x9d\x81\xbb\x1a\xe3~Qp\x95\x11p\x13\xbes\x05\xf6d&*\xce\xb5\x07jS9\x1c\x18#\xbd/\x7fY\xa36\x03\x96X\x1a'

cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=nounce)

try:
  db = DataBase(r"C:\Users\myhou\AppData\Local\Programs\AssetFlow\data.json")
  db.load_database()
  if db.database["password"]["data"] == []:
    is_users = False
  else:
    is_users = True
except:
  is_users = False
  try:
    os.mkdir(r"C:\Users\myhou\AppData\Local\Programs\AssetFlow")
  except:
    pass
  db = DataBase(r"C:\Users\myhou\AppData\Local\Programs\AssetFlow\data.json")
  db.create_table("password", ["password"])
  db.create_table("inventory", ["ID", "name", "price", "quantity"])


def main():
  clear()
  while True:
    print("|>====================================================>")
    print("|    INVENTORY :: INVENTORY   ")
    print("|>====================================================>")
    print("|  Welcome to AssetFlow!")
    print("|")
    print("|  1) Create a new item")
    print("|  2) Update an item")
    print("|  3) Delete an item")
    print("|  4) x - y")
    print("|  5) Logout")
    print("|")

    user = input("|  Choice :: ")

    if user == "1":
      print("|>====================================================>")
      print("|         NEW :: NEW          ")
      print("|>====================================================>")
      i = 0
      for item in db.database["inventory"]["data"]:
        i += 1
      db.insert_row(table_name="inventory", row=[i, input("|  name: "), input("|  price: "), int(input("|  quantity: "))])
      db.save_database()
    elif user == "2":
      print("|>====================================================>")
      print("|       UPDATE :: UPDATE      ")
      print("|>====================================================>")
      ID = int(input("|  ID: "))
      db.update_row(table_name="inventory", index=ID, row=[ID, input("|  name: "), int(input("|  price: ")), int(input("|  quantity: "))])
      db.save_database()
    elif user == "3":
      print("|>====================================================>")
      print("|      DELETE :: DELETE       ")
      print("|>====================================================>")
      db.delete_row(table_name="inventory", index=int(input("|  ID: ")))
      db.save_database()
    elif user == "4":
      print("|>====================================================>")
      print("|       X - Y :: X - Y        ")
      print("|>====================================================>")
      ID1 = int(input("|  ID High: "))
      ID2 = int(input("|  ID Low: "))
      for index, item in enumerate(db.database["inventory"]["data"]):
        if index >= ID1 and index <= ID2:
          print(f"|  {item[0]:^10} | {item[1]:^10} | {item[2]:^10} | {item[3]:^10} |")

    elif user == "5":
      print("|>====================================================>")
      print("|          BYE :: BYE         ")
      print("|>====================================================>")
      db.save_database()
      quit()
    else:
      print("|  Invalid choice!")


def signup_user():
  print("|>====================================================>")
  print("|       SIGNUP :: SIGNUP      ")
  print("|>====================================================>")
  password = input("|  password: ").encode("utf-8")
  try:
    db.database["password"]["data"].append(cipher.encrypt(password).decode())
  except:
    print("|  There was an error!")
  db.save_database()
  return 5


def login():
  cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=nounce)
  try:
    decode_pass = cipher.decrypt(db.database["password"]["data"][0].encode("utf-8")).decode()
  except:
    print("|  There was an error!")
    print("|>====================================================>")
    print("|          BYE :: BYE         ")
    print("|>====================================================>")
    quit()
  print("|>====================================================>")
  print("|        LOGIN :: LOGIN       ")
  print("|>====================================================>")
  password = input("|  password: ")
  if password == decode_pass:
    main()
  else:
    login()


def menu():
  clear()
  print("|>====================================================>")
  print("|         MENU :: MENU        ")
  print("|>====================================================>")
  print("|")
  print("|  Welcome to AssetFlow!")
  print("|  When You Create A Password\n"
        "|  Create A 4 Digit Password")
  print("|")
  if not is_users:
    code = signup_user()
    if code == 5:
      login()
  else:
    code = login()
    if code == 5:
      signup_user()


if __name__ == "__main__":
  menu()