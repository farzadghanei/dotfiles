# Defined in - @ line 1
function gitc --wraps='git checkout' --description 'alias gitc git checkout'
  git checkout $argv;
end
