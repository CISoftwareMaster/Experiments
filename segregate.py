import re


data = [
    "Jane Green",
    "John Brown",
    "johnbrown@goomail.com",
    "www.tasks.org",
    "johnnyappleseed@wahhoo.com",
    "Justin Time",
    "johnattanegg@english.something",
    "Polly Politics",
    "Arnold Armitage",
    "vote.now.org",
    "Christine Chops",
    "white@black.colours",
    "pay.taxes.gov",
    "www.website.com",
    "J Julius Abacus Williams",
    "no.privacy-on_the_internet@anonymous.net",
    "Theresa White",
    "https://a_really_secure_website.org",
    "http://lesssecure.com",
    "https://free_internet.org",
    "annie63@doctor.net",
    "starship-uk.net",
    "free059.internet.net",
    "julia_c59@skynet.org"
]


# printing function
def print_list(l: list, name: str):
    print("\n%s (%i items): " % (name, len(l)))
    for item in l:
        print(item)
    print("-------------")


names = list()
emails = list()
websites = list()
unclassified = list()

# compile regular expression patterns
email = re.compile("(\W|\w)*.@\w+?\.")
website = re.compile("^(http[s]?:[\/]{2})?.((w{2}|[\w\W\d]{0,4}))?.([\w\W\d]*)?\.(.[\w\W\d]*)?$")
name = re.compile("\w*[A-z]*\ .[A-z]*")

# check for matches in the data set
for item in data:
    if email.match(item):
        emails.append(item)
    elif website.match(item):
        websites.append(item)
    elif name.match(item):
        names.append(item)
    else:
        unclassified.append(item)

# print the data bins
print_list(names, "Names")
print_list(emails, "Email Addresses")
print_list(websites, "Website Addresses")
print_list(unclassified, "Unclassified")
