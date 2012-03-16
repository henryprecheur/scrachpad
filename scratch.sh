#!/bin/sh

remote_script='rc -e /var/www/henry.precheur.org/scratchpad/publish.rc'

function rfc3339 {
    date +%FT%T%z | sed 's/\([+-][01][0-9]\)\([0-9][0-9]\)$/\1:\2/'
}

function read {
    echo -n "$*" > /dev/tty
    awk '{print;exit}' < /dev/tty
}

function edit {
    typeset flags='+set ft=markdown spell'
    if test -z "$DISPLAY"
    then
        vim "$flags" "$*" < /dev/tty > /dev/tty
    else
        gvim --nofork "$flags" "$*"
    fi
}

function publish {
    {
        rfc3339
        echo
        cat "$*"
    } | ssh henry@alena.koalabs.org "$remote_script"
}

function transaction {
    if test -z "$*"
    then
        typeset tmp=$(mktemp)
    else
        typeset tmp="$*"
    fi

    edit "$tmp"

    while test -f "$tmp"
    do
        case $(read 'Publish,Keep,Edit? ') in
            [pP]*)
                publish "$tmp" && rm "$tmp"
                ;;
            [Kk]*)
                typeset save="$HOME/.scratch.$(rfc3339)"
                mv "$tmp" "$save"
                echo "$save"
                ;;
            [Ee]*)
                echo Editing
                edit "$tmp"
                ;;
            *)
                echo Invalid command
                ;;
        esac
    done
}

transaction "$*"
