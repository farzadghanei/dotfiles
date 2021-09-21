# Defined in - @ line 1
function gitf --wraps='git fetch --prune' --description 'alias gitf git fetch --prune'
  git fetch --prune $argv;
end
