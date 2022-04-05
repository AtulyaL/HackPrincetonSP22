import major_scrapper
import reference


def major_courses(major):
    url = "https://www.princeton.edu/academics/area-of-study/" + \
        major.lower().replace(" ", "-")
    return major_scrapper.get_major_courses(url)


def valid_department(department):
    try:
        return reference.courses[department.upper()]
    except:
        return "Invalid Department. Please try again."
