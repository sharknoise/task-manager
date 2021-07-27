# DANGER DANGER DANGER: If you use these settings and run tests, they will
# install vacuous testing data on your database.

# Note that the default ./manage.py test behavior creates a fresh database
# to test on. But the whole point of Heroku is to magically create all the
# stuff you need. It's totally appropriate that THEY make the testing database
# and we just use it. Simple. Easy. But the assumption that your web framework
# will administer your testing databases is pretty well baked into Django,
# hence this kind of hack.

# See https://gist.github.com/cordery/d52d9ba44541fabaf4b012f4e62d675b
# for more discussion.

# The environments.test section in app.json is really important here.

from django.test.runner import DiscoverRunner

from task_manager.settings import *

TEST_RUNNER = 'task_manager.heroku_ci_test_settings.ExistingDBDiscoverRunner'


class ExistingDBDiscoverRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
