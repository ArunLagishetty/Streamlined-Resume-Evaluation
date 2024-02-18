
from bardapi import BardCookies

from bardapi import Bard

bard = BardCookies(token_from_browser=True)
print(bard.get_answer("give me some questions ir the topic datascience for interviewing my candidate")['content'])