import subprocess
import sys
import os
import shutil


def extract_voice(path):
  #print(path)
  index = path.rfind(".")
  new_path = path if index == -1 else path[:index+1] + "wav"
  command = "avconv -i "+ path + " -ab 160k -ac 1 -ar 16000 -vn " + new_path
  print(command);
  subprocess.call(command, shell=True)

def generate_frames(target, file_name):
  index = file_name.rfind(".")
  input_directory = target + file_name
  output_directory = target + (file_name if index == -1 else file_name[:index+1].replace(".", "")) + 'out'

  if not os.path.exists(output_directory):
      os.mkdir(output_directory)

  command = "avconv -i " + input_directory + " -vsync 1 -r 10 -an -y -qscale 1 -s 256x256 " + output_directory + "/%06d.jpg"
  subprocess.call(command, shell=True)



def generate_video(target, file_name):
  index = file_name.rfind(".")
  input_generic_name = (file_name if index == -1 else file_name[:index+1].replace(".", ""))
  frames_path = target + input_generic_name + 'out'
  audio_path = target + input_generic_name + ".wav"
  output_path = target + input_generic_name + "out.mp4"
  command = "avconv -r 10 -i " + frames_path + "/%06d.jpg -i " + audio_path  + "  -c:v libx264 -c:a libmp3lame  -crf 10 -r 10 -shortest -y " + output_path
  subprocess.call(command, shell=True)

def pre_process(target, destination, file_name):
    extract_voice(destination)
    generate_frames(target, file_name)

def clean_data(target):
    if os.path.exists(target):
        shutil.rmtree(target)
        os.mkdir(target)
