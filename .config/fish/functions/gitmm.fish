function gitmm --description "Git merge origin to local master, and prune"
    set -l branch master
    if ! git branch | grep -q $branch
        set branch main
    end
    git fetch --prune
    git checkout $branch
    git merge origin/$branch
end
