# Defined in - @ line 1
function gitl --wraps='git log' --wraps='git log -w -p HEAD' --description 'alias gitl git log -w -p HEAD'
  git log -w -p HEAD $argv;
end
