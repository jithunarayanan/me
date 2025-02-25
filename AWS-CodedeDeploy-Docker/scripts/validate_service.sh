#!/bin/bash

# verify we can access our webpage successfully
#curl -v --silent localhost:3001 2>&1 | grep function
#curl -s -w "%{http_code}\n" localhost:3001 2>&1 error.log | grep -q 200

#!/bin/bash

url="localhost:3001"
status=$(curl -s -w "%{http_code}" -o /dev/null $url)

if [ $status -eq 200 ]; then
  echo "Website is up and running (status code: $status)"
else
  echo "Website is down or returned an error (status code: $status)"
fi

