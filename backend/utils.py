import subprocess
import os
import platform
import urllib.request

def open_dir(folder_path):
    system = platform.system()
    if system == 'Windows':
        subprocess.Popen(f'explorer "{folder_path}"')
    elif system == 'Darwin':  # macOS
        subprocess.Popen(["open", folder_path])
    else:  # Linux (and other Unix-like systems)
        subprocess.Popen(["xdg-open", folder_path])

# Create folder if it does not exist in the directory and return path
def mk_dir(parent_dir, directory):
    path = os.path.join(parent_dir, directory)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# Download images from directory if you know the link
def download_batch(cdn_source, image_type, directory, fname, start, end):
    
    folder = fname if fname is not None else directory
    
    path = mk_dir(os.getcwd(), folder)
   
   
    for x in range(start, end + 1):
        image_name = f"0{x}" if x <= 9 else str(x)
        file_name = os.path.join(path, f"{image_name}{image_type}")
       
        try:
            image_url = f"{cdn_source}{directory}/{x}{image_type}"
            urllib.request.urlretrieve(image_url, file_name)
        except urllib.error.HTTPError as e:
            try:
                # Try downloading with alternate image type
                alt_image_type = ".png" if image_type == ".jpg" else ".jpg"
                urllib.request.urlretrieve(f"{cdn_source}{directory}/{x}{alt_image_type}", os.path.join(path, f"{image_name}{alt_image_type}"))
            except urllib.error.HTTPError as e:
                try:
                    # Try downloading with ".gif" as fallback
                    urllib.request.urlretrieve(f"{cdn_source}{directory}/{x}.gif", os.path.join(path, f"{image_name}.gif"))
                except urllib.error.HTTPError as e:
                    print(f"Can't find the image file: {e}")
        except Exception as e:
            # Handle other types of exceptions
            print("Error:", e)
        
    