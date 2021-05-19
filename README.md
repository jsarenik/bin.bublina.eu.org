# bin.bublina.eu.org

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/jsarenik/bin.bublina.eu.org)

Minimalist POSIX shell reimplementation of
server-side [PrivateBin](https://privatebin.info/),
everything else is the same.

See https://bin.bublina.eu.org
or http://roep6uguk4gv7grlnoc3swz4uomu572ho2x6byzxpp6wfisdfjywe6qd.onion
whereas the former [is front-served by Caddy2](contrib/Caddyfile)
and the latter (onion link) goes straight to
[`busybox httpd` served site](contrib/run).

Notable differences to PrivateBin:

  - i18n not working yet - not important

What works:

  - [Burn after reading](public/cgi-bin/aGETp.sh#L31)
  - [rate limiting](public/cgi-bin/aPOST.sh#L14)
  - [size limit](public/cgi-bin/aPOST.sh#L26-L35)
  - [comments with static avatar for all](public/cgi-bin/aPOST.sh#L38-L50)
  - [correct cleanup of TTL pastebins](contrib/cleanup.sh)

## How to upgrade to current PrivateBin

 1. Clone the current PrivateBin repo.
 2. Add my branch [jsn/local-httpd](https://github.com/jsarenik/PrivateBin/tree/jsn/local-httpd), rebase to master of PrivateBin if needed
 3. Run `./run-site.sh` (requires BusyBox' `httpd` and `php`)
    and keep it running.
 4. Clone [this repo](https://github.com/jsarenik/bin.bublina.eu.org)
    elsewhere.
 5. Inside the cloned `bin.bublina.eu.org` directory
    run `./update-scripts.sh`.
