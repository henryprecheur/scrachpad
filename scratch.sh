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
    readonly flags='+set ft=markdown spell'
    if test -z "$DISPLAY"
    then
        vim "$flags" $@ < /dev/tty > /dev/tty
    else
        gvim --nofork "$flags" $@
    fi
}

function publish {
    {
        rfc3339
        echo
        cat $@
    } | ssh henry@alena.koalabs.org "$remote_script"
}

function transaction {
    readonly tmp=$(mktemp)

    if test -n "$*"
    then
        cat "$*" > $tmp
    fi

    edit "$tmp"

    while test -f "$tmp"
    do
        case $(read 'Publish,Keep,Edit? ') in
            [pP]*)
                publish "$tmp" && rm "$tmp"
                ;;
            [Kk]*)
                readonly save="$HOME/.scratch.$(rfc3339)"
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

transaction $@
