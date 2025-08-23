# Dump DDL for the StatBucket DB 
ddl_filename="ddl.sql"
DIR="../sql"
if [ ! -d "$DIR" ]; then
    echo "Creating directory $DIR"
    mkdir -p "$DIR"
fi
echo "loading .env"
source load_env.sh
mysqldump -u $BACKEND_DB_USER -p$BACKEND_DB_PASSWORD --no-data --routines --triggers $BACKEND_DB_NAME > $DIR/$ddl_filename