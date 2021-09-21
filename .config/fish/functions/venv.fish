function venv --description "activate Python virtualenv from ~/.virtualenvs"
    set -l venv_path ~/.virtualenvs
    set -l venv_shell "$venv_path/$argv[1]/bin/activate.fish"
    source $venv_shell
end
