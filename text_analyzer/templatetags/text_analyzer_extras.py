from django import template

register = template.Library()

# this is how we could make django accept more than 2 arguments for filtering
# template tags..
# @register.simple_tag()
# def percentage(argument):
#     args = [arg.strip() for arg in argument.split(',')]
#
#     return str( float(args[0]) / float(args[1]) * 100)
    # return str( float(numerator) / float(denominator) * 100)

@register.simple_tag
def percentage(**kwargs):
    numerator = kwargs['numerator']
    denominator = kwargs['denominator']
    result = float(numerator) / float(denominator) * 100
    return str(int(result * 100)/100) + "%" # round to two decimal places

register.filter('percentage', percentage)