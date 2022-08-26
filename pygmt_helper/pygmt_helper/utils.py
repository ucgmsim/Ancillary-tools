IM_NAME_LOOKUP = {}

def get_im_name(id: str):
    """Gets the proper feature name for the specified 'id'"""
    name = IM_NAME_LOOKUP.get(id)

    if id.startswith("pSA"):
        return f"pSA({id.split('_')[-1]}s)"

    if name is None:
        return id
    return name