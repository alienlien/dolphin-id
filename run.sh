#!/bin/bash
# Config for mongo db.
# Usage: run.sh [mongo|parse|all]
MONGODB_PORT=27017
MONGODB_DBPATH=/tmp/mongo
MONGODB_LOGPATH=/tmp/logs/mongo/server1.log

# Config for parse server.
PARSE_APPLICATION_ID=1
PARSE_MASTER_KEY=abc123
PARSE_PORT=1337
PARSE_DATABASE_URI=mongodb://localhost:$MONGODB_PORT/parse
PARSE_LOGS_FOLDER=/tmp/logs/parse

# Runs mongo db.
if [ "$1" == "all" ] || [ "$1" == "mongo" ]; then
    mongod \
        --verbose \
        --logpath $MONGODB_LOGPATH \
        --port $MONGODB_PORT \
        --dbpath $MONGODB_DBPATH &

    # Wait for the mongo db ready.
    sleep 5
fi

# Runs parse server.
if [ "$1" == "all" ] || [ "$1" == "parse" ]; then
    parse-server \
        --verbose \
        --jsonLogs \
        --logsFolder $PARSE_LOGS_FOLDER \
        --appId $PARSE_APPLICATION_ID \
        --masterKey $PARSE_MASTER_KEY \
        --port $PARSE_PORT \
        --databaseURI $PARSE_DATABASE_URI &
fi
