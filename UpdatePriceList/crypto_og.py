def encrypt(message, shift, alphabet):
  enc = ""
  if len(message) > 0:
    for i in message:
      x=0
      while (i != alphabet[x]):
        x+=1
      if (x + shift) >= len(alphabet):
        enc += alphabet[shift - (len(alphabet) - x)]
      else: 
        enc += alphabet[x + shift]
  return enc

def passwordIsValid(password):
  if len(password) < 5:
    valid = False
  elif not password[0] == '_' and not password[0].isalpha():
    valid = False
  else:
    spec_char = "!@#$%^_."
    nums = 0
    spec = False
    up = False
    low = False
    valid = True
    i = 0
    while ((not spec or not up or not low or (nums < 2)) and i < len(password)):
      ch = password[i]
      if ch.isalpha():
        if ch.isupper():
          up = True
        else:
          low = True
      elif ch in spec_char:
          spec = True
      elif ch.isdigit():
        nums+=1
      i+=1
  if not spec or not up or not low or nums<2:
    valid = False
  return valid


message = "abcxyz"
shift = 2
alphabet = "abcdefghijklmnopqestuvwxyz"
print(encrypt(message,shift,alphabet))

password = "BU n # YY113"
print(passwordIsValid(password))
