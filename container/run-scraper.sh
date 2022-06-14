#!/usr/bin/bash

LVMT_PATH=/root/lvmscraper
LVMT_RMQ=${LVMT_RMQ:=localhost}


echo $LVMT_DEBUG
if [ $LVMT_DEBUG ]; then 
    export PYTHONPATH=$LVMT_PATH/python/
fi

sed "s/host: .*$/host: $LVMT_RMQ/" < $LVMT_PATH/python/lvmscraper/etc/scraper.yml \
            > $LVMT_PATH/python/lvmscraper/etc/lvmscraper_${LVMT_RMQ}.yml


            
python3 $LVMT_PATH/python/lvmscraper/__main__.py -c $LVMT_PATH/python/lvmscraper/etc/lvmscraper_${LVMT_RMQ}.yml --verbose start --debug
