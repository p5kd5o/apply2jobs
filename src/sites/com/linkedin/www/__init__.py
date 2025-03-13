import linkedin_api

from sites import get_package_site

SITE_SHORTNAME = "LinkedIn"
SITE = get_package_site(__package__)
CLIENT_TYPE = linkedin_api.Linkedin
