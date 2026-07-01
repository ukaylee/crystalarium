class Crystal:
  def __init__(self, id, name, props, desc):
    self.id = id
    self.name = name
    self.props = props
    self.desc = desc

  def get_name(self):
    return self.name

  def get_props(self):
    return self.props

  def get_desc(self):
    return self.desc