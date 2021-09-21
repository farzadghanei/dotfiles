# Defined in - @ line 1
function gitd --wraps='git diff' --description 'alias gitd git diff'
  git diff $argv;
end
