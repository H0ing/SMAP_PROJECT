from abc import ABC , abstractmethod

class Report(ABC):

  def __init__(self, title):
    self.__title = title


  
  @property
  def title(self):
    return self.__title
  
  @abstractmethod
  def generate_report(self):
    pass


  @abstractmethod
  def content_report(self):
    pass


  def save_to_file(self, filepath):
    pass




def greeting():
    print("Hello from the report module")



if __name__ == '__main__':
  greeting()
