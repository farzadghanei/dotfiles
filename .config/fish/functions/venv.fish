function --description "activate Python virtualenv from ~/.virtualenvs" venv
    set -l venv_path ~/.virtualenvs
    set -l venv "$venv_path/$argv[1]/bin/activate.fish"
    source $venv
end
