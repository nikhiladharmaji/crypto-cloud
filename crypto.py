import flask
from flask import request, jsonify, render_template
from Crypto.Cipher import AES
from Crypto import Random
from flask import send_file

key = Random.new().read(AES.block_size)
iv = Random.new().read(AES.block_size)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.


# @app.route('/', methods=['GET'])
# def home():
#   return render_template("index.html")


@app.route('/api/v1/encrypt', methods=['POST'])
def encrypt():
  print(request.get_data())
  if 'file' in request.files:
    orig_file = request.files['file']
  else:
    print("params missing")
    return "params missing"
  # key = Random.new().read(AES.block_size)
  # iv = Random.new().read(AES.block_size)
  ogf = orig_file.read()
  input_data = ogf

  cfb_cipher = AES.new(key, AES.MODE_CFB, iv) #find a way to incorp password with key
  enc_data = cfb_cipher.encrypt(input_data)

  enc_file = open("encrypted_local.png", "wb")
  enc_file.write(enc_data)
  enc_file.close()
  return send_file(enc_file, attachment_filename='enc_file.png')

@app.route('/api/v1/decrypt', methods=['POST'])
def decrypt():
  cfile= request.args['cfile']
  with open(cfile, 'rb') as f:
    enc_data2 = f.read()

  cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
  plain_data = cfb_decipher.decrypt(enc_data2)

  output_file = open("decrypted.png", "wb")
  output_file.write(plain_data)
  output_file.close()


app.run()
