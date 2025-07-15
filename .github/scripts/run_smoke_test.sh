#!/bin/bash

OPENAI_API_KEY=$1
OPENAI_ENDPOINT=$2
TEST_BRANCH_NAME=${3:-main}

BASE_DIR=~/moonshot
SCRIPTS_DIR=~/scripts

# Export the env variables for smoke test to use
export OPENAI_TOKEN=$OPENAI_API_KEY
export OPENAI_URI=$OPENAI_ENDPOINT
export MOONSHOT_URL="http://127.0.0.1"
export MOONSHOT_PORT_NUMBER="3100"
export ADDITIONAL_PARAMETERS="{
  'timeout': 300,
  'allow_retries': true,
  'num_of_retries': 3,
  'temperature': 0.5,
  'model': 'gpt-4o'
}"

cd $BASE_DIR

if [ -d "moonshot-smoke-testing-aisi" ]; then
  echo "Removing existing moonshot-smoke-testing-aisi directory..."
  rm -rf moonshot-smoke-testing-aisi
fi

# Clone the smoke test repo from the specified branch
echo "Cloning moonshot-smoke-testing repo from branch $BRANCH_NAME..."
git clone --branch $TEST_BRANCH_NAME https://github.com/sgaisi/moonshot-smoke-testing-aisi.git
cd moonshot-smoke-testing-aisi
npm ci

cp $SCRIPTS_DIR/moonshot_test_env .env
echo "Created .env"
cat .env

# Install Playwright (if needed)
#sudo npx playwright install-deps
### If the above didn't work, try the following:
##sudo apt-get install libatk1.0-0\
##         libatk-bridge2.0-0\
##         libxkbcommon0\
##         libatspi2.0-0\
##         libxcomposite1\
##         libxdamage1\
##         libxfixes3\
##         libxrandr2\
##         libgbml

echo "Running smoke test on moonshot at $MOONSHOT_URL:$MOONSHOT_PORT_NUMBER..."
npx playwright test tests/smoke-test.spec.ts --reporter=list

#echo "Exit code: $?"
