#
# Autogenerate an Options.py file from the RDI argument specs.
#
import io
import math

from ctrando.arguments import arguments, argumenttypes


option_class_buf = io.StringIO()
dataclass_buf = io.StringIO()
option_groups_buf = io.StringIO()

group_name_list: list[str] = []

args_to_omit = [
    "ending"
]


def get_class_name(val: str) -> str:
    return ''.join(x.capitalize() for x in val.split('_'))


def get_display_name(val: str) -> str:
    return val.replace('_', ' ').title()


def write_toggle_control(flag: str, spec: argumenttypes.FlagArg):
    control = f'''
class {get_class_name(flag)}(Toggle):
    """{spec.help_text}"""
    display_name = "{get_display_name(flag)}"\n\n'''
    option_class_buf.write(control)


def write_range_control(flag: str, spec: argumenttypes.DiscreteNumericalArg):

    if spec.type_fn is not int:
        # AP ranges don't support floats
        # Get nearest valid int
        min_val = math.ceil(spec.min_value)
        max_val = math.floor(spec.max_value)
        default_val = math.floor(spec.default_value)
    else:
        min_val = spec.min_value
        max_val = spec.max_value
        default_val = spec.default_value

    control = f'''
class {get_class_name(flag)}(Range):
    """{spec.help_text}"""
    display_name = "{get_display_name(flag)}"
    range_start = {min_val}
    rage_end = {max_val}
    default = {default_val}\n\n'''
    option_class_buf.write(control)


def write_choice_control(flag: str, spec: argumenttypes.DiscreteCategorialArg):
    control = f'''
class {get_class_name(flag)}(Choice):
    """{spec.help_text}"""
    display_name = "{get_display_name(flag)}"\n'''
    option_class_buf.write(control + "\n")

    # Write each choice value
    default_val = 0
    counter = 0
    for choice in spec.choices:
        choice_str = spec.str_from_choice_fn(choice)
        if choice == spec.default_value:
            default_val = counter

        # "random" seems to be a reserved value in AP choice types
        # So we need to rename it to avoid errors
        # TODO: Need a better way to deconflict these names
        if choice_str == "random":
            choice_str = "rdi_random"

        choice_str = choice_str.replace(' ', '_')
        choice_str = choice_str.replace('?', '')
        option_class_buf.write(f"    option_{choice_str} = {counter}\n")
        counter = counter + 1

    option_class_buf.write(f"    default = {default_val}\n\n")


def write_string_control(flag: str, spec: argumenttypes.StringArgument):
    control = f'''
class {get_class_name(flag)}(FreeText):
    """{spec.help_text}"""
    display_name = "{get_display_name(flag)}"
    default = ""\n\n'''
    option_class_buf.write(control)


def parse_option_group(group_name: str, arg_spec: dict):

    if group_name not in group_name_list:
        if group_name_list:
            # Close out the previous group
            option_groups_buf.write('''
        ]
    ),\n''')
        option_groups_buf.write(f'''
    OptionGroup(
        "{get_display_name(group_name)}",
        [\n''')
        group_name_list.append(group_name)

    for flag, spec in arg_spec.items():
        if flag in args_to_omit:
            continue

        if isinstance(spec, dict):
            # Recursive arg specs
            parse_option_group(group_name, spec)
        else:
            if not isinstance(spec, argumenttypes.MultipleDiscreteSelection):
                dataclass_buf.write(f"    {flag}: {get_class_name(flag)}\n")
                option_groups_buf.write(
                    f"            {get_class_name(flag)},\n")

        if isinstance(spec, argumenttypes.FlagArg):
            write_toggle_control(flag, spec)
        elif isinstance(spec, argumenttypes.DiscreteNumericalArg):
            write_range_control(flag, spec)
        elif isinstance(spec, argumenttypes.DiscreteCategorialArg):
            write_choice_control(flag, spec)
        elif isinstance(spec, argumenttypes.MultipleDiscreteSelection):
            # TODO: Not sure how to do these in AP
            pass
        elif isinstance(spec, argumenttypes.StringArgument):
            write_string_control(flag, spec)


def main():

    option_class_buf.write('''
from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, FreeText, OptionGroup, \\
    PerGameCommonOptions, Range, Toggle\n\n''')

    dataclass_buf.write('''
@dataclass
class CTRDIOptions(PerGameCommonOptions):\n''')

    option_groups_buf.write('''\n
option_groups: list[OptionGroup] = [\n''')

    arg_specs = arguments.Settings.get_argument_spec()
    for section_name, arg_spec in arg_specs.items():
        if section_name == "plando_options":
            continue
        parse_option_group(section_name, arg_spec)

    # Close out the last option group
    option_groups_buf.write('''
        ]
    )
]
''')

    # Write everything to the options file
    option_class_buf.seek(0)
    dataclass_buf.seek(0)
    option_groups_buf.seek(0)
    with open("Options.py", 'w') as file:
        file.write(option_class_buf.read())
        file.write(dataclass_buf.read())
        file.write(option_groups_buf.read())


if __name__ == "__main__":
    main()
