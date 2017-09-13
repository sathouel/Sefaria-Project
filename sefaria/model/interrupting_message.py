import json
from django.template.loader import render_to_string

class InterruptingMessage(object):
  def __init__(self, attrs={}, request=None):
    if attrs is None:
      attrs = {}
    self.name        = attrs.get("name", None)
    self.repetition  = attrs.get("repetition", 0)
    self.condition   = attrs.get("condition", {})
    self.request     = request
    self.cookie_name = "%s_%d" % (self.name, self.repetition)

  def check_condition(self):
    if not self.name:
    	return False

    # Always show to debug
    if self.condition.get("debug", False):
      return True

    # Don't show this name/repetiion pair more than once
    if self.request.COOKIES.get(self.cookie_name, False):
    	return False

    # Limit to returning visitors only
    if self.condition.get("returning_only", False):
    	if not self.request.COOKIES.get("_ga", False):
    		return False

    # Filter mobile traffic
    if self.condition.get("desktop_only", True):
      if self.request.flavour == "mobile":
        return False

    return True

  def json(self):
    if self.check_condition():
      return json.dumps({
          "name": self.name,
          "html": render_to_string("messages/%s.html" % self.name),
          "repetition": self.repetition
        })
    else:
      return "null"