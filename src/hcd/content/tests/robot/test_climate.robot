# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s hcd.content -t test_climate.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src hcd.content.testing.HCD_CONTENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_climate.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Climate
  Given a logged-in site administrator
    and an add climate form
   When I type 'My Climate' into the title field
    and I submit the form
   Then a climate with the title 'My Climate' has been created

Scenario: As a site administrator I can view a Climate
  Given a logged-in site administrator
    and a climate 'My Climate'
   When I go to the climate view
   Then I can see the climate title 'My Climate'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add climate form
  Go To  ${PLONE_URL}/++add++Climate

a climate 'My Climate'
  Create content  type=Climate  id=my-climate  title=My Climate


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the climate view
  Go To  ${PLONE_URL}/my-climate
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a climate with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the climate title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
