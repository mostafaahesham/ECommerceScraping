import json

from googletrans import Translator, constants
from pprint import pprint

translator = Translator()
  
print(translator.translate('ابيض').text)
