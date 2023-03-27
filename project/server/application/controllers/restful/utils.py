def min_length(min_length):

  def validate(s):
    if type(s) is not str:
      raise ValueError("Must be at least {0} characters long".format(min_length))
    if len(s) >= min_length:
      return s
    raise ValueError("Must be at least {0} characters long".format(min_length))

  return validate
