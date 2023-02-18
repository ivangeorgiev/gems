def select(field_list):
    def select_transformation(row):
        result = {}
        for f in _field_list:
            result[f] = row[f]
        return result
    if isinstance(field_list, str):
        _field_list = [field_name.strip() for field_name in field_list.split(',')]
    return select_transformation

def update_field(field_name, func):
    def update_field_transformation(row):
        row[field_name] = func(row[field_name])
        return row
    return update_field_transformation

