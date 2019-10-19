FROM    rpi/debian:buster

RUN     useradd chrome  --shell /bin/bash   --create-home

RUN     apt-get update                                          \
                                                            &&  \
        apt-get upgrade -y                                      \
                                                            &&  \
        apt autoremove  -y                                      \
                                                            &&  \
        apt-get clean   -y                                      \
                                                            &&  \
        rm  -rf /var/lib/apt/lists/*        /var/cache/apt/*


RUN     apt-get update                                          \
                                                            &&  \
        apt-get install -y  --no-install-recommends             \
                            locales                             \
                            xvfb                                \
                            xauth                               \
                            x11-xserver-utils                   \
                                                            &&  \
        apt-get clean   -y                                      \
                                                            &&  \
        rm  -rf /var/lib/apt/lists/*        /var/cache/apt/*

RUN     apt-get update                                          \
                                                            &&  \
        apt-get install -y  --no-install-recommends             \
                            chromium-browser                    \
                            chromium-browser-l10n               \
                            chromium-driver                     \
                            xfonts-cyrillic                     \
                            xfonts-100dpi                       \
                            xfonts-75dpi                        \
                            xfonts-base                         \
                            xfonts-scalable                     \
                            fonts-liberation                    \
                                                            &&  \
        apt-get clean   -y                                      \
                                                            &&  \
        rm  -rf /var/lib/apt/lists/*        /var/cache/apt/*

RUN     ln  -s  /usr/bin/chromium-browser   /usr/bin/google-chrome

ENV     CHROMEDRIVER_PORT               '4444'
ENV     CHROMEDRIVER_LOG_LEVEL          'INFO'
ENV     CHROMEDRIVER_WHITELISTED_IPS    ''
ENV     CHROMEDRIVER_URL_BASE           ''
ENV     CHROMEDRIVER_EXTRA_ARGS         ''
ENV     XVFB_SCREEN_GEOMETRY            '1600x900x24'

EXPOSE  4444
VOLUME  [ "/home/chrome" ]

ADD     entrypoint.sh       /
RUN     chmod   755     /entrypoint.sh

USER    chrome

ENTRYPOINT  [ "/entrypoint.sh" ]
