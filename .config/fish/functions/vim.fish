function vim --description "run vim with proper initialization files"
    # if set -q VIMRC && test -n "$VIMRC" && test -e "$VIMRC"
    if set -q VIMRC; and test -e "$VIMRC"
        command vim -u "$VIMRC" $argv
    else
        command vim $argv
    end
end
