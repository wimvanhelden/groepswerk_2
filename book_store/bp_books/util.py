import secrets
import os
from PIL import Image #PIL is pillow, used for resizing profile pictures 
from flask import current_app


#handles the logic of saving a picture
def save_picture(form_picture):  #needs more try/except... 
    #first generate a random name, using secrets module
    random_hex = secrets.token_hex(8)
    #make sure we save the file with the same extension as it is uploaded
    #so check which extension it is... 
    _f_name, f_ext = os.path.splitext(form_picture.filename)  #path.splitext return two things, we only use f_ext
    #concat random hex and file extension for new filename
    picture_fn = random_hex + f_ext
    #form path where picture file will be saved
    picture_path = os.path.join(current_app.root_path, 'static/pictures', picture_fn)
    #resize the image using PIP (Pillows)
    output_size = (125,125)  #nice thing to put in a config file
    i = Image.open(form_picture)
    i.thumbnail(output_size)  
    #save image: 
    i.save(picture_path)
    #nice possible addition: delete the previous image
    return picture_fn  #return filename to store in db