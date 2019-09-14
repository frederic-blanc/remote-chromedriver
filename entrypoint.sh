#!/bin/bash

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --log-level=*)
        LOG_LEVEL=${1#"--log-level="}
        
        ;;
        --geometry=*)
        SCREEN_GEOMETRY=${1#"--geometry="}
        
        ;;
        --whitelisted-ips=*)
        WHITELISTED_IPS=${1#"--whitelisted-ips="}
        ;;
        --url-base=*)
        URL_BASE=${1#"--url-base="}
        ;;
        *) # arguments
        break
        ;;
    esac
    shift
done

LOG_LEVEL=${LOG_LEVEL:-${CHROMEDRIVER_LOG_LEVEL}}
SCREEN_GEOMETRY=${SCREEN_GEOMETRY:-${XVFB_SCREEN_GEOMETRY}}
WHITELISTED_IPS=${WHITELISTED_IPS:-${CHROMEDRIVER_WHITELISTED_IPS}}
URL_BASE=${URL_BASE:-${CHROMEDRIVER_URL_BASE}}

/usr/bin/xvfb-run   -a      --server-args="-screen 0 ${SCREEN_GEOMETRY} -ac +extension RANDR"   \
    /usr/bin/chromedriver   --port="${CHROMEDRIVER_PORT}"                                       \
                            --log-level="${LOG_LEVEL}"                                          \
                            --whitelisted-ips="${WHITELISTED_IPS}"                              \
                            --url-base="${URL_BASE}"                                            \
                            ${CHROMEDRIVER_EXTRA_ARGS} ${@}
exit $?
