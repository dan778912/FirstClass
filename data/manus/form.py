"""
This module provides a sample query form.
"""

import backendcore.data.form_filler as ff

from templates.fields import CODE

FORM_FLDS = [
    {
        ff.FLD_NM: CODE,
        ff.QSTN: 'Sample:',
        ff.PARAM_TYPE: ff.QUERY_STR,
    },
]


def validate_form_fields(fields: list):
    required_keys = {ff.FLD_NM, ff.QSTN, ff.PARAM_TYPE}
    for field in fields:
        if not required_keys.issubset(field):
            raise ValueError(f"Field missing required keys: {field}")
        

validate_form_fields(FORM_FLDS)


def get_form() -> list:
    return FORM_FLDS


def get_form_descr():
    """
    For Swagger!
    """
    try:
        return ff.get_form_descr(FORM_FLDS)
    except Exception as e:
        raise ValueError(f"Failed to get form description: {e}")


def get_fld_names() -> list:
    return ff.get_fld_names(FORM_FLDS)


def main():
    print(f'Form: {get_form()=}')
    print(f'Form: {get_form_descr()=}')
    print(f'Field names: {get_fld_names()=}')


if __name__ == "__main__":
    main()