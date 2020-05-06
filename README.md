# bin.bublina.eu.org
Minimalist POSIX shell reimplementation of PrivateBin

See https://bin.bublina.eu.org
or http://roep6uguk4gv7grlnoc3swz4uomu572ho2x6byzxpp6wfisdfjywe6qd.onion
whereas the former [is front-served by Caddy2](contrib/Caddyfile)
and the latter (onion link) goes straight to
[`busybox httpd` served site](contrib/run).

Notable differences to PrivateBin:

  - i18n not working yet - not important
  - [correct cleanup of TTL pastebins not implemented yet](contrib/cleanup.sh)

What works:

  - [Burn after reading](public/cgi-bin/aGETp.sh#L31)
  - [rate limiting](public/cgi-bin/aPOST.sh#L14)
  - [size limit](public/cgi-bin/aPOST.sh#L26-L35)
  - [comments with static avatar for all](public/cgi-bin/aPOST.sh#L38-L50)
