"""
Given a list of args as strings and a body which is a Discord interaction,
return a list of values corresponding to the given args.
"""
def get_slash_args(args, body):
    options = body["data"]["options"]
    options_dict = {option["name"]: option["value"] for option in options}
    return [options_dict[arg] if arg in options_dict else None for arg in args]