function gitmm --description "Git merge origin to local master, and prune"
    git fetch --prune
    git checkout master
    git merge origin/master
end
