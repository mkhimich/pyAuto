# pyAuto
Python automation framework

to run test use:
``nosetests --with-flaky --force-flaky --max-runs=2 --min-passes=1 -v --with-xunit --nologcapture test.py``
or
``py.test androidtest/android_real.py -d --tx 2*popen//python=python3.5 --force-flaky --max-runs=2 --min-passes=1``