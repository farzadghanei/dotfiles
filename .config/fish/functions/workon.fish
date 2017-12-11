function --description "work on a work project" workon
    set -l name $argv[1]
    set -l work_path ~/work/$name
    set -l venv_path $work_path/.virtualenvs

    if test -z $name
        echo "no project name specified!"
    else
        if test -e $venv_path
            source "$venv_path/$name/bin/activate.fish"
        end

        if test -e $work_path
            cd $work_path
        else
            echo "work dir not found on $work_path"
        end
    end
end
