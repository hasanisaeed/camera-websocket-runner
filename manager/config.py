import configparser

class SectionType(type):
    def __new__(cls, name, bases, cls_dict, section_name, items_dict):
        cls_dict['__doc__'] = f'Configs for {section_name} section'
        cls_dict['section_name'] = section_name
        for key, value in items_dict.items():
            cls_dict[key] = value
        return super().__new__(cls, name, bases, cls_dict)


def environment(env= 'conf.ini'):
    def wrapper(cls):
        config = configparser.ConfigParser()
        config.read(env)
        for section_name in config.sections():
            class_name = cls.__qualname__
            class_attribute_name = section_name.casefold()
            section_items = config[section_name] 
            Section = SectionType(
                class_name, (), {}, section_name=section_name, items_dict=section_items
            )
            setattr(cls, class_attribute_name, Section)    
            
        return cls
    return wrapper
