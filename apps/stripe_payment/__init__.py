def create_empty_file(filename):
  """Creates an empty file with the specified filename.

  Args:
    filename: The name of the file to create.
  """
  with open(filename, 'w') as f:
    pass

if __name__ == '__main__':
  file_name = "my_empty_file.txt"  # Replace with your desired filename
  create_empty_file(file_name)
  print(f"Empty file '{file_name}' created successfully.")