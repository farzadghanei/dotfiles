function --description "work on a project" be
    set -l name $argv[1]
    set -l venv_path ~/.virtualenvs/$name
    set -l work_path ~/projects/$name

    if test -z $name
        echo "no project name specified!"
    else
        if test -e $venv_path
            venv $name
        end

        if test -e $work_path
            cd $work_path
        else
            echo "project work dir not found on $work_path"
        end
    end
end
